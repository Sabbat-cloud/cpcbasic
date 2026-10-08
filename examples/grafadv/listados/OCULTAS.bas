5 REM****PROGRAMA OCULTAS****
10 REM Utilice PP=1000 para probar
20 MODE 1:INK 0,13:INK 1,1:INK 2,3:CLS
30 pp=1000
40 DIM x(40),y(40),z(40),ln(2,60),a(4,4),fa(12,40),nl(40),ls(40)
50 DIM xp(40),yp(40),zp(40)
60 REM Toma los datos para dibujar la superficie
70 INPUT"NOMBRE DEL FICHERO";h$:OPENIN h$
80 INPUT #9,npts
90 FOR i=1 TO npts
100 INPUT #9,x(i)
110 INPUT #9,y(i)
120 INPUT #9,z(i)
130 xp(i)=x(i):yp(i)=y(i)
140 NEXT i
150 INPUT #9,li
160 FOR i=1 TO li
170 INPUT #9,ln(1,i),ln(2,i)
180 NEXT i
190 INPUT #9,nf
200 FOR i=1 TO nf
210 FOR j=1 TO 12
220 INPUT #9,fa(j,i)
230 NEXT j
240 NEXT i
250 FOR i=1 TO nf
260 INPUT #9,nl(i)
270 NEXT i
280 CLOSEIN
300 REM Toma el eje de giro
310 INPUT"Eje de giro? X=1, Y=2, Z=3";m
320 theta=0
330 GOSUB 540:REM Ajuste completo de la rotacion - solo la primera vez
340 REM Comienzo del bucle de giro principal
350 k$=INKEY$:IF k$="S" OR k$="s" THEN CLS:GOTO 300:REM Aborta esta rotacion
360 REM Ahora dibuja el objeto
370 REM Las coordenadas son respecto al origen, con traslacion al centro
380 CLS
390 GOSUB 700
400 REM Giro de 10 grados
410 theta=theta+0.174533
420 a(m1,m2)=SIN(theta)
430 a(m1,m1)=COS(theta):a(m2,m2)=COS(theta):a(m2,m1)=-SIN(theta)
440 REM Calculo de la proyeccion en el plano X,Y
450 FOR i=1 TO npts
460 xt=a(1,1)*x(i)+a(1,2)*y(i)+a(1,3)*z(i)+a(1,4)
470 yt=a(2,1)*x(i)+a(2,2)*y(i)+a(2,3)*z(i)+a(2,4)
480 zt=a(3,1)*x(i)+a(3,2)*y(i)+a(3,3)*z(i)+a(3,4)
490 dd=zt+pp:xp(i)=xt*pp/dd:yp(i)=yt*pp/dd:zp(i)=zt
500 NEXT i
510 GOSUB 780:REM Rutina de lineas ocultas
520 REM Fin del bucle principal
530 GOTO 340
540 REM Subrutina de giro
550 c=COS(theta)
560 s=SIN(theta)
570 FOR k=1 TO 4
580 FOR l=1 TO 4
590 a(k,l)=0
600 NEXT l
610 NEXT k
620 REM Ahora calcula las inserciones adecuadas en la matriz
630 REM Vea la teoria en el Apendice!
640 a(4,4)=1
650 a(m,m)=1
660 m1=3-m:IF m1=0 THEN m1=1
670 m2=3:IF m=3 THEN m2=2
680 a(m1,m1)=c:a(m2,m2)=c:a(m2,m1)=-s:a(m1,m2)=s
690 RETURN
700 REM Dibujo de los ejes
710 MOVE 310,300
720 DRAW 310,190,2,0
730 DRAW 400,190,2,0
740 LOCATE 20,6:PRINT"Y"
750 LOCATE 26,14:PRINT"X"
760 LOCATE 20,14:PRINT"Z"
770 RETURN
780 REM Subrutina OCULTAS
790 ic=0:c=0:REM Inicializacion de los contadores
800 REM Toma de puntos del plano
810 FOR ih=1 TO nf
820 i1=fa(1,ih):i2=fa(2,ih)
830 i5=ln(1,i1):i6=ln(2,i1):i7=ln(1,i2)
840 IF (i5=i7) OR (i6=i7) THEN i7=ln(2,i2)
850 REM Calculo de la posicion del plano
860 x5=xp(i5)-xp(i6):y5=yp(i5)-yp(i6):z5=zp(i5)-zp(i6)
870 x6=xp(i7)-xp(i6):y6=yp(i7)-yp(i6):z6=zp(i7)-zp(i6)
880 a9=y5*z6-y6*z5
890 b9=z5*x6-z6*x5
900 c9=x5*y6-x6*y5
910 d9=a9*xp(i5)+b9*yp(i5)+c9*zp(i5)
920 REM Estan el observador y el origen en distintos lados del plano?
925 IF d9=0 THEN f9=0:GOTO 940:REM Previene la division por cero
930 f9=(1+c9*pp)/d9
940 IF f9>=0 THEN 1010
950 c=c+1
960 ix=nl(ih)
970 FOR jh=1 TO ix
980 ic=ic+1
990 ls(ic)=fa(jh,ih)
1000 NEXT jh
1010 NEXT ih
1020 REM Ordenamiento de la lista
1030 FOR ih=1 TO ic-1
1040 ii=ih+1
1050 l1=ls(ih)
1060 FOR jh=ii TO ic
1070 IF l1<=ls(jh) THEN 1110
1080 l1=ls(jh)
1090 ls(jh)=ls(ih)
1100 ls(ih)=l1
1110 NEXT jh
1120 NEXT ih
1130 REM Seguimiento de las duplicaciones de la lista
1140 jh=1
1150 FOR ih=2 TO ic
1160 IF ls(ih)=ls(jh) THEN 1190
1170 jh=jh+1
1180 ls(jh)=ls(ih)
1190 NEXT ih
1200 ic=jh
1210 in=1
1220 lq=ls(1)
1230 REM Ahora dibuja la figura utilizando solo las lineas de la lista
1240 FOR ih=1 TO li
1250 i2=ln(2,ih)
1260 i1=ln(1,ih)
1270 IF ih<>lq OR in>ic THEN 1320
1280 MOVE xp(i1)+320,yp(i1)+200
1290 DRAW xp(i2)+320,yp(i2)+200,1,0
1300 in=in+1
1310 lq=ls(in)
1320 NEXT ih
1330 FOR i=1 TO 1000:NEXT i
1340 RETURN
