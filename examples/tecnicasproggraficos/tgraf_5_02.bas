10 MODE 1
20 GOSUB 1000
30 GOSUB 2000
40 END
998 REM leer en dos conjuntos de 26 coordenadas
999 REM para dibujar dos posiciones del perro 
1000 DIM x(100),y(100)
1010 FOR con=1 TO 52
1020   READ x(con),y(con)
1030   NEXT
1040 RETURN
1050 DATA 0,0,20,40,20,40,10,80,10,80,0,120,20,10,35,50,35,50,10,80,10,80,70,80
1060 DATA 60,0,80,40,80,40,70,80,80,10,95,50,95,50,70,80,70,80,90,140,90,140,110,120,110,120,80,110
1070 DATA 5,10,25,40,25,40,15,80,15,80,10,120,0,15,30,50,30,50,15,80,15,80,75,80
1080 DATA 75,80,85,40,85,40,65,10,75,80,90,50,90,50,60,15,75,80,100,130,100,130,120,110,120,110,90,100
1999 REM dibujar y borrar sucesivamente el perro 
2000 xinc=0
2010 indicador=0
2020 WHILE x(1)+xinc<639
2030   IF indicador=0 THEN comienzo=1:indicador=1 ELSE comienzo=27:indicador=0
2039   REM dibujo del perro
2040   color=1:GOSUB 3000
2049   REM borrado del perro
2050   color=0:GOSUB 3000
2059   REM mover a la nueva posicion
2060   xinc=xinc+20
2070 WEND
2080 RETURN
2999 REM el perro se dibuja empalmando puntos 
3000 FOR con=comienzo TO comienzo+25 STEP 2 
3010   MOVE x(con)+xinc,y(con)
3020   DRAW x(con+1)+xinc,y(con+1),color
3030 NEXT 
3040 RETURN
