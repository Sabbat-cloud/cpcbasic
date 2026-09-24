10 MODE 1
20 GOSUB 1000
30 GOSUB 1500
40 END
999 REM lectura de los datos del poligono 
1000 READ lados
1010 READ radio
1020 READ centrox,centroy
1030 READ radiocambio,angulocambio
1040 color=2
1050 paso=2*PI/lados
1060 angulocom=0:angulofin=2*PI
1070 RETURN
1500 ORIGIN centrox,centroy
1508 REM no se dibuja el poligono cuando se hace demasiado grande
1509 REM lo que significa radio>200 para los poligonos de los DATA
1510 WHILE radio<200
1520   MOVE radio*SIN(angulocom),radio*COS(angulocom)
1530   FOR angulo=angulocom TO angulofin STEP paso 
1540     DRAW radio*SIN(angulo),radio*COS(angulo),color
1550   NEXT
1560   DRAW radio*SIN(angulocom),radio*COS(angulocom)
1569   REM se incrementa el radio
1570   radio=radio+radiocambio
1579   REM se gira el siguiente poligono para que forme angulo con el anterior
1580   angulocom=angulocom+angulocambio
1590   angulofin=angulofin+angulocambio
1600 WEND
1610 RETURN
2000 DATA 3,20,300,200,5,1 
2010 DATA 3,20,300,200,3,10 
2020 DATA 4,30,300,200,4,3 
2030 DATA 6,20,300,200,1,6 
2040 DATA 6,20,300,200,6,1 
2050 DATA 8,10,300,200,5,10 
2060 DATA 8,10,300,200,5,2
