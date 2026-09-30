10 MODE 1
20 GOSUB 1000
100 END
1000 xorigen=315:yorigen=190
1010 ORIGIN xorigen,yorigen
1020 color=1
1029 REM valor del incremento del radio de la espiral cada vez que se dibuja un nuevo punto
1030 radioincremento=0.5
1040 paso=PI/30
1049 REM angulofinal determina las vueltas que dara la espiral
1049 REM un valor excesivo hace que se salga de la pantalla
1050 angulofinal=40
1059 REM se comienza con radio 1
1060 radiocom=1 
1070 GOSUB 2000 
1900 RETURN
2000 MOVE 0,0
2010 FOR angulo=0 TO angulofinal STEP paso
2020   DRAW radiocom*SIN(angulo),radiocom*COS(angulo),color
2030   radiocom=radiocom+radioincremento
2040 NEXT
2050 RETURN
