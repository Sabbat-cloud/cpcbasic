10 MODE 1
20 xorigen=320:yorigen=200
30 ORIGIN xorigen,yorigen
40 color=1
50 FOR angulo=0 TO 20 STEP PI/30
53   IF angulo>10 THEN color=3
55   MOVE 200*SIN(angulo),200*COS(angulo)
60   DRAW 100*COS(angulo*3),200*SIN(angulo/3),color
70 NEXT
