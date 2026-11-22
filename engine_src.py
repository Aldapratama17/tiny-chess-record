import json,os,time
import urllib.request as ureq
b3=100000
bf=1000000
bj=(0,100,320,330,500,900,0)
b4=[31,33,14,18,-31,-33,-14,-18]
b1=[15,17,-15,-17]
b5=[1,-1,16,-16]
b2=b1+b5
aj={4:((6,(5,6),7,1),(2,(3,2,1),0,2)),116:((118,(117,118),119,4),(114,(115,114,113),112,8))}
cp=(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0)
co=(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50)
cm=(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20)
cq=(0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0)
cn=(-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20)
bh=(None,cp,co,cm,cq,cp,cn)
bg=[((7-(ae>>4))*8+(ae&7))for ae in range(128)]
b0=20261122
an=[[(b0:=(b0*6364136223846793005+1442695040888963407)%(1<<64))for a in range(128)]for a in range(13)]
ao=(b0:=(b0*6364136223846793005+1442695040888963407)%(1<<64))
al=[(b0:=(b0*6364136223846793005+1442695040888963407)%(1<<64))for a in range(16)]
am=b0^b0<<13
class bi:
    def __init__(cg):
        cg.j=[0]*128
        cg.ci=1
        cg.at=0
        cg.ax=-1
        cg.a2=0
        cg.a0=0
        cg.hash=0
    def do(cg,bm):
        ab=bm.split()
        cg.j=[0]*128
        ad=7
        o=0
        for ar in ab[0]:
            if ar=="/":
                ad-=1
                o=0
            elif ar.isdigit():
                o+=int(ar)
            else:
                ae=ad*16+o
                ba="PNBRQK".index(ar.upper())+1
                ah=ba if ar.isupper() else -ba
                cg.j[ae]=ah
                if ba==6:
                    if ah>0:cg.a2=ae
                    else:cg.a0=ae
                o+=1
        cg.ci=1 if ab[1]=="w" else -1
        cg.at=0
        au=ab[2]
        cg.at=sum(1<<z for z,k in enumerate("KQkq")if k in au)
        cg.ax=-1
        if len(ab)>3 and ab[3]!="-":
            cg.ax=(int(ab[3][1])-1)*16+(ord(ab[3][0])-97)
        y=0
        for ae in range(128):
            if not ae&8 and cg.j[ae]:
                y^=an[cg.j[ae]+6][ae]
        y^=ao if cg.ci==1 else 0
        y^=al[cg.at]
        if cg.ax>=0:y^=am
        cg.hash=y
def ds(a8,ae,aq):
    j=a8.j
    if aq==1:
        for l in(-15,-17):
            af=ae+l
            if not af&136 and j[af]==1:return True
    else:
        for l in(15,17):
            af=ae+l
            if not af&136 and j[af]==-1:return True
    for l in b4:
        af=ae+l
        if not af&136 and j[af]==2*aq:return True
    for l in b2:
        af=ae+l
        if not af&136 and j[af]==6*aq:return True
    for l in b1:
        af=ae+l
        while not af&136:
            ah=j[af]
            if ah:
                if ah==3*aq or ah==5*aq:return True
                break
            af+=l
    for l in b5:
        af=ae+l
        while not af&136:
            ah=j[af]
            if ah:
                if ah==4*aq or ah==5*aq:return True
                break
            af+=l
    return False
def dz(a8,dy=False):
    ci=a8.ci
    j=a8.j
    a5=[]
    for ae in range(128):
        if ae&8:continue
        ah=j[ae]
        if ah*ci<=0:continue
        ba=ah*ci
        if ba==1:
            l=16*ci
            ad=ae>>4
            dm=7 if ci==1 else 0
            for av in(l-1,l+1):
                af=ae+av
                if af&136:continue
                if j[af]*ci<0 or af==a8.ax:
                    if (af>>4)==dm:
                        for a9 in(5,2,4,3):a5.append((ae,af,a9,0))
                    else:a5.append((ae,af,0,0))
            if not dy:
                af=ae+l
                if not af&136 and not j[af]:
                    if (af>>4)==dm:
                        for a9 in(5,2,4,3):a5.append((ae,af,a9,0))
                    else:
                        a5.append((ae,af,0,0))
                        if ad==(1 if ci==1 else 6) and not j[af+l]:
                            a5.append((ae,af+l,0,2))
        elif ba==6:
            for l in b2:
                af=ae+l
                if af&136:continue
                if j[af]*ci<=0:a5.append((ae,af,0,0))
            if not dy and ae in(4,116):
                for az,aw,bb,ap in aj[ae]:
                    if a8.at&ap and j[bb]==4*ci and not any(j[ai]for ai in aw)and not any(ds(a8,ai,-ci)for ai in aw+(ae,)):
                        a5.append((ae,az,0,1))
        else:
            cd=b4 if ba==2 else(b1 if ba==3 else(b5 if ba==4 else b2))
            for l in cd:
                af=ae+l
                while not af&136:
                    ag=j[af]
                    if ag*ci>0:break
                    if not dy or ag:a5.append((ae,af,0,0))
                    if ag or ba==2:break
                    af+=l
    return a5
