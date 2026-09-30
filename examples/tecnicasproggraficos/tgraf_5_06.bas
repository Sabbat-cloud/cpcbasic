10 MODE 1
14 REM para mayor velocidad se utilizan numeros enteros
15 DEFINT c,s,t,x,y
20 GOSUB 1000
30 GOSUB 2000
40 PRINT CHR$(23)CHR$(0);
50 END
998 REM lectura en dos conjuntos de 26 coordenadas
999 REM para dibujar dos posiciones diferentes d el perro
1000 DIM x(100),y(100)
1010 FOR con=1 TO 52
1020   READ x(con),y(con)
1030 NEXT
1040 RETURN
1050 DATA 0,0,20,40,20,40,10,80,10,80,0,120,20,10,35,50,35,50,10,80,10,80,70,80
1060 DATA 60,0,80,40,80,40,70,80,80,10,95,50,95,50,70,80,70,80,90,140,90,140,110,120,110,120,80, 110
1070 DATA 5,10,25,40,25,40,15,80,15,80,10,120,0,15,30,50,30,50,15,80,15,80,75,80
1080 DATA 75,80,85,40,85,40,65,10,75,80,90,50,90,50,60,15,75,80,100,130,100,130,120,110,120,110, 90,100
1999 REM la tinta 3 con el color que interesa para XOR
2000 INK 3,24
2010 color=1:color1=24
2020 tipo=3:tono=1
2029 REM dibujo de la figura en la posicion inicial
2030 GOSUB 4000
2040 GOSUB 5000
2050 tipo=3:tono=2
2060 xinc=0
2070 WHILE x(1)+xinc<639
2079   REM se actualiza xinc para la nueva figura 
2080   xinc=xinc+20
2089   REM dibujo de la nueva figura en el color del fondo
2090   GOSUB 5000
2099   REM conmutacion de las tintas
2100   GOSUB 4000
2109   REM se borra la figura previa cuándo esta del color del fondo
2110   xinc=xinc-20
2120   GOSUB 5000
2129   REM se actualiza xinc para la figura actual 
2130   xinc=xinc+20
2140   IF tono=2 THEN tono=1 ELSE tono=2
2150 WEND
2160 RETURN
2999 REM el perro se dibuja empalmando puntos 
3000 FOR con=comienzo TO comienzo+25 STEP 2 
3010   MOVE x(con)+xinc,y(con)
3020   DRAW x(con+1)+xinc,y(con+1),tono
3030 NEXT
3040 RETURN
3999 REM conmutacion de colores
4000 IF color=1 THEN color=24:color1=1 ELSE color=1:color1=24
4010 INK 1,color
4020 INK 2,color1
4030 RETURN
4999 REM cambio del modo grafico entre dibujo y borrado
5000 PRINT CHR$(23)CHR$(tipo);
5010 IF tipo+tono=4 THEN comienzo=1 ELSE comienzo=27
5020 GOSUB 3000
5030 IF tipo=2 THEN tipo=3 ELSE tipo=2
5040 RETURN
