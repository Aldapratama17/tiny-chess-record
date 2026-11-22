import json,os,time
import urllib.request as ureq
M=100000;I=1000000
V=(0,100,320,330,500,900,0)
N=(31,33,14,18,-31,-33,-14,-18)
K=(15,17,-15,-17)
S=(1,-1,16,-16)
KS=K+S
C={4:((6,(5,6),7,1),(2,(3,2,1),0,2)),116:((118,(117,118),119,4),(114,(115,114,113),112,8))}
P=(
0,0,0,0,0,0,0,0,
50,50,50,50,50,50,50,50,
10,10,20,30,30,20,10,10,
5,5,10,25,25,10,5,5,
0,0,0,20,20,0,0,0,
5,-5,-10,0,0,-10,-5,5,
5,10,10,-20,-20,10,10,5,
0,0,0,0,0,0,0,0)
Nt=(
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,0,0,0,0,-20,-40,
-30,0,10,15,15,10,0,-30,
-30,5,15,20,20,15,5,-30,
-30,0,15,20,20,15,0,-30,
-30,5,10,15,15,10,5,-30,
-40,-20,0,5,5,0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50)
B=(
-20,-10,-10,-10,-10,-10,-10,-20,
-10,0,0,0,0,0,0,-10,
-10,0,5,10,10,5,0,-10,
-10,5,5,10,10,5,5,-10,
-10,0,10,10,10,10,0,-10,
-10,10,10,10,10,10,10,-10,
-10,5,0,0,0,0,5,-10,
-20,-10,-10,-10,-10,-10,-10,-20)
Q=(
0,0,0,0,0,0,0,0,
5,10,10,10,10,10,10,5,
-5,0,0,0,0,0,0,-5,
-5,0,0,0,0,0,0,-5,
-5,0,0,0,0,0,0,-5,
-5,0,0,0,0,0,0,-5,
-5,0,0,0,0,0,0,-5,
0,0,0,5,5,0,0,0)
Kg=(
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
20,20,0,0,0,0,20,20,
20,30,10,0,0,10,30,20)
PS=(None,P,Nt,B,Q,P,Kg)
SQ=[((7-(i>>4))*8+(i&7))for i in range(128)]
Z=20261122
def R(s):return(s*6364136223846793005+1442695040888963407)%18446744073709551616
ZP=[[0]*128 for _ in range(13)]
for p in range(13):
 for s in range(128):Z=R(Z);ZP[p][s]=Z
ZS=R(Z)
ZC=[0]*16
for i in range(16):Z=R(Z);ZC[i]=Z
ZE=R(Z)^(R(Z)<<13)
class B:
 def __init__(s):
  s.b=[0]*128;s.c=1;s.p=0;s.C=0;s.E=-1;s.K=[0,0];s.h=0
 def F(s,f):
  p=f.split();s.b=[0]*128;r=7;fl=0
  for ch in p[0]:
   if ch=="/":r-=1;fl=0
   elif ch.isdigit():fl+=int(ch)
   else:
    sq=r*16+fl;pt="PNBRQK".index(ch.upper())+1;pc=pt if ch.isupper()else-pt
    s.b[sq]=pc
    if pt==6:s.K[0 if pc>0 else 1]=sq
    fl+=1
  s.c=1 if p[1]=="w"else-1;s.p=0;s.C=0
  for i,ch in enumerate("KQkq"):
   if ch in p[2]:s.C|=1<<i
  s.E=-1
  if len(p)>3 and p[3]!="-":s.E=(int(p[3][1])-1)*16+ord(p[3][0])-97
  h=0
  for sq in range(128):
   if not sq&8 and s.b[sq]:h^=ZP[s.b[sq]+6][sq]
  if s.c==1:h^=ZS
  h^=ZC[s.C]
  if s.E>=0:h^=ZE
  s.h=h
def A(b,k,c):
 j=b.b
 if c==1:
  for d in(-15,-17):
   t=k+d
   if not t&136 and j[t]==1:return 1
 else:
  for d in(15,17):
   t=k+d
   if not t&136 and j[t]==-1:return 1
 for d in N:
  t=k+d
  if not t&136 and j[t]==2*c:return 1
 for d in KS:
  t=k+d
  if not t&136 and j[t]==6*c:return 1
 for d in K:
  t=k+d
  while not t&136:
   p=j[t]
   if p:
    if p==3*c or p==5*c:return 1
    break
   t+=d
 for d in S:
  t=k+d
  while not t&136:
   p=j[t]
   if p:
    if p==4*c or p==5*c:return 1
    break
   t+=d
 return 0
