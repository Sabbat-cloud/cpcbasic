3000 REM subrutina de clasificacion
3010 FOR k=1 TO npts
3020 FOR j=1 TO npts
3030 zz=zp(k)
3040 yy=yp(k)
3050 xx=xp(k)
3060 sn=ss(k):REM almacenamiento de los valores temporales
3065 sm=si(k)
3070 IF zp(j)<=zp(k) THEN 3110
3080 zp(k)=zp(j):zp(j)=zz
3090 yp(k)=yp(j):yp(j)=yy
3100 xp(k)=xp(j):xp(j)=xx
3105 ss(k)=ss(j):ss(j)=sn
3107 si(k)=si(j):si(j)=sm
3110 NEXT j
3120 NEXT k
3130 RETURN
