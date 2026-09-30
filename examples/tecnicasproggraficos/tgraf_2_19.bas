10 MODE 1
19 REM los tres caracteres que definen el cohete
20 SYMBOL 240,0,24,24,24,24,36,36,36
30 SYMBOL 241,36,36,36,36,36,36,36,36
40 SYMBOL 242,66,129,129,129,129,153,195,129
49 REM definicion del cohete usando movimientos del cursor
50 cohete$=CHR$(240)+CHR$(8)+CHR$(10)+CHR$(241)+ CHR$(8)+CHR$(10)+CHR$(242)
59 REM con este procedimiento la coordenada x no debe pasar de 34
60 x=1:y=20
70 LOCATE 3,23
80 PRINT "Definido con movimientos del cursor" 
90    FOR ycoord=y TO 1 STEP -1
100   LOCATE x,ycoord+3
110   PRINT " "
120   LOCATE x,ycoord
130   PRINT cohete$
140 NEXT
149 REM hay que pulsar una tecla para continuar la demostracion
150 respuesta$=""
160 WHILE respuesta$=""
170 respuesta$=LOWER$(INKEY$)
180 WEND
190 CLS
199 REM con este procedimiento la coordenada s p uede tomar cualquier valor
200 x=36:y=20
210 LOCATE 7,23
220 PRINT "Definido usando LOCATE para cada parte"
229 REM cada parte del cohete se coloca mediante su propia instruccion LOCATE
230 FOR ycoord=y TO 1 STEP -1
240   LOCATE x,ycoord 
250   PRINT CHR$(240) 
260   LOCATE x,ycoord+1 
270   PRINT CHR$(241) 
280   LOCATE x,ycoord+2 
290   PRINT CHR$(242)
299   REM Se horra la base del cohete de la posicion anterior
300   LOCATE x,ycoord+3
310   PRINT " "
320 NEXT
