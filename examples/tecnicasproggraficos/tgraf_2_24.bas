10 MODE 1
19 REM los tres caracteres que forman el camion
20 SYMBOL 240,0,0,96,96,96,127,18,12
21 SYMBOL 241,0,0,0,0,0,255,0,0
22 SYMBOL 242,248,132,132,255,255,255,72,48
30 camion$=CHR$(240)+CHR$(241)+CHR$(242)
40 xgrafico=0:ygrafico=200
49 REM asociar el texto al cursor grafico
50 TAG
60 FOR x=xgrafico TO 600
70   MOVE x,ygrafico
79   REM el espacio en blanco es para borrar la parte trasera del camion anterior
80   PRINT " "camion$;
90 NEXT
