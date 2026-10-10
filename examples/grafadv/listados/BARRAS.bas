10 REM **** AMPLIACION DEL PROGRAMA TABLA QUE DIBUJA BARRAS ****
20 REM Dibuja un diagrama de barras rotulado para un periodo de 12 meses
260 REM ahora dibuja las barras
270 READ mxx
280 xf=131
290 TAG:MOVE 105,360:PRINT mxx;
300 MOVE 105,235:PRINT mxx/2;
310 MOVE 105,112:PRINT 0;
320 FOR i =1 TO 12
340 READ valor
340 valor=((valor/mxx)*250)+112
350 xf=xf+32
360 REM dibuja el rectangulo para este mes
370 MOVE xf-8,valor:DRAW xf+8,valor
380 DRAW xf+8,112
390 DRAW xf-8,112
400 DRAW xf-8,valor
410 MOVE xf,115:fill 1
420 NEXT i
