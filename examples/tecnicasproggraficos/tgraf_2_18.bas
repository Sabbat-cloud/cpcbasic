10 MODE 1
19 REM los tres caracteres que forman el cohete
20 SYMBOL 240,0,24,24,24,24,36,36,36
30 SYMBOL 241,36,36,36,36,36,36,36,36
40 SYMBOL 242,66,129,129,129,129,153,195,129
50 cohete$=CHR$(240)+CHR$(8)+CHR$(10)+CHR$(241)+ CHR$(8)+CHR$(10)+CHR$(242)
60 x=20:y=20
70 LOCATE x,y
80 PRINT cohete$
90 respuesta$=""
100 REM leer del teclado en tanto no se pulse 'e
110 WHILE respuesta$<>"e" AND y>1
120 ynuevo=y
130 respuesta$=LOWER$(INKEY$)
140 IF respuesta$="a" THEN ynuevo=y-1
150 REM si se ha movido el cohete se borra con un blanco el antiguo caracter inferior
160 IF ynuevo<>y THEN LOCATE x,y+2:PRINT " ":LOCATE x,ynuevo:PRINT cohete$
170 y=ynuevo
180 WEND
