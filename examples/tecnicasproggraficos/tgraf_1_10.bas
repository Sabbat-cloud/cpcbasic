10 MODE 0
20 x=0:y=0
30 color=1
40 FOR con=0 TO 350 STEP 4
50 MOVE x+con,y
60 DRAW x+350,y+con,color
70 MOVE x,y+con
80 DRAW x+con,y+350
90 color=(color+1) MOD 16
100 NEXT
