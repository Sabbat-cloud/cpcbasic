84 REM definicion del caracter flecha
85 SYMBOL 240,8,12,14,127,127,14,12,8
86 REM definicion del caracter auxiliar para XOR
87 SYMBOL 241,24,20,18,129,129,18,20,24
90 FOR xcord=xprint TO 400 STEP 2
100   MOVE xcord,yprint
108   REM escribir la flecha normal en la primera posicion
109   REM y usar XOR para trasladar la flecha a la siguiente posicion
110   IF xcord=xprint THEN PRINT CHR$(240); ELSE PRINT CHR$(241);
120 NEXT
129 REM opcion grafica normal y modo texto normal
130 TAGOFF
140 PRINT CHR$(23)CHR$(0);
150 END