def G(b,q=0):
 c=b.c;j=b.b;m=[]
 for sq in range(128):
  if sq&8:continue
  p=j[sq]
  if p*c<=0:continue
  pt=p*c
  if pt==1:
   f=16*c;pr=7 if c==1 else 0
   for d in(f-1,f+1):
    t=sq+d
    if t&136:continue
    if j[t]*c<0 or t==b.E:
     if t>>4==pr:
      for pm in(5,2,4,3):m.append((sq,t,pm,0))
     else:m.append((sq,t,0,0))
   if not q:
    t=sq+f
    if not t&136 and not j[t]:
     if t>>4==pr:
      for pm in(5,2,4,3):m.append((sq,t,pm,0))
     else:
      m.append((sq,t,0,0))
      if sq>>4==(1 if c==1 else 6)and not j[t+f]:m.append((sq,t+f,0,2))
  elif pt==6:
   for d in KS:
    t=sq+d
    if t&136:continue
    if j[t]*c<=0:m.append((sq,t,0,0))
   if not q and sq in C:
    for kt,pa,rt,rm in C[sq]:
     if b.C&rm and j[rt]==4*c and not any(j[x]for x in pa)and not any(A(b,x,-c)for x in pa+(sq,)):
      m.append((sq,kt,0,1))
  else:
   dD=N if pt==2 else(K if pt==3 else(S if pt==4 else KS))
   for d in dD:
    t=sq+d
    while not t&136:
     tp=j[t]
     if tp*c>0:break
     if not q or tp:m.append((sq,t,0,0))
     if tp or pt==2:break
     t+=d
 return m
def Mv(b,m):
 f,t,pm,fl=m;j=b.b;pc=j[f];c=b.c
 u=(j[t],t,b.C,b.E,b.h)
 h=b.h^ZP[pc+6][f]
 # En passant capture
 if abs(pc)==1 and t==b.E and (t&15)!=(f&15):
  cv=t-16*c
  h^=ZP[j[cv]+6][cv]
  j[cv]=0
 elif j[t]:
  h^=ZP[j[t]+6][t];j[t]=0
 mp=pm*c if pm else pc
 j[t]=mp;j[f]=0
 h^=ZP[mp+6][t]
 if mp==6:b.K[0]=t
 elif mp==-6:b.K[1]=t
 b.E=(f+t)//2 if abs(pc)==1 and abs(t-f)==32 else-1
 if b.E>=0:h^=ZE
 if abs(pc)==6 and fl==1:
  if t==f+2:
   r=j[f+3];j[f+1]=r;j[f+3]=0;h^=ZP[r+6][f+3]^ZP[r+6][f+1]
  else:
   r=j[f-4];j[f-1]=r;j[f-4]=0;h^=ZP[r+6][f-4]^ZP[r+6][f-1]
 b.c=-b.c;h^=ZS
 oc=b.C
 if pc==6:b.C&=~3
 elif pc==-6:b.C&=~12
 if f==7 or t==7:b.C&=~1
 if f==0 or t==0:b.C&=~2
 if f==119 or t==119:b.C&=~4
 if f==112 or t==112:b.C&=~8
 if b.C!=oc:h^=ZC[oc]^ZC[b.C]
 b.h=h
 return u
def U(b,m,u):
 f,t,pm,fl=m;cp,cs,oc,oe,oh=u;j=b.b;pc=j[t];c=b.c
 b.C=oc;b.E=oe;b.h=oh;b.c=-b.c
 j[f]=pc;j[t]=0
 if cp:j[cs]=cp
 # En passant capture
 if abs(pc)==1 and cs==oe and (cs&15)!=(f&15):
  cv=cs+16*c
  j[cv]=-pc
 if abs(pc)==6 and fl==1:
  if t==f+2:j[f+3]=j[f+1];j[f+1]=0
  else:j[f-4]=j[f-1];j[f-1]=0
 if pc==6:b.K[0]=f
 elif pc==-6:b.K[1]=f
def E(b):
 s=0;j=b.b
 for sq in range(128):
  if sq&8:continue
  p=j[sq]
  if not p:continue
  pt=abs(p);ix=SQ[sq]
  if p>0:s+=V[pt]+PS[pt][ix]
  else:s-=V[pt]+PS[pt][ix]
 return s*b.c
n=[0];dl=[0];TT={}
def Q(b,a,b_):
 n[0]+=1
 if n[0]&1023==0 and time.time()>dl[0]:raise TimeoutError
 s=E(b)
 if s>=b_:return s
 if s>a:a=s
 c=b.c;k=b.K[0]if c==1 else b.K[1]
 m=G(b,1);m.sort(key=lambda x:-(abs(b.b[x[1]])or 1))
 for mv in m:
  u=Mv(b,mv)
  nk=b.K[0]if b.c==-1 else b.K[1]
  if A(b,nk,b.c):U(b,mv,u);continue
  sc=-Q(b,-b_,-a)
  U(b,mv,u)
  if sc>=b_:return sc
  if sc>a:a=sc
 return a
