10 REM****PROGRAMA ENFASIS****
20 REM version del programa tabla que resalta la comparacion entre dos conjuntos de datos
30 REM Dibuja una gráfica rotulada para un periodo de doce meses
40 REM por ejemplo, para representar ventas, fluctuaciones de demanda,,
50 REM Los datos estánal final del programa, pero la introuccion interactiva requiere solo un sencillo cambio
70 REM Esta versión rellena las areas situadas entre ambos conjuntos de datos
80 REM con un color diferente, segun cual sea la que supera a la otra
90 REM la orden FILL solo esta disponible en el CPC 664/6128
100 REM se utiliza el modo 1
110 DIM xp(12),yp(12),comp(2,12):REM COMP sirve para guardar pares de puntos de datos
120 CLS:MODE 1:INK 0,13:INK 1,0:INK 2,2:INK 3,20
130 REM entrada de rotulos
140 INPUT "TITULO PRINCIPAL (Max 40 caracteres)";t$
150 INPUT "TITULO LATERAL (Max 20 caracteres)";s$
160 INPUT"SUBTITULO LATERAL (Max 10 caracteres)";s1$
170 REM calculo de las posiciones de los titulos
180 t1=LEN(t$)
190 t2=LEN(s$)
200 t3=LEN(s1$)
210 xt=20-(t1/2)
220 xs=5-(t2/2)
230 xs1=5-(t3/2)
240 CLS
250 LOCATE xt+1,1:PRINT t$
260 LOCATE xs,6:PRINT s$
270 LOCATE xs1,15:PRINT s1$
280 GOSUB 700:REM colocacione de las leyendas de los meses en pantalla
290 REM ahora dibuja los ejes
300 MOVE 164,365:DRAW 164,105
310 DRAW 520,105
320 MOVE 520,105:DRAW 520,365
330 REM ahora hace las graduaciones del eje Y
340 FOR y=362 TO 112 STEP -25
350 MOVE 161,y:DRAW 167,y
360 NEXT y
370 REM dibuja la primera linea
380 READ mxx
390 xf=135
400 TAG:MOVE 85,360:PRINT mxx;
410 MOVE 90,235:PRINT mxx/2;
420 MOVE 98,112:PRINT 0;
430 FOR i=1 TO 12
440 READ valor
450 valor=((valor/mxx)*250)+112
460 comp(1,i)=valor:REM carga el valor del punto para su posterior comparacion
470 ymin=115
480 xf=xf+32
490 IF i=1 THEN x2=xf:y2=valor
500 x1=x2:y1=y2
510 x2=xf:y2=valor
520 MOVE x1,y1
530 DRAW x2,y2
540 NEXT i
550 REM dibuja la segunda linea
560 xf=135
570 FOR i=1 TO 12
580 READ valor
590 valor=((valor/mxx)*250)+112
600 comp(2,i)=valor:REM carga el valor del punto para su posterior comparacion
610 xf=xf+32
620 IF i=1 THEN x2=xf:y2=valor
630 x1=x2:y1=y2
640 x2=xf:y2=valor
650 MOVE x1,y1
660 DRAW x2,y2
670 NEXT i
680 GOSUB 800:REM rellena las areas con color
690 |COPY:END
700 REM leyendas de los meses
710 LOCATE 1,19
720 PRINT TAB(11);"| | | | | | | | | | | |"
730 PRINT TAB(11);"E F M A M J J A S O N D"
740 PRINT TAB(11);"N E A B A U U G E C O I"
750 PRINT TAB(11);"E B R R Y N L O P T V C"
760 RETURN
770 DATA 100
780 DATA 80,45,40,10,30,50,65,80,60,40,30,10
790 DATA 20,30,50,70,60,55,30,50,60,70,90,95
800 REM Ahora rellena las áreas de color con el comando FILL
810 xx=135
820 FOR i=1 TO 12
830 IF comp(1,i)<comp(2,i) THEN col=2
840 IF comp(1,i)>comp(2,i) THEN col=3
850 IF comp(1,i)=comp(2,i) THEN xx=xx+32:GOTO 900
860 yy=(comp(1,i)+comp(2,i))/2
870 xx=xx+32
880 MOVE xx,yy
890 FILL col
900 NEXT i
910 RETURN
