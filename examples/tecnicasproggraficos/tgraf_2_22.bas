10 MODE 1
19 REM definicion del invasor extraterrestre
20 SYMBOL 240,24,60,126,219,255,255,165,165
30 invasor$=CHR$(240)
40 xgrafico=100:ygrafico=200
49 REM asociar el texto al •cursor grafito
50 TAG
60 FOR x=xgrafico TO 600 
70   MOVE x,ygrafico
78   REM el espacio en blanco es para borrar el invasor de la posicion anterior
79   REM elimine el punto y coma para probar
80   PRINT " "invasor$; 
90 NEXT
