10 MODE 0
998 REM tinta 3 amarilla para que resulte adecuado el resultado del solapamiento cyan/amarillo
999 REM amarillo es el color de primer plano
1000 INK 3,24
1001 REM tinta 6 cyan para que resulte adecuado el resultado del solapamiento cyan/blanco
1002 REM blanco es el color del fondo
1003 INK 6,20 
2071 MOVE 0,0 
2072 DRAW 0,0,2
3030 FOR xcord=xprint TO 550 STEP 4
4000 IF color =1 THEN color=4 ELSE color=1
4010 FOR xcord=x TO x+30 STEP 2
4020   MOVE xcord,y
4030   DRAWR 0,100,color
4040 NEXT
4050 RETURN
