10 MODE 1
20 GOSUB 1000
28 REM tintas que parpadeen entre dos colores
29 REM con alternancia entre ambas
30 INK 1,1,20 
12 INK 2,20,1
50 respuesta$=""
60 WHILE respuesta$=""
70 respuesta$=INKEY$
80 WEND
90 INK 1,24:INK 2,20
100 END
1053 REM ahora las dos tintas son iguales
1054 REM al dar el mismo color a la tinta 1 que a la tinta 2
1055 INK 1,20
2014 REM las lineas se dibujan alternando las dos tintas
2015 IF color=1 THEN color=2 ELSE color=1