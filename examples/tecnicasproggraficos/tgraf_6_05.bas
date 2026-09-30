10 MODE 0
14 REM matrices para las coordenadas de los punt os no coloreados
15 DIM x(300),y(300)
19 REM aqui pude icorporar su propia figura de p rueba
20 xant=150:yant=150 
30 MOVE xant,yant 
40 DRAWR 100,0 
50 DRAWR 0,100 
60 DRAWR -100,0 
70 DRAWR 0,-100
78 REM x e y son las coordenadas de un punto
79 REM de dentro de la figura
80 x=200:y=200
90 colorvisible=1 
100 GOSUB 15000
110 PRINT CHR$(23)CHR$(0);
999 END
15000 comienzo=2:final=1
15010 xrell=x:yrell=y 
15020 x(2)=x:y(2)=y
15030 PRINT CHR$(23)CHR$(0);
15040 PLOT x,y,0 
15050 GOSUB 16000 
15060 GOSUB 17000
15070 PRINT CHR$(23)CHR$(1);
15080 IF circ>0 OR rectangulo>0 OR triangulo>0 THEN PLOT x,y,colorvisible
15090 RETURN
15999 REM comprobar el color del punto
16000 xactual=xrell:yactual=yrell
16010 IF TEST(xrell,yrell)<>0 THEN RETURN
16020 xinc=-4
16029 REM comprobacion del color de los puntos de la izquierda
16030 GOSUB 18000
16040 xrell=xactual-4:yrell=yactual
16049 REM comprobacion del color de los puntos de la derecha
16050 xinc=4 
16060 GOSUB 18000
16070 RETURN
16999 REM se toman puntos de la lista mientras haya
17000 WHILE comienzo<>(final+1) MOD 300
17010   xrell=x(comienzo):yrell=y(comienzo)
17020   comienzo=(comienzo+1) MOD 300
17030   GOSUB 16000
17040 WEND 
17050 RETURN
17999 REM comprobacion punto por punto a izquierda o derecha
18000 t=0:WHILE t=0
18010   xrell=xrell+xinc
18020   t=TEST(xrell,yrell)
18030   IF t=0 THEN PLOT xrell,yrell,colorvisible 
18040 WEND
18050 xrell=xrell-xinc:yrell=yrell-2
18059 REM si el punto de la linea de abajo no esta coloreado, se almacena
18060 IF TEST(xrell,yrell)=0 THEN GOSUB 19000 
18070 yrell=yrell+4
18079 REM si el punto de la linea de arriba no esta coloreado, se almacena
18080 IF TEST(xrell,yrell)=0 THEN GOSUB 19000 
18090 RETURN
18999 REM almacenamiento de las coordenadas del punto no coloreado
19000 final=(final+1) MOD 300
19010 x(final)=xrell:y(final)=yrell
19020 RETURN
