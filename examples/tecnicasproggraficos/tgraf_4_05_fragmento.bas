35 color1=1:color2=1
70 FOR con=0 TO 200
80 MOVE 0,0:MOVER con*factor1,0 
90 DRAWR -con*factord,200,colorl
100 MOVER -con*factor2*2,0
110 DRAWR -con*factord,-200,color2 
120 DRAWR con*factord,-200,co1orl
130 MOVER con*factor2*2,0
140 DRAWR con*factord, 200,color2
150 color1=1+(color1+1) MOD 4: color2=1+(color2+1) MOD 4
160 NEXT