def cc(a8,aa):
    ay,be,c3,b9=aa
    j=a8.j
    ah=j[ay]
    bk=j[be]
    cv=be
    if not bk and abs(ah)==1 and be==a8.ax and(be&15)!=(ay&15):
        cv=be-16*a8.ci
        bk=j[cv]
    ck=(bk,cv,a8.at,a8.ax,a8.hash)
    y=a8.hash^an[ah+6][ay]
    if bk:
        y^=an[bk+6][cv]
        j[cv]=0
    a6=c3*a8.ci if c3 else ah
    j[be]=a6
    j[ay]=0
    y^=an[a6+6][be]
    if a6==6:a8.a2=be
    elif a6==-6:a8.a0=be
    a8.ax=(ay+be)//2 if(abs(ah)==1 and abs(be-ay)==32)else-1
    if a8.ax>=0:y^=am
    if abs(ah)==6 and b9==1:
        if be==ay+2:
            bb=j[ay+3]
            j[ay+1]=bb
            j[ay+3]=0
            y^=an[bb+6][ay+3]^an[bb+6][ay+1]
        else:
            bb=j[ay-4]
            j[ay-1]=bb
            j[ay-4]=0
            y^=an[bb+6][ay-4]^an[bb+6][ay-1]
    a8.ci=-a8.ci
    y^=ao
    c2=a8.at
    if ah==6:c2&=~3
    elif ah==-6:c2&=~12
    if ay==7 or be==7:c2&=~1
    if ay==0 or be==0:c2&=~2
    if ay==119 or be==119:c2&=~4
    if ay==112 or be==112:c2&=~8
    if c2!=a8.at:
        y^=al[a8.at]^al[c2]
        a8.at=c2
    a8.hash=y
    return ck
def dh(a8,aa,ck):
    ay,be,c3,b9=aa
    bk,cv,a8.at,a8.ax,a8.hash=ck
    a8.ci=-a8.ci
    j=a8.j
    ah=a8.ci if c3 else j[be]
    j[ay]=ah
    j[be]=0
    if bk:j[cv]=bk
    if ah==6:a8.a2=ay
    elif ah==-6:a8.a0=ay
    if b9==1:
        if be==ay+2:
            j[ay+3]=j[ay+1]
            j[ay+1]=0
        else:
            j[ay-4]=j[ay-1]
            j[ay-1]=0
def du(a8):
    bc=0
    j=a8.j
    for ae in range(128):
        if ae&8:continue
        ah=j[ae]
        if not ah:continue
        ab=abs(ah)
        if ah>0:
            bc+=bj[ab]+bh[ab][56-8*(ae>>4)+(ae&15)]
        else:
            bc-=bj[ab]+bh[ab][(ae>>4)*8+(ae&15)]
    # Pawn structure eval
    for c in(1,-1):
        mult=1 if c==1 else -1
        # Doubled pawns
        for f in range(8):
            cnt=0
            for r in range(8):
                sq=r*16+f
                if j[sq]==c:cnt+=1
            if cnt>1:bc-=mult*15*(cnt-1)
        # Passed pawns
        for r in range(8):
            for f in range(8):
                sq=r*16+f
                if j[sq]==c:
                    passed=True
                    for df in(-1,0,1):
                        nf=f+df
                        if 0<=nf<8:
                            for nr in range(r+1,8)if c==1 else range(r-1,-1,-1):
                                ns=nr*16+nf
                                if j[ns]==-c:passed=False;break
                            if not passed:break
                    if passed:bc+=mult*20*(7-r if c==1 else r)
        # King safety - pawn shield
        ks=a8.a2 if c==1 else a8.a0
        kr,ksf=ks>>4,ks&15
        shield=0
        for df in(-1,0,1):
            nf=ksf+df
            if 0<=nf<8:
                for dr in(-1,0,1)if c==1 else(1,0,-1):
                    nr=kr+dr
                    if 0<=nr<8:
                        ns=nr*16+nf
                        if j[ns]==c:shield+=1
        if shield<3:bc-=mult*30*(3-shield)
    # Mobility (cheap)
    oci=a8.ci
    a8.ci=1
    wm=len(dz(a8,True))
    a8.ci=-1
    bm=len(dz(a8,True))
    a8.ci=oci
    bc+=(wm-bm)//4
    return bc*a8.ci
cl=[0]
dr=[0]
ak={}
def dn(a8,ct,b7):
    cl[0]+=1
    if cl[0]&1023==0 and time.time()>dr[0]:raise TimeoutError
    c5=du(a8)
    if c5>=b7:return c5
    if c5>ct:ct=c5
    b8=dz(a8,True)
    b8.sort(key=lambda aa:-(abs(a8.j[aa[1]])or 1))
    for aa in b8:
        ck=cc(a8,aa)
        bo=a8.a2 if a8.ci==1 else a8.a0
        if ds(a8,bo,a8.ci):
            dh(a8,aa,ck)
            continue
        bc=-dn(a8,-b7,-ct)
        dh(a8,aa,ck)
        if bc>=b7:return bc
        if bc>ct:ct=bc
    return ct
