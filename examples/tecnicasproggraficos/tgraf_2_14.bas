10 MODE 0
30 flecha$=CHR$(240)
40 PEN 1'
50 xflecha=13:yflecha=10
60 respuesta$=""
70 WHILE respuesta$<>"e"
80   ynuevo=yflecha:xnuevo=xflecha
90   respuesta$=INKEY$
100   IF respuesta$="a" AND yflecha>1 THEN ynuevo=yflecha-1:flecha$=CHR$(240)
110   IF respuesta$="z" AND yflecha<25 THEN ynuevo=yflecha+1:flecha$=CHR$(241)
120   IF respuesta$="," AND xflecha>1 THEN xnuevo=xflecha-1:flecha$=CHR$(243)
130   IF respuesta$="." AND xflecha<20 THEN xnuevo=xflecha+1:flecha$=CHR$(242)
140   IF xflecha<>xnuevo OR yflecha<>ynuevo THEN LOCATE xflecha,yflecha:PRINT " ";:xflecha=xnuevo: yflecha=ynuevo
150   LOCATE xflecha,yflecha
160   PRINT flecha$
170 WEND
