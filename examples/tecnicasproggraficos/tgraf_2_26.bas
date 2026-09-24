1 DEFINT x,y
10 MODE 1
19 REM los tres caracteres que forman el camion
20 SYMBOL 240,0,0,96,96,96,127,19,12
21 SYMBOL 241,0,0,0,0,0,255,0,0
22 SYMBOL 242,240,132,132,255,255,255,72,48
30 camion$=CHR$(240)+CHR$(241)+CHR$(242)
40 xgrafico=0:ygrafico=200
49 REM asociar el texto al cursar grafico
50 TAG
55 tiempoinicial=TIME
60 FOR x=xgrafico TO 600
70   MOVE x,ygrafico
79   REM el espacio en blanca es para borrar la pa rte trasera del camion anterior
80   PRINT " "camion$;
90 NEXT
99 tiempototal=TIME
100 TAGOFF
110 LOCATE 1,20
120 PRINT "Tiempo transcurrido "(tiempototal-tiempoinicial)/300 "segundos"