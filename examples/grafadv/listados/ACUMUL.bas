10 REM ****PROGRAMA TABLA****
12 REM ampliacion acumulativa
15 ymin=400
45 REM esta version dibuja una grafica acumulativa para dos conjuntos de datos
46 REM el conjunto inferior de datos esta sombreado
260 REM ahora dibuja la gráfica superior
270 READ mxx
280 xf=131
290 TAG:MOVE 105,360:PRINT mxx;
300 MOVE 105,235:PRINT mxx/2;
310 MOVE 105,112:PRINT 0;
320 FOR i=1 TO 12
330 READ valor
340 valor=((valor/mxx)*250)+112
345 ymin=115
350 xf=xf+32
360 IF i=1 THEN x2=xf:y2=valor
370 x1=x2:y1=y2
380 x2=xf:y2=valor
390 MOVE x1,y1
400 DRAW x2,y2
420 NEXT i
422 REM ahora dibuja la linea inferior
426 xf=131
428 FOR i=1 TO 12
430 READ valor
432 valor=((valor/mxx)*250)+112
434 xf=xf+32
436 IF i=1 THEN x2=xf:y2=valor
438 x1=x2:y1=y2
439 x2=xf:y2=valor
440 MOVE x1,y1
442 DRAW x2,y2
444 NEXT i
446 GOSUB 1000:REM Rellena el area superior
448 GOTO 448
520 DATA 10
530 DATA 3.6,5.8,4.5,6.7,3.1,5.6,5.6,6.9,7.9,8.9,6.1,9.3
540 DATA 1.1,1.3,2.1,1.3,0.6,1.2,3.3,3.2,4.3,5.1,3.2,4.1
1000 REM valores de sombreado de la linea superior
1005 inc=4
1010 yval=ymin-2:REM posicion del motivo que constituye el patron de sombreado
1015 xx=250+inc
1020 FOR yy=yval TO 400 STEP 2
1030 IF TEST(xx,yy)<>0 THEN 1100
1040 PLOT xx,yy
1065 NEXT yy
1100 FOR yy=yval TO 0 STEP -2
1110 IF TEST(xx,yy)<>0 THEN 1200
1120 PLOT xx,yy
1130 NEXT yy
1200 xx=xx+inc
1210 IF xx>515 THEN inc=-inc:xx=250
1220 IF xx<165 THEN RETURN
1230 GOTO 1020
