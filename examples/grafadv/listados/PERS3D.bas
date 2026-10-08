10 REM**** PROGRAMA PERS3D ****
20 REM Demostracion de un metodo de proyeccion en perspectiva
30 DIM x(60),y(60),z(60),ln(2,80),a(4,4)
40 DIM xp(60),yp(60),zp(60)
50 CLS
55 MODE 1:INK 0,13:INK 1,1:INK 2,3
60 INPUT "NOMBRE DEL FICHERO";n$
70 OPENIN n$
80 INPUT #9,npts
90 FOR i=1 TO npts
100 INPUT #9,x(i),y(i),z(i)
105 IF z(i)>0 THEN z(i)=z(i)-60
110 xp(i)=x(i)
120 yp(i)=y(i)
125 zp(i)=z(i)
130 NEXT i
140 INPUT #9,li
150 FOR i=1 TO li
160 INPUT #9,ln(1,i),ln(2,i)
170 NEXT i
180 CLOSEIN
182 REM Toma el eje de giro
183 INPUT"Eje de giro? - x=1, y=2, z=3";m
184 theta=0
190 REM Toma la distancia del observador al origen
195 INPUT"Distancia al origen";pp
222 GOSUB 400
225 REM Comienzo del bucle principal de rotacion
227 k$=INKEY$:IF k$="S" OR k$="s" THEN CLS:GOTO 182:REM Abortar esta rotacion
230 REM Ahora dibuja la casa
240 REM Las coordenadas son con respecto al origen, con traslacion al centro
245 CLS
247 GOSUB 1000:REM Dibujo de los ejes
250 FOR i=1 TO li
260 MOVE xp(ln(1,i))+320,yp(ln(1,i))+200
270 DRAW xp(ln(2,i))+320,yp(ln(2,i))+200,1,0
280 NEXT i
290 REM Giro de 10 grados
300 theta=theta+0.174533
310 a(m1,m2)=SIN(theta)
311 a(m1,m1)=COS(theta):a(m2,m2)=COS(theta):a(m2,m1)=-SIN(theta)
312 REM Borrado de la ultima figura
313 GOTO 320
314 FOR i=1 TO li
316 MOVE xp(ln(1,i))+200,yp(ln(1,i))+200
317 DRAW xp(ln(2,i))+200,yp(ln(2,i))+200,1,1
318 NEXT i
320 REM Calculo de la proyeccion en el plano X,Y
330 FOR i=1 TO npts
340 xt=a(1,1)*x(i)+a(1,2)*y(i)+a(1,3)*z(i)+a(1,4)
350 yt=a(2,1)*x(i)+a(2,2)*y(i)+a(2,3)*z(i)+a(2,4)
352 zt=a(3,1)*x(i)+a(3,2)*y(i)+a(3,3)*z(i)+a(3,4)
354 dd=zt+pp:xp(i)=xt*pp/dd:yp(i)=yt*pp/dd:zp(i)=dd
360 NEXT i
370 REM Fin del bucle principal
380 GOTO 225
400 REM Subrutina de rotacion
410 c=COS(theta)
420 s=SIN(theta)
430 FOR k=1 TO 4
440 FOR l=1 TO 4
450 a(k,l)=0
460 NEXT l
470 NEXT k
475 REM Ahora calcula las inserciones correctas de la matriz
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
1032 LOCATE 20,6:PRINT"X"
1034 LOCATE 26,14:PRINT"Y"
1036 LOCATE 20,14:PRINT"Z"
1040 RETURN
