10 REM ****MOL3D - PROGRAMA MOLECULA 3D****
15 REM Utiliza ENTRADAMOL para tomar datos de entrada
20 REM Representa las moleculas como circulos rellenos
30 REM REPRESENTACION DE SUPERFICIES OCULTAS
40 INK 0,13:INK 1,1:MODE 1
45 INK 2,3:INK 3,9
50 pp=1000:sc=2:REM seleccion de escala y distancia al observador
60 INPUT"Impresion del resultado? (S o N)";p$:pt=0
70 IF p$="s" OR p$="S" THEN pt=1
80 DIM x(100),y(100),z(100),si(100),a(4,4),ss(100),xp(100),yp(100),zp(100)
90 lx=1000:hx=0:ly=1000:hy=0:lz=1000:hz=0:sz=0:REM inicializa variables
100 INPUT "NOMBRE DE FICHERO";n$
110 OPENIN n$
112 INPUT #9,h$:REM nombre de la molecula
115 INPUT #9,npts
117 PRINT"hay",npts,"atomos"
120 FOR i=1 TO npts
130 INPUT #9,x(i),y(i),z(i),si(i)
135 IF z(i)=0 THEN z(i)=1
140 GOSUB 4000:
150 NEXT i
160 CLOSEIN
170 GOSUB 4100:REM escala
180 REM toma el eje de giro
190 INPUT "Indique el eje de giro: x=1,y=2,z=3";m: IF m<1 OR m>3 THEN m=1
200 INPUT "Angulo de rotacion";theta
210 INPUT "Rellenado";p$:ps=0
220 IF p$="S"OR p$="s" THEN ps=1
240 FOR i=1 TO npts
250 xp(i)=x(i)
260 yp(i)=y(i)
270 zp(i)=z(i)
280 ss(i)=si(i)
290 NEXT i
300 REM realiza la rotacion
310 theta =theta * 0.017455
320 GOSUB 1000:REM subrutina de giro
330 lx=1000:hx=0:ly=1000:hy=0:lz=1000:hz=0:sz=0:REM reinicializacion de variables
340 REM calculo de la proyeccion sobre el plano x,y
350 FOR i=1 TO npts
360 x4=x(i):REM x4-x8 son variables para calcular el radio del atomo proyectado
370 x5=x4+(si(i)/2)
380 x6=a(1,1)*x5+a(1,2)*y(i)+a(1,3)*z(i)+a(1,4)
390 xt=a(1,1)*x(i)+a(1,2)*y(i)+a(1,3)*z(i)+a(1,4)
400 yt=a(2,1)*x(i)+a(2,2)*y(i)+a(2,3)*z(i)+a(2,4)
410 zt=a(3,1)*x(i)+a(3,2)*y(i)+a(3,3)*z(i)+a(3,4)
420 dd=zt+pp
430 xp(i)=xt*pp/dd
440 yp(i)=yt*pp/dd
450 zp(i)=dd
460 x4=xp(i)
470 REM ajuste del diametro del atomo
480 x7=x6*pp/dd
490 IF x7<x4 THEN x8=x4-x7
500 IF x4<x7 THEN x8=x7-x4
510 ss(i)=(sc*x8)*2
520 IF ss(i)<0 THEN ss(i)=-ss(i)
530 GOSUB 5000:REM calcula el maximo y el minimo de los datos transformados
540 NEXT i
550 REM fin de la seccion de perspectiva
555 CLS:REM borra la pantalla
560 GOSUB 3000:REM clasifica segun la profundidad
562 IF m=1 THEN m$="X"
564 IF m=2 THEN m$="Y"
566 IF m=3 THEN m$="Z"
570 ga$=STR$(theta*(1/0.017455)):LOCATE 2,25:PRINT"angulo="+ga$+" Eje="+m$
580 GOSUB 5100:REM ajusta la escala de los datos transformados
590 REM preparado para dibujar
600 FOR i=1 TO npts
610 GOSUB 2000
620 NEXT i
630 k$=INKEY$:IF k$="" THEN 630
640 IF pt=1 THEN |copy
650 REM repetir para una vista diferente
660 GOTO 180
1000 REM subrutina de rotacion
1010 c=COS(theta)
1020 s=SIN(theta)
1030 FOR k=1 TO 4
1040 FOR l=1 TO 4
1050 a(k,l)=0
1060 NEXT l
1070 NEXT k
1080 a(4,4)=1
1090 a(m,m)=1
1100 m1=3-m:IF m1=0 THEN m1=1
1110 m2=3:IF m=3 THEN m2=2
1120 a(m1,m1)=c
1130 a(m2,m2)=c
1140 a(m2,m1)=-s
1150 a(m1,m2)=s
1160 RETURN
2000 REM **** RUTINA PARA DIBUJAR ATOMOS ****
2010 r=si(i):xl=xp(i):yl=yp(i):pd=1:flag=0
2012 LOCATE 1,1:PRINT h$
2020 IF r=50 THEN pd=2:REM Define el color de dibujo para el atomo de radio 15
2030 IF r=40 THEN pd=3:REM Define el color de dibujo para el atomo de radio 20
2035 IF r=25 THEN pd=1:REM Define el color de dibujo para el atomo de radio 25
2040 r=ss(i):REM ahora redefine el radio para el tamaño de la perspectiva
2050 ai=(2*PI)*(1/500)
2055 an=-ai
2130 x1=r*COS(an):y1=r*SIN(an):xs=x1:ys=y1
2160 FOR ik=1 TO 63
2180 an=an+ai
2190 x1=r*COS(an):y1=r*SIN(an)
2220 GOSUB 3500:REM simetria de octantes
2240 NEXT ik
2245 IF ps=0 THEN RETURN
2246 REM seccion de rellenado
2248 nn=500
2250 r=r-2
2260 x1=r*COS(an):y1=r*SIN(an)
2270 xs=x1:ys=y1
2280 x2=x1:y2=y1
2290 an=an+ai
2300 x1=r*COS(an):y1=r*SIN(an)
2310 IF TEST(x1+xl,y1+yl)>0 THEN GOTO 2350
2340 MOVE xl+x1,yl+y1
2345 FILL pd
2350 an=(ai*(nn/4))
2360 x1=r*COS(an):y1=r*SIN(an)
2370 IF TEST(x1+xl,y1+yl)>0 THEN GOTO 2410
2400 MOVE xl+x1,yl+y1
2405 FILL pd
2410 an=(ai*(nn/2))
2420 x1=r*COS(an):y1=r*SIN(an)
2430 IF TEST(x1+xl,y1+yl)>0 THEN GOTO 2470
2460 MOVE xl+x1,yl+y1
2465 FILL pd
2470 an=(ai*(nn*0.75))
2480 x1=r*COS(an):y1=r*SIN(an)
2490 IF TEST(x1+xl,y1+yl)>0 THEN GOTO 2540
2500 MOVE xl+x1,yl+y1
2520 FILL pd
2540 r=r+2:RETURN
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
3500 REM simetria de octantes para el circulo
3510 IF TEST(x1+xl,y1+yl)=0 THEN PLOT x1+xl,y1+yl,1,0
3520 IF TEST(y1+xl,x1+yl)=0 THEN PLOT y1+xl,x1+yl,1,0
3530 IF TEST(y1+xl,-x1+yl)=0 THEN PLOT y1+xl,-x1+yl,1,0
3540 IF TEST(x1+xl,-y1+yl)=0 THEN PLOT x1+xl,-y1+yl,1,0
3550 IF TEST(-x1+xl,-y1+yl)=0 THEN PLOT -x1+xl,-y1+yl,1,0
3560 IF TEST(-y1+xl,-x1+yl)=0 THEN PLOT -y1+xl,-x1+yl,1,0
3570 IF TEST(-y1+xl,x1+yl)=0 THEN PLOT -y1+xl,x1+yl,1,0
3580 IF TEST(-x1+xl,y1+yl)=0 THEN PLOT -x1+xl,y1+yl,1,0
3590 RETURN
4000 REM subrutina de determinacion del maximo y el minimo
4010 IF x(i)<lx THEN lx=x(i)
4020 IF x(i)>hx THEN hx=x(i)
4030 IF y(i)<ly THEN ly=y(i)
4040 IF y(i)>hy THEN hy=y(i)
4050 IF z(i)<lz THEN lz=z(i)
4060 IF z(i)>hz THEN hz=z(i)
4070 IF si(i)>sz THEN sz=si(i)
4080 RETURN
4100 REM subrutina de cambio de escala
4105 fa=hx-lx
4110 IF (hx-lx)>(hy-ly) THEN fa=hx-lx
4120 IF (hy-ly)>(hx-lx) THEN fa=hy-ly
4125 IF fa=0 THEN fa=1
4130 sz=sz*sc:zo=1000:zm=0
4140 FOR i=1 TO npts
4150 x(i)=(x(i)-lx+1)*((640-sz)/fa)
4155 x(i)=x(i)-320
4156 y(i)=(y(i)-ly+1)*((400-sz)/fa)
4157 y(i)=y(i)-200
4160 z(i)=(z(i)-lz+1)*((400-sz)/fa)
4170 IF z(i)<zo THEN zo=z(i)
4180 IF z(i)>zm THEN zm=z(i)
4190 NEXT i
4200 sz=sz/sc
4210 RETURN
5000 REM subrutina de maximo y minimo para xp, etc
5010 IF xp(i)<lx THEN lx=xp(i)
5020 IF xp(i)>hx THEN hx=xp(i)
5030 IF yp(i)<ly THEN ly=yp(i)
5040 IF yp(i)>hy THEN hy=yp(i)
5050 IF zp(i)<lz THEN lz=zp(i)
5060 IF zp(i)>hz THEN hz=zp(i)
5070 IF ss(i)>sz THEN sz=ss(i)
5080 RETURN
5100 REM subrutina de cambio de escala para xp, etc
5105 fa=hx-lx
5110 IF (hx-lx)>(hy-ly) THEN fa=hx-lx
5120 IF (hy-ly)>(hx-lx) THEN fa=hy-ly
5125 IF fa=0 THEN fa=1
5130 sz=sz*sc
5140 FOR i=1 TO npts
5150 xp(i)=(xp(i)-lx+1)*((600-sz)/fa)
5155 xp(i)=xp(i)+(sz/2)
5156 yp(i)=(yp(i)-ly+1)*((380-sz)/fa)
5157 yp(i)=yp(i)+(sz/2)
5160 zp(i)=(zp(i)-lz+1)*((380-sz)/fa)
5190 NEXT i
5200 sz=sz/sc
5210 RETURN
