10 MODE 1
20 xorigen=320:yorigen=200
30 ORIGIN xorigen,yorigen
40 MOVER 100,0
50 FOR angulo=0 TO 32 STEP PI/30
60   DRAW 100*COS(angulo),100*SIN(angulo*0.8) 
70 NEXT