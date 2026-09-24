10 MODE 1
20 x=230:y=130
29 REM dibujar y rellenar un rectangulo
30 FOR xcord=x TO x+100 STEP 2 
40   MOVE xcord,y
50   DRAWR 0,100,1
60 NEXT
70 xprint=0:yprint=180
79 REM texto en el cursor grafico 
80 TAG
89 REM escribir el caracter en las sucesivas posiciones
90 FOR xcord=xprint TO 400 STEP 2 
100   MOVE xcord,yprint
110   PRINT CHR$(233);
120 NEXT
130 END

'-----

109 REM caracter que es una flecha sin borde blanco a la izquierda
110 PRINT CHR$(243);