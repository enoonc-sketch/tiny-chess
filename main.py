import json,os,urllib.request
U=os.environ['MAKEFUN_ENV_URL']
V=(0,100,320,330,500,900,0)
ND=(-33,-31,-18,-14,14,18,31,33);KD=(-17,-16,-15,-1,1,15,16,17);BD=(-17,-15,15,17);RD=(-16,-1,1,16)
CF=(0,1,2,3,3,2,1,0)
P=[[0]*128 for _ in range(13)]
for s in range(128):
 if s&136:continue
 f=s&7;r=s>>4;g=CF[f];c=g+CF[r]
 for t,v in enumerate((8*r+3*g,5*c,4*c,2*g,2*c,-4*g-6*r),7):
  P[t][s]=v;P[12-t][s^112]=v
B=[0]*128;S=1;C=15;E=-1;sc=0;KS=[4,116];N=[0];I=999999
def setup(mv):
 global S,C,E,sc
 B[:]=[0]*128
 for i,p in enumerate((4,2,3,5,6,3,2,4)):B[i]=p;B[i+112]=-p;B[i+16]=1;B[i+96]=-1
 S=1;C=15;E=-1;sc=0;KS[:]=4,116
 for u in mv:mk(fu(u))
def atk(s,by):
 if any(not ((s+dd)&136) and B[s+dd]==by for dd in (-16*by-1,-16*by+1)):return 1
 for ds,pp,sl in ((ND,2,0),(KD,6,0),(RD,4,1),(BD,3,1)):
  for dd in ds:
   u=s+dd
   while not (u&136):
    q=B[u]
    if q:
     if q==pp*by or q==5*by and sl:return 1
     break
    if not sl:break
    u+=dd
 return 0
def gen(cap):
 ms=[];A=ms.append
 for s in range(128):
  p=B[s]
  if not p or p*S<0:continue
  t=abs(p)
  if t==1:
   d=16*S;pr=(s>>4)==(6 if S>0 else 1)
   for dd in (d,d-1,d+1):
    u=s+dd
    if u&136:continue
    q=B[u]
    if cap and dd==d or q and (dd==d or q*S>0 or abs(q)==6) or dd!=d and not q and u!=E:continue
    if pr:
     for r in (5,4,3,2):A(s|u<<7|r<<14)
    else:
     A(s|u<<7)
     if dd==d and not cap and (s>>4)==(1 if S>0 else 6) and not B[s+2*d]:A(s|(s+2*d)<<7)
  else:
   ds=(ND,BD,RD,KD,KD)[t-2]
   sl=2<t<6
   for d in ds:
    u=s+d
    while not (u&136):
     q=B[u]
     if q:
      if q*S<0 and abs(q)!=6:A(s|u<<7)
      break
     if not cap:A(s|u<<7)
     if not sl:break
     u+=d
 if not cap:
  ks=4 if S>0 else 116
  for d,bt in ((1,1),(-1,2)):
   if C&(bt if S>0 else bt*4) and not B[ks+d] and not B[ks+2*d] and (d>0 or not B[ks+3*d]) and all(not atk(ks+i*d,-S) for i in (0,1,2)):A(ks|(ks+2*d)<<7)
 return ms
def mk(m):
 global S,C,E,sc
 f=m&127;t=(m>>7)&127;pr=m>>14
 p=B[f]
 cap=B[t];cs=t
 if abs(p)==1 and t%8!=f%8 and not cap:
  cs=t-16*S;cap=B[cs]
 u=(cap,cs,C,E,sc)
 sg=(p>0)*2-1
 np=pr*S if pr else p
 B[f]=B[cs]=0;B[t]=np
 sc+=(V[abs(np)]+P[np+6][t]-V[abs(p)]-P[p+6][f])*sg
 if cap:sc+=(V[abs(cap)]+P[cap+6][cs])*sg
 if abs(p)==6:
  KS[1-(S>0)]=t;C&=~(3 if S>0 else 12)
  if abs(t-f)==2:
   rf=f+3 if t>f else f-4;rt=f+1 if t>f else f-1
   r=B[rf];B[rt],B[rf]=r,0
   sc+=(P[r+6][rt]-P[r+6][rf])*sg
 for sq,bt in ((0,2),(7,1),(112,8),(119,4)):
  if f==sq or t==sq:C&=~bt
 E=f+16*S if abs(p)==1 and t-f==32*S else -1
 S=-S
 return u
def un(m,u):
 global S,C,E,sc
 f=m&127;t=(m>>7)&127;pr=m>>14
 cap,cs,C,E,sc=u
 S=-S
 p=S if pr else B[t]
 B[f]=p;B[t]=0
 if cap:B[cs]=cap
 if abs(p)==6:
  KS[1-(S>0)]=f
  if abs(t-f)==2:
   rf=f+3 if t>f else f-4;rt=f+1 if t>f else f-1
   B[rf],B[rt]=B[rt],0
def capv(m):
 q=B[(m>>7)&127]
 return (10*V[abs(q)]-V[abs(B[m&127])] if q else 0)
def s(d,a,b):
 N[0]+=1
 if N[0]>120000:1/0
 if d<=0:
  v=sc*S
  if v>=b:return b
  if v>a:a=v
 c=atk(KS[1-(S>0)],-S)
 m=gen(not(d>0 or c))
 m.sort(key=capv,reverse=True)
 z=-I
 for x in m:
  u=mk(x)
  if atk(KS[1-(S<0)],S):
   un(x,u);continue
  v=-s(d-1,-b,-a)
  un(x,u)
  z=max(z,v);a=max(a,v)
  if a>=b:break
 if d<=0:
  if z==-I:return -100000 if c else 0
  return a
 if z==-I:return -100000-d if c else 0
 return z
def root(ms):
 if len(ms)==1:return ms[0]
 ms.sort(key=capv,reverse=True)
 best=ms[0]
 N[0]=0
 for d in range(12):
  try:
   a=-I
   for x in ms:
    u=mk(x);v=-s(d,-I,I);un(x,u)
    if v>a:a=v;best=x
  except Exception:break
 return best
def post(p,b):
 return json.load(urllib.request.urlopen(U+p,json.dumps(b).encode()))
def uci(m):
 return chr(97+(m&7))+str((m>>4&7)+1)+chr(97+(m>>7&7))+str((m>>11&7)+1)+('  nbrq'[m>>14] if m>>14 else '')
def fu(u):
 f=ord(u[0])-97|(int(u[1])-1)<<4;t=ord(u[2])-97|(int(u[3])-1)<<4
 return f|t<<7|(('nbrq'.index(u[4])+2)<<14 if len(u)==5 else 0)
g=post('/game',{})
while g['status']!='done':
 while g['status']=='your_move':
  setup(g['moves'])
  ms=[fu(u) for u in g['legal_moves']]
  g=post('/move',{'game':g['game'],'move':uci(root(ms))})
 g=post('/game',{})
