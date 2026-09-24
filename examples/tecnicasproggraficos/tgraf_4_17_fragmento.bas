10 MODE 1
20 GOSUB 1000
29 REM las tintas 2 y 3 sol intermitentes y alternadas entre si
30 GOSUB 1500 
40 INK 2,1,20 
50 INK 3,20,1
59 REM se espera la pulsacion de una tecla
60 respuesta$=""
70 WHILE respuesta$=""
80 respuesta$=INKEY$
90 WEND
99 REM tintas normales
100 INK 2,20 
110 INK 3,6 
120 END
1504 REM tinta 3 igual a la 2
1505 INK 3,20
1594 REM los poligonos se dibujan alternativamente con una y otra tinta
1595 IF color=2 THEN color=3 ELSE color=2
