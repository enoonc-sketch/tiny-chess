import json,os,urllib.request
U=os.environ['MAKEFUN_ENV_URL'];o=urllib.request.urlopen
V=(0,100,320,330,500,900,0)
ND=(-33,-31,-18,-14,14,18,31,33);KD=(-17,-16,-15,-1,1,15,16,17);BD=(-17,-15,15,17);RD=(-16,-1,1,16)
CF=(0,1,2,3,3,2,1,0)
P=[[0]*128 for _ in range(13)]
for s in range(128):
 if s&136:continue
 f=s&7;r=s>>4;g=CF[f];c=g+CF[r]
 for t,v in enumerate((8*r+3*g+r*g,5*c,4*c,2*g,2*c,-4*g-6*r),7):
  P[t][s]=v;P[12-t][s^112]=v
W=lambda p,s:V[abs(p)]+P[p+6][s]
B=[0]*128;S=1;C=15;sc=0;KS=[4,116];N=[0];I=999999;T={};K=[0]*12
def setup(mv):
 global S,C,sc
 B[:]=[0]*128
 for i,p in enumerate((4,2,3,5,6,3,2,4)):B[i]=p;B[i+112]=-p;B[i+16]=1;B[i+96]=-1
 S=1;C=15;sc=0;KS[:]=4,116
 for u in mv:mk(fu(u))
def atk(s,by):
 if any(B[s+dd]==by for dd in(-16*by-1,-16*by+1)if not(s+dd)&136):return 1
 for ds,pp,sl in((ND,2,0),(KD,6,0),(RD,4,1),(BD,3,1)):
  for dd in ds:
   u=s+dd
   while not(u&136):
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
   d=16*S;pr=(s>>4)==1+5*(S>0)
   for dd in(d,d-1,d+1):
    u=s+dd
    if u&136:continue
    q=B[u]
    if dd==d and(cap or q)or dd!=d and(q and(q*S>0 or abs(q)==6)or not q):continue
    if pr:
     for r in(5,4,3,2):A(s|u<<7|r<<14)
    else:
     A(s|u<<7)
     if dd==d and not cap and(s>>4)==6-5*(S>0) and not B[s+2*d]:A(s|(s+2*d)<<7)
  else:
   ds=(ND,BD,RD,KD,KD)[t-2]
   sl=2<t<6
   for d in ds:
    u=s+d
    while not(u&136):
     q=B[u]
     if q:
      if q*S<0 and abs(q)!=6:A(s|u<<7)
      break
     if not cap:A(s|u<<7)
     if not sl:break
     u+=d
 if not cap:
  ks=116-112*(S>0)
  for d,bt in((1,1),(-1,2)):
   if C&(bt<<2 if S<0 else bt) and not(B[ks+d]or B[ks+2*d]) and(d>0 or not B[ks+3*d]):A(ks|(ks+2*d)<<7)
 return ms
def mk(m):
 global S,C,sc
 f=m&127;t=(m>>7)&127;pr=m>>14
 p=B[f]
 cap=B[t]
 u=(cap,C,sc)
 sg=(p>0)*2-1
 np=pr*S if pr else p
 B[f]=0;B[t]=np
 sc+=(W(np,t)-W(p,f))*sg
 if cap:sc+=W(cap,t)*sg
 if abs(p)==6:
  KS[1-(S>0)]=t;C&=~(3 if S>0 else 12)
  if abs(t-f)==2:
   rf=f+3 if t>f else f-4;rt=f+1 if t>f else f-1
   r=B[rf];B[rt],B[rf]=r,0
   sc+=(W(r,rt)-W(r,rf))*sg
 for x in(f,t):
  if x in(0,7,112,119):C&=~(1<<((x&7==0)+2*(x>>4==7)))
 S=-S
 return u
def un(m,u):
 global S,C,sc
 f=m&127;t=(m>>7)&127;pr=m>>14
 cap,C,sc=u
 S=-S
 p=S if pr else B[t]
 B[f]=p;B[t]=0
 if cap:B[t]=cap
 if abs(p)==6:
  KS[1-(S>0)]=f
  if abs(t-f)==2:
   rf=f+3 if t>f else f-4;rt=f+1 if t>f else f-1
   B[rf],B[rt]=B[rt],0
def capv(m):
 q=B[m>>7&127]
 return 10*V[abs(q)]-V[abs(B[m&127])]if q else 0
def s(d,a,b):
 N[0]+=1
 if N[0]>360000:1/0
 if d>0:
  k=(tuple(B),S,C);e=T.get(k)
  if e and e[0]>=d and(e[1]==1 or e[2]>=b):return e[2]
  t=e[3]if e else 0
 if d<=0:
  v=sc*S
  if v>=b:return b
  if v>a:a=v
 c=atk(KS[S<0],-S)
 m=gen(not(d>0 or c))
 m.sort(key=capv,reverse=True)
 if d>0:
  for q in(K[d],t):
   if q in m:m.remove(q);m.insert(0,q)
 a0=a;z=-I;bm=0
 for x in m:
  u=mk(x)
  if atk(KS[not(S<0)],S):
   un(x,u);continue
  v=-s(d-1,-b,-a)
  un(x,u)
  if v>z:z=v;bm=x
  if v>a:a=v
  if a>=b:K[max(d,0)]=x;break
 if d<=0:return -100000 if z==-I and c else a
 if z==-I:return -100000-d if c else 0
 if z>a0:
  if len(T)>2e5:T.clear()
  T[k]=(d,1+(z>=b),z,bm)
 return z
def root(ms):
 best=ms[0]
 N[0]=0
 for d in range(12):
  try:
   a=-I;b2=best
   for x in ms:
    u=mk(x);v=-s(d,-I,I);un(x,u)
    if v>a:a=v;b2=x
   best=b2
  except Exception:break
 return best
def post(p,b):
 return json.load(o(U+p,json.dumps(b).encode()))
q=lambda x:chr(97+(x&7))+str((x>>4&7)+1)
uci=lambda m:q(m)+q(m>>7)+('  nbrq'[m>>14] if m>>14 else '')
def fu(u):
 f=ord(u[0])-97|int(u[1])-1<<4;t=ord(u[2])-97|int(u[3])-1<<4
 return f|t<<7|(('nbrq'.index(u[4])+2)<<14 if len(u)==5 else 0)
while(g:=post('/game',{}))['status']!='done':
 while g['status']=='your_move':
  setup(g['moves']);ms=[fu(u) for u in g['legal_moves']]
  g=post('/move',{'game':g['game'],'move':uci(root(ms))})
