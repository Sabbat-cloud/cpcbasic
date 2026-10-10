10 REM****PROGRAMA SUPERG****
20 REM Version del programa GRAFICA que representa dos variables
30 REM en una sola gráfica rotulada
40 INK 0,13
50 INK 1,0
60 READ titulo$
70 opcion=1:REM seleccione 1 para dibujar puntos y 2 para dibujar líneas
80 MODE 2
90 READ puntos
100 DIM x(puntos),y(puntos)
110 FOR i=1 TO puntos
120 READ x(i)
130 READ y(i)
140 NEXT i
150 READ xmin,xmax,ymin,ymax
160 READ x$:REM nombre del eje X
170 READ y$:REM nombre del eje Y
180 CLS
190 REM ahora dibuja los ejes
200 MOVE 100,380
210 DRAW 100,80
220 DRAW 550,80
230 REM genera las marcas de las escalas
240 FOR i=1 TO 11
250 MOVE 90,(i*30)+50
260 DRAW 100,(i*30)+50
270 NEXT i
280 FOR i=1 TO 16
290 MOVE (i*30)+70,70
300 DRAW (i*30)+70,80
310 NEXT i
320 REM imprime el titulo
330 p1=LEN(titulo$):p1=40-(p1/2)
340 LOCATE p1,1:PRINT titulo$;
350 REM ahora rotula los ejes
360 REM en primer lugar rotula el X
370 REM La posicion de comienzo es el centro del eje X menos la mitad de la longitud de la cadena
380 ax=(320-((LEN(x$)*16)/2))
390 REM la posicion de comienzo es el centro del eje Y mas la mitad de la longitud de la cadena
400 ay=(220+((LEN(y$)*16)/2))
410 TAG
420 MOVE ax,40
430 PRINT x$;
440 REM ahora imprime la leyenda del eje Y en vertical
450 FOR i=1 TO LEN(y$):m1$=MID$(y$,i,1)
460 MOVE 40,ay-((i-1)*16)
470 PRINT m1$;
480 NEXT i
490 MOVE 530,60:PRINT xmax;
500 MOVE 50,382:PRINT ymax;
510 MOVE 70,90:PRINT ymin;
520 MOVE 80,60:PRINT xmin;
530 MOVE 55,240:PRINT INT((ymax+ymin)/2);
540 MOVE 290,60:PRINT INT((xmax+xmin)/2);
550 REM ahora dibuja los puntos
560 IF opcion=2 THEN GOTO 640
570 FOR i=1 TO puntos
580 xtop=xmax-xmin:ytop=ymax-ymin
590 xtrue=xtop-(xmax-x(i)):ytrue=ytop-(ymax-y(i))
600 MOVE 96+(450*(xtrue/xtop)),86+(300*(ytrue/ytop))
610 PRINT CHR$(244);
620 NEXT i
630 |COPY:END
640 REM seccion de dibujo de lineas
650 FOR i=1 TO puntos
660 xtop=xmax-xmin:ytop=ymax-ymin
670 xtrue=xtop-(xmax-x(i)):ytrue=ytop-(ymax-y(i))
680 IF i=1 THEN MOVE 96+(450*(xtrue/xtop)),86+(300*(ytrue/ytop))
690 DRAW 96+(450*(xtrue/xtop)),86+(300*(ytrue/ytop))
700 NEXT i
710 |COPY:END
720 REM secuencia de datos: TITULO, NUM DE PUNTOS, VALX, VALY DE CADA PUNTO
730 REM XMIN, XMAX, YMIN, YMAX
740 REM X$, Y$
750 DATA "INDICE DE PARTICIPACION SOBRE UN PERIODO DE DIECISEIS AÑOS"
760 DATA 16,1970,380,1971,550,1972,500,1973,400,1974,270,1975,290,1976,480,1977
765 DATA 500,1978,500,1979,500,1980,495,1981,520,1982,540,1983,660,1984,800,1985,940
770 DATA 1970,1985,0,1000
780 DATA "AÑO","INDICE ORDINARIO"
