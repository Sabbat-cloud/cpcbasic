5 REM ****PROGRAMA DISEÑO****
10 cs=2:ss=5
15 MODE 1
30 INK 0,13:INK 1,1:INK 2,3
45 CLS
50 REM Definicion del tamaño y pasos del cursor
60 fl=0:npts=1:na=1
70 lb=0:REM contador de lineas
80 se=0:REM indicador de fin de segmento
90 s1=0:REM contador de segmentos
91 sp=0:REM contador de elementos de la figura
92 fi=0:REM indicador de corte de linea
93 li=0:REM contador de lineas del segmento
94 jy=1:REM indicador de comienzo/final de linea
95 pf=1:REM indicador del tipo de segmento
100 DIM xp(500),yp(500),ln(2,500),s(3,10),rd(3,100):REM Dimensionamiento de matrices
110 GOTO 1690:REM vuelta al menu principal
120 REM colocacion del cursor en la posicion central
125 IF pf=2 THEN GOSUB 2900
130 x=320:y=200
140 GOSUB 180:REM rutina de dibujo del cursor
150 GOSUB 230:REM rutina de movimiento del cursor
160 GOSUB 340:REM rutina de barrido de la linea
170 GOTO 140
180 REM rutina de dibujo del cursor
190 x1=x-cs:y1=y-cs:x2=x+cs:y2=y+cs
200 MOVE x1,y
205 DRAW x2,y,1,1
210 MOVE x,y1
215 DRAW x,y2,1,1
220 RETURN
230 REM rutina de movimiento del cursor
240 y3=y:x3=x
250 IF JOY(0)=0 THEN 310
260 IF JOY(0)=1 THEN y=y+ss:GOTO 310
270 IF JOY(0)=2 THEN y=y-ss:GOTO 310
280 IF JOY(0)=4 THEN x=x-ss:GOTO 310
290 IF JOY(0)=8 THEN x=x+ss:GOTO 310
310 MOVE x3,y2
320 DRAW x3,y1,1,1
325 MOVE x1,y3
326 DRAW x2,y3,1,1
330 RETURN
340 REM rutina de dibujo y barrido de la linea
350 a$=INKEY$
355 IF a$="" AND JOY(0)<>16 THEN IF fl=0 THEN RETURN
370 IF JOY(0)=16 AND jy=1 THEN jy=2:LOCATE 2,2:PRINT "S":GOSUB 3000:GOTO 430
380 IF JOY(0)=16 AND jy=2 THEN jy=1:LOCATE 2,2:PRINT "F":GOSUB 3000:GOTO 460
390 IF a$="B" THEN jy=1 THEN jy=1:GOTO 450:REM corte de linea
400 IF a$="E" THEN se=1:jy=1:GOTO 460:REM fin de la figura
420 GOTO 650:REM dibujo/borrado normal de la linesa
430 xi=x:yi=y:REM coordenadas de comienzo
440 fl=1
450 fi=1:REM indicador de corte de linea
460 xf=x:yf=y:REM asignacion de punto
480 MOVE xi,yi
485 DRAW xf,yf
490 npts=npts+1:na=na+1:li=li+1:lb=lb+1:REM incrementa contadores
500 xp(na)=xf:yp(na)=yf:REM asignacion de punto
510 xp(na-1)=xi:yp(na-1)=yi:REM asignacion de puntos
560 ln(1,lb)=na-1:REM asignacion de indices de linea
570 ln(2,lb)=na
580 IF fi=1 THEN na=na+1:fi=0:REM incremento si el indicador de corte esta activado
590 IF se=1 THEN s1=s1+1:s(1,s1)=npts-li:s(2,s1)=npts-1:s(3,s1)=0:GOTO 690
630 fl=0:RETURN
640 fl=0
650 REM realizacion del dibujo/borrado de la linea
660 MOVE x,y
665 DRAW xi,yi,1,1
670 MOVE x,y
675 DRAW xi,yi,1,1
680 RETURN
690 REM continuar
710 FOR i=s(1,s1) TO s(2,s1)
730 MOVE xp(ln(1,i)),yp(ln(1,i))
735 DRAW xp(ln(2,i)),yp(ln(2,i)),1,0
740 NEXT i
750 k$=INKEY$:IF k$="" THEN 750
780 li=0:fl=0:se=0:na=na+1:REM si, entonces actualiza los contadores
790 IF pf=1 THEN 1690:REM trazado, entonces volver al menu principal
792 GOSUB 1000:REM comprimir el elemento de la figura
794 GOTO 1690:REM vuelta al menu principal
796 GOTO 120
800 REM ahora crea el fichero que contiene los datos
810 CLS
820 INPUT"nombre del fichero de salida";n$
830 OPENOUT n$
840 WRITE#9,na
850 FOR i=1 TO na
860 WRITE#9,xp(i)
870 WRITE#9,yp(i)
875 NEXT i
880 WRITE#9,lb
890 FOR i=1 TO lb
900 WRITE#9,ln(1,i)
910 WRITE#9,ln(2,i)
915 NEXT i
920 WRITE#9,s1
930 FOR i=1 TO s1
940 WRITE#9,s(1,i)
950 WRITE#9,s(2,i)
965 NEXT i
970 PRINT#9,sp
980 FOR i=1 TO sp
982 PRINT#9,rd(1,i),rd(2,i),rd(3,i)
984 NEXT i
986 CLOSEOUT
1000 REM comprime el elemento de la figura
1030 REM imprime "tamaño del elemento:"
1040 REM INPUT "Anchura en pixels?";PW
1060 REM define punteros maximos y minimos
1070 xh=0:xl=640:yh=0:yl=400
1080 l1=ln(1,s(1,s1)):l2=ln(2,s(2,s1))
1085 FOR i=l1 TO l2
1090 IF xp(i)<xh THEN xl=xp(i)
1100 IF xp(i)>xh THEN xh=xp(i)
1110 IF yp(i)<yl THEN yl=yp(i)
1120 IF yp(i)>yh THEN yh=yp(i)
1130 NEXT i
1140 REM ajusta la anchura
1145 wi=0.16
1150 REM calcula el punto central para trasladarlo al origen
1160 xc=((xh+xl)/2)*wi:yc=((yh+yl)/2)*wi
1170 REM ahora reduce el tamaño del objeto y lo lleva al origen
1180 FOR i=l1 TO l2
1185 xp(i)=(xp(i)*wi)-xc
1186 yp(i)=(yp(i)*wi)-yc
1187 NEXT i
1190 RETURN
1200 REM coloca en pantalla los segmentos
1210 sm=0:x=320:y=200
1220 GOSUB 180:REM rutina de dibujo del cursor
1230 GOSUB 230:REM rutina de movimiento del cursor
1235 IF x>574 THEN GOSUB 1900:REM escoger segmento
1240 IF JOY(0)=16 THEN GOSUB 1260:REM dibujar segmento
1245 IF x<4 THEN GOTO 1690:REM regreso al menu principal
1250 GOTO 1220:REM regreso del bucle
1260 REM dibujo del segmento
1265 sp=sp+1:rd(1,sp)=x:rd(2,sp)=y:rd(3,sp)=sm
1270 FOR i=s(1,sm) TO s(2,sm)
1280 l1=ln(1,i):l2=ln(2,i)
1285 MOVE xp(l1)+x,yp(l1)+y
1290 DRAW xp(l2)+x,yp(l2)+y,2,0
1300 NEXT i
1310 RETURN
1330 REM rutina de entrada de fichero
1340 INPUT"nombre del fichero de entrada";h$
1360 OPENIN h$
1370 INPUT#9,npts
1380 FOR i=1 TO npts
1390 INPUT#9,xp(i),yp(i)
1395 NEXT i
1400 INPUT#9,li
1420 FOR i=1 TO li
1425 INPUT#9,ln(1,i),ln(2,i)
1427 NEXT i
1430 INPUT#9,s1
1440 FOR i=1 TO s1
1450 INPUT#9,s(1,i),s(2,i)
1460 NEXT i
1465 INPUT#9,sp
1470 FOR i=1 TO sp
1475 INPUT#9,rd(1,i),rd(2,i),rd(3,i)
1480 NEXT i
1485 CLOSEIN
1490 PRINT"fichero",h$,"cargado correctamente"
1500 RETURN
1560 REM rutina de dibujo de los límites de la hoja de diseño
1570 MOVE 6,394
1575 DRAW 146,394
1580 MOVE 440,394
1590 DRAW 634,394
1600 DRAW 634,6
1610 DRAW 6,6
1620 DRAW 6,394
1630 MOVE 574,394
1635 DRAW 574,6
1640 FOR i=60 TO 340 STEP 56
1645 MOVE 574,i
1650 DRAW 634,i
1655 NEXT i
1660 MOVE 574,34
1665 DRAW 634,34
1670 LOCATE 13,1:PRINT"RECINTO DE DISEÑO"
1675 IF pf=1 THEN LOCATE 1,1:PRINT"TRAZADO"
1676 RETURN
1680 REM MENU PRINCIPAL
1690 CLS:pf=2
1700 PRINT
1710 PRINT"          DISEÑO - MENU PRINCIPAL"
1720 PRINT"      DIBUJAR EL TRAZADO DE LA IMAGEN        - 1"
1740 PRINT"      DEFINIR ELEMENTOS                      - 2"
1750 PRINT"      GRABAR LA FIGURA                       - 3"
1755 PRINT"      GRABAR SOLO LOS ELEMENTOS              - 4"
1760 PRINT"      CARGAR FIGURA                          - 5"
1770 PRINT"      DIBUJAR LOS ELEMENTOS DEL TRAZADO      - 6"
1780 PRINT"      BORRAR ELEMENTOS ANTES DE DIBUJARLOS   - 7"
1790 PRINT"      IMPRIMIR LA FIGURA                     - 8"
1792 PRINT"      SALIR DEL PROGRAMA                     - 9"
1794 k$=INKEY$: IF k$="" THEN 1794
1796 IF k$="1" THEN pf=1 :CLS:GOSUB 1570:GOTO 120:REM definir trazado
1800 IF k$="2" THEN pf=2 :CLS:GOTO 120:REM definir elemento
1810 IF k$="3" THEN GOTO 810:REM grabar todo
1815 IF k$="4" THEN GOSUB 2700:GOTO 1680:REM grabar solo los elementos
1820 IF k$="5" THEN sp=0:GOSUB 2300:GOTO 1690:REM cargar todo
1830 IF k$="6" THEN CLS:GOSUB 2000:GOSUB 1570:GOSUB 2100:GOTO 1210
1840 IF k$="7" THEN CLS:sp=0:s1=1:GOSUB 2000:GOSUB 1570:GOSUB 2100:GOTO 1210
1850 IF k$="8" THEN |COPY:GOTO 1680:REM volcado de pantalla con Tascopy
1860 IF k$="9" THEN PRINT"PROGRAMA ABANDONADO":END
1870 GOTO 1794
1900 REM rutina de eleccion de segmento para su dibujo
1910 IF y>340 THEN sm=2:RETURN
1920 IF y>284 THEN sm=3:RETURN
1930 IF y>228 THEN sm=4:RETURN
1940 IF y>172 THEN sm=5:RETURN
1950 IF y>116 THEN sm=6:RETURN
1960 IF y>60 THEN lcopy:sm=7:RETURN
1965 IF y>32 THEN GOSUB 2200:x=x-30:RETURN:REM regenerar la figura
1970 IF y<34 THEN GOTO 1690
1990 IF JOY(0)<>16 THEN RETURN
2000 REM rutina de dibujo de segmento
2010 ya=424
2020 IF s1=1 THEN 2085
2027 FOR i=2 TO s1
2030 ya=ya-56
2040 FOR j=s(1,i) TO s(2,i)
2060 MOVE xp(ln(1,j))+604,yp(ln(1,j))+ya
2065 DRAW xp(ln(2,j))+604,yp(ln(2,j))+ya,2,0
2070 NEXT j
2080 NEXT i
2082 TAG
2085 MOVE 574,54:PRINT"RELL "
2090 MOVE 574,26:PRINT"SAL  "
2092 TAGOFF
2095 RETURN
2100 REM regeneracion del trazado del diseño
2110 FOR i=s(1,1) TO s(2,1)
2120 l1=ln(1,i):l2=ln(2,i)
2130 MOVE xp(l1),yp(l1)
2135 DRAW xp(l2),yp(l2),1,0
2140 NEXT i
2150 RETURN
2200 REM rutina de regeneracion de la figura
2215 IF sp=0 THEN GOSUB 2100:RETURN
2220 FOR i=1 TO sp
2230 xx=rd(1,i):yy=rd(2,i)
2235 FOR j=s(1,rd(3,i)) TO s(2,rd(3,i))
2240 l1=ln(1,j):l2=ln(2,j)
