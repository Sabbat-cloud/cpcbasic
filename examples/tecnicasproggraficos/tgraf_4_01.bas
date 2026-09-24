10 MODE 1
20 x=320:y=200
28 REM maximo da la longitud de los brazos de la figura
29 REM pruebe cambiando maximo y paso
30 maximo=200
40 paso=5
50 FOR con=0 TO maximo STEP paso
60   MOVE x-con,y
70   DRAW x,y+(maximo-con) 
80   DRAW x+con,y
90   DRAW x,y-(maximo-con) 
100  DRAW x-con,y
110 NEXT
