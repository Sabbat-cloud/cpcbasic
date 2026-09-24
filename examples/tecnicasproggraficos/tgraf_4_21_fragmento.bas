55 lineadib=0
999 REM dibujo de la recta (o no si lineadib=0) 
1000 PLOT x,y,colorvisible
1005 IF lineadib=0 THEN RETURN
1010 DRAW xant,yant
1020 RETURN
2070 IF respuesta$=" " THEN GOSUB 3000:lineadib= 1
2071 IF respuesta$="1" THEN IF lineadib=0 THEN lineadib=1 ELSE lineadib=0
