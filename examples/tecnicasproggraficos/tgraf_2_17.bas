10 MODE 1
20 REM los tres caracteres que forman el camion 
30 SYMBOL 240,0,0,96,96,96,127,18,12
40 SYMBOL 241,0,0,0,0,0,255,0,0
50 SYMBOL 242,248,132,132,255,255,255,72,48 
60 camion$=CHR$(240)+CHR$(241)+CHR$(242)
70 x=1:y=13
80 LOCATE x,y
90 PRINT camion$
100 respuesta$=""
109 REM
110 WHILE respuesta$<>"e"
120 xnuevo=x
130 respuesta$=LOWER$(INKEY$)
140 IF respuesta$="." THEN xnuevo=x+1
149 REM si el camion se ha movido se borra con un espacio el antiguo caracter de la izquierda
150 IF xnuevo<>x THEN LOCATE x,y:PRINT " ";camion$
160 x=xnuevo
170 WEND
