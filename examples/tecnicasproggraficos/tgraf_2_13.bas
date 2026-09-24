10 MODE 0
20 SYMBOL 240,0,4,7,132,124,130,130,0
30 perro$=CHR$(240)
40 PEN 1
50 xperro=13:yperro=10
60 respuesta$=""
70 WHILE respuesta$<>"e"
80   ynuevo=yperro:xnuevo=xperro
90   respuesta$=INKEY$
100   IF respuesta$="a" AND yperro>1 THEN ynuevo=yperro-1
110   IF respuesta$="z" AND yperro<25 THEN ynuevo=yperro+1
120   IF respuesta$="," AND xperro>1 THEN xnuevo=xperro-1
130   IF respuesta$="." AND xperro<20 THEN xnuevo=xperro+1
140   IF xperro<>xnuevo OR yperro<>ynuevo THEN LOCATE xperro,yperro:PRINT " ";:xperro=xnuevo:yperro=ynuevo
150   LOCATE xperro,yperro
160   PRINT perro$
170 WEND
