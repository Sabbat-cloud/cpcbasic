10 MODE 1
20 xorigen=320:yorigen=200
30 ORIGIN xorigen,yorigen
40 MOVER 100,0
50 FOR angulo=0 TO 6.4 STEP PI/35
55   MOVE 200*SIN(angu1o),100*COS(angulo) 
60   DRAW 100*COS(angulo),200*SIN(angulo) 
70 NEXT
