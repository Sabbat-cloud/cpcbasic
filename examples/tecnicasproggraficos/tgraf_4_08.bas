10 MODE 1
20 xorigen=320:yorigen=200
30 ORIGIN xorigen,yorigen
50 FOR angulo=0 TO 6.4 STEP PI/35
55   MOVE 300*SIN(angulo),50*COS(angulo)
60   DRAW 10*COS(angulo/5),200*SIN(angulo*2) 
70 NEXT