def df(a8,cw,bq,ct,b7):
    cl[0]+=1
    if cl[0]&1023==0 and time.time()>dr[0]:raise TimeoutError
    y=a8.hash
    if bq and y in ak:
        bw,dg,c6,bv,bu=ak[y]
        if dg>=cw:
            if c6==0:return bv
            if c6==1 and bv>=b7:return bv
            if c6==2 and bv<=ct:return bv
    bl=ds(a8,a8.a2 if a8.ci==1 else a8.a0,-a8.ci)
    if cw<=0:return dn(a8,ct,b7)
    b6=-bf
    cu=None
    a5=dz(a8)
    de=[]
    for aa in a5:
        bs=0
        if y in ak and ak[y][4]==aa:bs=1<<30
        elif a8.j[aa[1]]:
            bs=1000000+100*abs(a8.j[aa[1]])-abs(a8.j[aa[0]])
        else:bs=0
        de.append((bs,aa))
    de.sort(key=lambda ai:-ai[0])
    c0=0
    for a,aa in de:
        ck=cc(a8,aa)
        bo=a8.a2 if a8.ci==1 else a8.a0
        if ds(a8,bo,a8.ci):
            dh(a8,aa,ck)
            continue
        c0+=1
        # LMR
        rd=1 if c0>4 and cw>=3 and not a8.j[aa[1]] and aa[2]==0 and aa[3]!=1 else 0
        bc=-df(a8,cw-1-rd,bq+1,-b7,-ct)
        if rd and bc>ct:
            bc=-df(a8,cw-1,bq+1,-b7,-ct)
        dh(a8,aa,ck)
        if bc>b6:b6=bc;cu=aa
        if bc>ct:ct=bc
        if ct>=b7:break
    if not c0:return -b3+bq if bl else 0
    ak[y]=(y,cw,1 if b6>=b7 else(2 if b6<=ct else 0),b6,cu)
    return b6
def d0(a8,dc=3500):
    global ak
    ak={}
    cl[0]=0
    dr[0]=time.time()+dc/1e3
    a5=dz(a8)
    de=[]
    for aa in a5:
        ck=cc(a8,aa)
        bo=a8.a2 if a8.ci==-1 else a8.a0
        bt=not ds(a8,bo,a8.ci)
        dh(a8,aa,ck)
        if bt:de.append(aa)
    if not de:return None
    cu=de[0]
    for cw in range(1,64):
        dt=None
        c9=-bf
        ct=-bf
        try:
            for aa in de:
                ck=cc(a8,aa)
                bc=-df(a8,cw-1,1,-bf,-ct)
                dh(a8,aa,ck)
                if bc>c9:c9=bc;dt=aa
                if bc>ct:ct=bc
            cu=dt
            if c9>99000:break
        except TimeoutError:break
    return cu
def dp(ae):return chr(97+(ae&15))+str((ae>>4)+1)
def dv(aa):
    ay,be,c3,a=aa
    ag=dp(ay)+dp(be)
    if c3:ag+="nbrq"[c3-1]if c3 in(2,3,4,5)else""
    return ag
def dx(bm,a4=3500):
    a8=bi()
    a8.do(bm)
    aa=d0(a8,a4)
    return aa
def dw(bx,ce,bp):
    ac=json.dumps(bp).encode()
    br=ureq.Request(bx+ce,data=ac,headers={"Content-Type":"application/json"},method="POST")
    return json.loads(ureq.urlopen(br,timeout=8).read().decode())
def cb():
    bx=os.environ["MAKEFUN_ENV_URL"]
    w=None
    bz=cx=ca=0
    ad=dw(bx,"/game",{})
    while True:
        bd=ad.get("status")
        if bd=="done"or ad.get("outcome"):
            a7=ad.get("outcome")
            if a7=="win":bz+=1
            elif a7=="loss":ca+=1
            else:cx+=1
            if"wins"in ad:bz=ad["wins"];cx=ad["draws"];ca=ad["losses"]
            ad=dw(bx,"/game",{})
            if ad.get("status")=="done"or ad.get("outcome"):break
            continue
        if bd!="your_move":break
        w=ad.get("game",w)
        bm=ad["fen"]
        a5=None
        try:
            aa=dx(bm,3500)
            if aa is None:raise RuntimeError("no moves")
            a5=dv(aa)
        except Exception as n:
            a3=ad.get("legal_moves")
            if a3:a5=a3[0]
            else:break
        try:
            ad=dw(bx,"/move",{"game":w,"move":a5})
        except Exception as n:break
if __name__=="__main__":cb()
