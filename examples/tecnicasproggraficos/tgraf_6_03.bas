1 REM este es un programa independiente
2 REM pero las subrutinas
3 REM están preparadas para ser incorporadas al programa principal
10 MODE 0
19 REM dibujo de un triangulo para que sirva de ejemplo
20 MOVE 200,100 
30 DRAW 450,350 
40 DRAW 340,400 
50 DRAW 200,100
54 REM se eligen 10 puntos al azar para rellenar rectas partiendo de ellos
55 FOR con=1 TO 10
59   REM punto al azar dentro del triangulo
60   rand=INT(RND(1)*230):xarranque=210+rand:yarranque=110+rand
70   colorvisible=1:yrell=yarranque
79   REM relleno a la izquierda del punto
80   xinc=-4:xrell=xarranque
90   GOSUB 18000
98   REM ahora a la derecha, pero no se empieza por
99   REM el propio punto sino por el que esta a su izquierda
100   xinc=4:xrell=xarranque-4
110   GOSUB 18000
120 NEXT
130 END
17999 REM comprobar punto por.punto a izquierda o derecha
18000 t=0:WHILE t=0
18010   xrell=xrell+xinc
18020   t=TEST(xrell,yrell)
18028   REM si t=0 es punto es del color del fondo 
18029   REM y hay que dibujarlo
18030   IF t=0 THEN PLOT xrell,yrell,colorvisible 
18040 WEND
18050 RETURN
