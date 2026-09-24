10 MODE 1
19 REM definicion de los dos caracteres con form a de perro
20 SYMBOL 240,0,132,135,132,124,130,130,0 
30 SYMBOL 241,0,36,71,132,124,130,65,0
40 perro1$=CHR$(240)
50 perro2$=CHR$(241)
60 perro$=perro1$
70 y=13
80 FOR x=1 TO 39
89    REM alternancia entre los dos caracteres perr o
90    IF perro$=perro1$ THEN perro$=perro2$ ELSE perro$=perro1$
100   LOCATE x,y
109   REM el espacio borra el perro anterior
110   PRINT " ";perro$
119   REM un tiempo de espera para que el movimiento no sea excesivamente rapido
120   tiempo=TIME
130   WHILE TIME<tiempo+30
140   WEND
150 NEXT
