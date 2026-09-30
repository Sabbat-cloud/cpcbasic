10 MODE 2
20 FOR x=0 TO 26
30   CLS
40   INK 0,x
50   FOR y=0 TO 26
60     IF x<>y THEN INK 1,y:PRINT "Color "; y
70     respuesta$=""
80      WHILE respuesta$=""
90       respuesta$=INKEY$
100     WEND 
110   NEXT 
120 NEXT
