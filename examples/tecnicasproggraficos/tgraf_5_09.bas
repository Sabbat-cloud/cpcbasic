10 MODE 1
20 x=230:y=130
29 REM dibujar y rellenar un rectangulo
30 FOR xcord=x TO x-1-100 STEP 2
40   MOVE xcord,y
50   DRAWR 0,100,1
60 NEXT
70 xprint=0:yprint=180
71 REM opcion XOR
75 PRINT CHR$(23)CHR$(1);
80 TAG
89 REM escribir el caracter en las sucesivas pos iciones
90 FOR xcord=xprint TO 400 STEP 2
100   MOVE xcord,yprint
110   PRINT CHR$(243);
120 NEXT
129 REM opcion grafica normal y modo texto normal
130 TAGOFF
140 PRINT CHR$(23)CHR$(0);
150 END
