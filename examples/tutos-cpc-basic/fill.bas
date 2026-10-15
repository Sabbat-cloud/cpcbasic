10 MODE 1
20 ink 0,0: ink 1,2: ink 2,15: ink 3,23
30 border 0
40 paper 0
50 for s=1 to 50
60 x = rnd*640
70 y = rnd*400
80 plot x,y,3
90 next s
100 ORIGIN 320,200
110 DEG
120 MOVE 0,100
130 FOR d=0 TO 360 STEP 10
140 DRAW 100*SIN(d),100*COS(d),1
150 NEXT
160 MOVE 0,0
170 FILL 2
180 while inkey$="": wend
190 call 0
