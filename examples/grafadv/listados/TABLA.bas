10 REM ****PROGRAMA TABLA****
20 REM dibuja una tabla rotulada para un periodo de 12 meses
30 REM por ejemplo, para representar ventas, fluctuaciones de la demanda, etc
40 REM los datos están al final del programa, pero la entrada interactiva de los mismos exige una simple modificación
50 DIM xp(12),yp(12)
60 CLS:MODE 2:INK 0,13:INK 1,0
70 REM entrada de rotulos
80 INPUT "TITULO PRINCIPAL (Maximo 80 caracteres)";t$
90 INPUT "TITULO LATERAL (Maximo 20 caracteres)";s$
95 INPUT"SUBTITULO LATERAL (Maximo 20 caracteres)";s1$
100 REM ahora calcula las posiciones de los titulos
110 t1=LEN(t$)
120 t2=LEN(s$)
125 t3=LEN(s1$)
130 xt=40-(t1/2)
140 xs=10-(t2/2)
145 xs1=10-(t3/2)
150 CLS
160 LOCATE xt,2:PRINT t$
170 LOCATE xs,12:PRINT s$
175 LOCATE xs1,13:PRINT s1$
180 GOSUB 450:REM pone en pantalla las leyendas de los meses
190 REM ahora dibuja los ejes
200 MOVE 145,365:DRAW 145,105
210 DRAW 550,105
220 REM hace las graduaciones del eje Y
230 FOR y=362 TO 112 STEP -25
240 MOVE 142,y:DRAW 147,y
250 NEXT y
260 REM dibujo de la tabla
270 READ mxx
280 xf=131
290 TAG:MOVE 105,360:PRINT mxx;
300 MOVE 105,235:PRINT mxx/2;
310 MOVE 105,112:PRINT 0;
320 FOR i=1 TO 12
330 READ valor
340 valor=((valor/mxx)*250)+112
350 xf=xf+32
360 IF i=1 THEN x2=xf:y2=valor
370 x1=x2:y1=y2
380 x2=xf:y2=valor
390 MOVE x1,y1
400 DRAW x2,y2
420 NEXT i
430 |COPY:REM Este es un comando del programa Tascopy
440 GOTO 440
450 REM leyendas de los meses
460 LOCATE 1,19
470 PRINT TAB(21);"|   |   |   |   |   |   |   |   |   |   |   |"
480 PRINT TAB(21);"E   F   M   A   M   J   J   A   S   O   N   D"
490 PRINT TAB(21);"N   E   A   B   A   U   U   G   E   C   O   I"
500 PRINT TAB(21);"E   B   R   R   Y   N   L   O   P   T   V   C"
510 RETURN
520 DATA 10
530 DATA 1.6,1.8,2.5,2.7,1.1,3.6,4.6,5.9,7.2,8.1,7.1,9.3
