10 MODE 1
20 radio=150
30 x=320:y=200
40 INPUT"Cuantos lados tiene la figura";lados 
50 CLS
60 paso=2*PI/lados
70 DIM x(lados),y(lados)
80 con=0
90 ORIGIN x,y
100 MOVE 0,radio
110 FOR angulo=0 TO 2*PI STEP paso
120   DRAW radio*SIN(angulo),radio*COS(angulo)
130   x(con)=radio*SIN(angulo):y(con)=radio*COS(angulo)
140   con=con+1
150 NEXT
155 DRAW 0,radio
160 FOR con1=1 TO lados-1
170   FOR con2=con1+1 TO lados
180     MOVE x(con1),y(con1)
190     DRAW x(con2),y(con2)
200   NEXT 
210 NEXT
