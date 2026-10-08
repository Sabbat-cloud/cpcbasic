10 REM **** PROGRAMA TRASL3D****
20 REM Demostracion de un sencillo metodo de proyeccion 3D
30 DIM x(30),y(30),z(30),ln(2,50),a(4,4)
40 DIM xp(30),yp(30)
50 CLS
55 MODE 1:INK 0,13:INK 1,1:INK 2,3
60 REM Toma los datos para dibujar la casa
70 OPENIN "casa.DAT"
80 INPUT #9,npts
90 FOR i=1 TO npts
100 INPUT #9,x(i),y(i),z(i)
105 IF z(i)>0 THEN z(i)=z(i)-60
110 xp(i)=x(i)
120 yp(i)=y(i)
130 NEXT i
140 INPUT #9,li
150 FOR i=1 TO li
160 INPUT #9,ln(1,i),ln(2,i)
170 NEXT i
180 CLOSEIN
182 REM toma el eje de giro
183 INPUT"Eje de giro? - x=1, y=2, z=3";m
184 theta=0
222 GOSUB 400:REM Ajuste completo de la rotacion - solo la primera vez
225 REM Comienzo del bucle principal para la rotacion
227 k$=INKEY$:IF k$="S" OR k$="s" THEN CLS:GOTO 182:REM Abortar la rotacion
230 REM Ahora dibuja la casa
240 REM Las coordenadas son respecto al origen, con traslacion al centro
245 CLS
247 GOSUB 1000:REM Dibuja los ejes
250 FOR i=1 TO li
260 MOVE xp(ln(1,i))+320,yp(ln(1,i))+200
270 DRAW xp(ln(2,i))+320,yp(ln(2,i))+200,1,0
280 NEXT i
290 REM Giro de 10 grados
300 theta=theta+0.174533
310 a(m1,m2)=SIN(theta)
311 a(m1,m1)=COS(theta):a(m2,m2)=COS(theta):a(m2,m1)=-SIN(theta)
320 REM Calcula la proyeccion en el plano X,Y
330 FOR i=1 TO npts
340 xp(i)=a(1,1)*x(i)+a(1,2)*y(i)+a(1,3)*z(i)+a(1,4)
350 yp(i)=a(2,1)*x(i)+a(2,2)*y(i)+a(2,3)*z(i)+a(2,4)
360 NEXT i
370 REM Fin del bucle principal
380 GOTO 225
400 REM Subrutina de giro
410 c=COS(theta)
420 s=SIN(theta)
430 FOR k=1 TO 4
440 FOR l=1 TO 4
450 a(k,l)=0
460 NEXT l
470 NEXT k
475 REM Ahora calcula las inserciones adecuadas de la matriz
476 REM Vea la teoria en el Apendice!
480 a(4,4)=1
490 a(m,m)=1
500 m1=3-m:IF m1=0 THEN m1=1
510 m2=3:IF m=3 THEN m2=2
520 a(m1,m1)=c:a(m2,m2)=c:a(m2,m1)=-s:a(m1,m2)=s
530 RETURN
1000 REM Dibujo de los ejes
1010 MOVE 310,300
1020 DRAW 310,190,2,0
1030 DRAW 400,190,2,0
1032 LOCATE 20,6:PRINT"Y"
1034 LOCATE 26,14:PRINT"X"
1036 LOCATE 20,14:PRINT"Z"
1040 RETURN
1200 REM SUBRUTINA DE CAMBIO DE ESCALA
1210 A(1,1)=SX:A(1,2)=0:A(1,3)=0:A(1,4)=0
1220 A(2,1)=0:A(2,2)=SY:A(2,3)=0:A(2,4)=0
1230 A(3,1)=0:A(3,2)=0:A(3,3)=SZ:A(3,4)=0
1240 A(4,1)=0:A(4,2)=0:A(4,3)=0:A(4,4)=1
1250 RETURN
1300 REM SUBRUTINA DE TRASLACIONES
1310 A(1,1)=1:A(1,2)=0:A(1,3)=0:A(1,4)=TX
1320 A(2,1)=0:A(2,2)=1:A(2,3)=0:A(2,4)=TY
1330 A(3,1)=0:A(3,2)=0:A(3,3)=1:A(3,4)=TZ
1340 A(4,1)=0:A(4,2)=0:A(4,3)=0:A(4,4)=1
1350 RETURN
