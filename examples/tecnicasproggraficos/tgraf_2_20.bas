10 MODE 1
19 REM definicion de los dos caracteres con form a de culebra
20 SYMBOL 240,0,0,32,80,81,74,130
30 SYMBOL 241,0,0,0,132,74,81,80,32
40 culebra1$=CHR$(240)
50 culebra2$=CHR$(241)
60 culebra$=culebra1$
70 y=13
80 FOR x=1 TO 39
89    REM alternancia entre los dos caracteres culebra
90    IF culebra$=culebra1$ THEN culebra$=culebra2$ ELSE culebra$=culebra1$
100   LOCATE x,y
109   REM el espacio borra la culebra anterior
110   PRINT " ";culebra$
119   REM un tiempo de espera para que el movimiento no sea excesivamente rapido
120   tiempo=TIME
130   WHILE TIME<tiempo+30
140   WEND
150 NEXT
