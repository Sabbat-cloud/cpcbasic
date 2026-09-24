10 MODE 1
19 REM se usan numeras enteros para mayor velocidad
20 DEFINT c,f,x,y
30 xorigen=320:yorigen=200
39 REM cambie estos factores para obtener diferentes efectos
40 factor1=3:factor2=1
50 factord=factor1-factor2
60 ORIGIN xorigen,yorigen
69 REM el bucle dibuja cuatro rectas de posicion variable
70 FOR con=0 TO 200
80    MOVE 0,0:MOVER con*factor1,0 
90    DRAWR -con*factord,200
100   MOVER -con*factor2*2,0
110   DRAWR -con*factord,-200
120   DRAWR con*factord,-200
130   MOVER con*factor2*2,0
140   DRAWR con*factord,200
150 NEXT
