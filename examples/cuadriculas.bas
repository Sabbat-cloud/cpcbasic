5 BORDER 26: INK 0,26: INK 1, 0
10 INPUT "Modo de pantalla (0 a 2)";modo
20 IF modo<0 OR modo>2 THEN PRINT "Incorrecto!":END
30 SYMBOL 255, 255,128,128,128,128,128,128,128
40 DIM columnas(2)
50 columnas(0)=20:columnas(1)=40:columnas(2)=80
60 MODE modo
70 FOR fila = 1 TO 25
80 FOR columna = 1 TO columnas(modo)
90 LOCATE columna, fila
100 PRINT CHR$(255);
110 NEXT columna
120 NEXT fila
130 MOVE 0,0:DRAW 639,0:DRAW 639,399
140 CALL &BB18
