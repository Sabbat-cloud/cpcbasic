19 REM rectangulo con un brazo vertical
20 xact=150:yact=150
30 MOVE xact,yact 
40 DRAWR 100,0 
50 DRAWR 0,100
55 DRAWR -10,0
56 DRAWR 0,50
57 DRAWR -60,0
58 DRAWR 0,-50 
60 DRAWR -30,0 
70 DRAWR 0,-100
16000 xactual=xrell:yactual=yrell
16010 IF TEST(xrell,yrell)<>0 THEN RETURN
16020 zinc=-4
16029 REM comprobacíon del color de los puntos de la izquierda
16030 GOSUB 18000
16031 REM coordenadas del extremo izquierdo de la linea
16032 xizq=xrell
16040 xrell=xactual-4:yrell=yactual
16049 REM comprobacion del color de los puntos de la derecha
16050 xinc=4 16060 GOSUB 18000
16061 REM coordenadas del extremo derecho de la linea
16062 xder=xrell
16063 REM calcular el punto medio de la linea 
16064 REM y comprobar el color de los puntos de arriba y abajo
16065 xrell=(xizq+xder)/2:yrell=yactual-2
16066 IF TEST(xrell,yrell)=0 THEN GOSUB 19000 
16067 yrell=yactual+2
16068 IF TEST(xrell,yrell)=0 THEN GOSUB 19000 
16069 REM no es perfecto pero es rapido
16070 RETURN