def Srch(b,d,pl,a,b_):
 n[0]+=1
 if n[0]&1023==0 and time.time()>dl[0]:raise TimeoutError
 h=b.h
 if pl and h in TT:
  th,td,tf,ts,tm=TT[h]
  if td>=d:
   if tf==0:return ts
   if tf==1 and ts>=b_:return ts
   if tf==2 and ts<=a:return ts
 c=b.c;k=b.K[0]if c==1 else b.K[1]
 chk=A(b,k,-c)
 if d<=0:return Q(b,a,b_)
 m=G(b)
 o=[]
 for mv in m:
  sc=0
  if h in TT and TT[h][4]==mv:sc=1<<30
  elif b.b[mv[1]]:sc=I+100*abs(b.b[mv[1]])-abs(b.b[mv[0]])
  o.append((sc,mv))
 o.sort(key=lambda x:-x[0])
 bm=None;bs=-I;mc=0
 for _,mv in o:
  u=Mv(b,mv)
  nk=b.K[0]if b.c==-1 else b.K[1]
  if A(b,nk,b.c):U(b,mv,u);continue
  mc+=1
  sc=-Srch(b,d-1,pl+1,-b_,-a)
  U(b,mv,u)
  if sc>bs:bs=sc;bm=mv
  if sc>a:a=sc
  if a>=b_:break
 if not mc:return-M+pl if chk else 0
 if bs>=b_:tf=1
 elif bs<=a:tf=2
 else:tf=0
 TT[h]=(h,d,tf,bs,bm)
 return bs
def D(f,tl=3000):
 global TT
 TT={};n[0]=0;dl[0]=time.time()+tl/1e3
 b=B();b.F(f)
 m=G(b);l=[]
 c=b.c
 for mv in m:
  u=Mv(b,mv)
  k=b.K[0]if b.c==-1 else b.K[1]
  if not A(b,k,b.c):l.append(mv)
  U(b,mv,u)
 if not l:return None
 bm=l[0]
 for d in range(1,64):
  try:
   a=-I;b_=-I;bt=None
   o=[]
   for mv in l:
    sc=0
    if b.h in TT and TT[b.h][4]==mv:sc=1<<30
    elif b.b[mv[1]]:sc=I+100*abs(b.b[mv[1]])-abs(b.b[mv[0]])
    o.append((sc,mv))
   o.sort(key=lambda x:-x[0])
   for _,mv in o:
    u=Mv(b,mv)
    k=b.K[0]if b.c==-1 else b.K[1]
    if A(b,k,b.c):U(b,mv,u);continue
    sc=-Srch(b,d-1,1,-I,-a)
    U(b,mv,u)
    if sc>a:a=sc;bt=mv
   if bt:bm=bt
   if a>99000:break
  except TimeoutError:break
 return bm
def U2(sq):return chr(97+(sq&15))+str((sq>>4)+1)
def U3(m):
 f,t,pm,_=m;u=U2(f)+U2(t)
 if pm:u+=" nbrq"[pm-1]if pm in(2,3,4,5)else""
 return u
def run():
 u=os.environ["MAKEFUN_ENV_URL"];g=None;w=d=l=0
 while 1:
  r=json.loads(ureq.urlopen(ureq.Request(u+"/game",data=b"{}",headers={"Content-Type":"application/json"},method="POST"),timeout=8).read().decode())
  st=r.get("status");o=r.get("outcome")
  if st=="done"or o:
   if o=="win":w+=1
   elif o=="loss":l+=1
   else:d+=1
   if"wins"in r:w=r["wins"];d=r["draws"];l=r["losses"]
   r=json.loads(ureq.urlopen(ureq.Request(u+"/game",data=b"{}",headers={"Content-Type":"application/json"},method="POST"),timeout=8).read().decode())
   if r.get("status")=="done"or r.get("outcome"):break
   continue
  if st!="your_move":break
  g=r.get("game",g);f=r["fen"]
  try:
   mv=D(f,3000)
   if mv is None:raise RuntimeError
   um=U3(mv)
  except:um=r.get("legal_moves",[0])[0]
  try:
   r=json.loads(ureq.urlopen(ureq.Request(u+"/move",data=json.dumps({"game":g,"move":um}).encode(),headers={"Content-Type":"application/json"},method="POST"),timeout=8).read().decode())
  except:break
if __name__=="__main__":run()
