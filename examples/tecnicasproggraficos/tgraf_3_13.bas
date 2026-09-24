10 MODE 1
20 GOSUB 1000 
30 GOSUB 2000 
40 GOSUB 3000 
50 END
997 REM leer del DATA las coordenadas del centro y el radio
1000 READ centrox,centroy
1010 READ radio 
1020 READ numdeval
1070 DIM valor(numdeval),angulo(numdeval)
1039 REM sumar todos los valores para calcular 1 as divisiones del circulo
1040 totalvalor=0
1050 FOR con=1 TO numdeval
1060   READ valor(con)
1070   totalvalor=totalvalor+valor(con)
1080 NEXT
1090 RETURN
1100 DATA 200,200,120,4,1,2,7,4
1999 REM calculo del angulo de cada sector 
2000 FOR con=1 TO numdeval
2010   angulo(con)=2*PI*valor(con)/totalvalor 
2020 NEXT
2030 RETURN
3000 REM cambiaremos esto enseguida
3010 comangulo=0
3020 incremento=PI/60
3030 color=1
3039 REM para modo 0 hacer numdecol=15 (sin contar el color del fondo)
3040 numdecol=3
3050 FOR con=1 TO numdeval
3057   REM angulo en que termina el sector 
3060   finangulo=comangulo+angulo(con)
3069   REM color del sector
3070   color=1+(color+1) MOD numdecol
3079   REM asegurarse de que el primero y el ultimo sector son de colores diferentes
3080   IF con=numdeval AND numdeval MOD numdecol=1 THEN color=1+(color+1) MOD numdecol
3090   MOVE centrox,centroy:DRAW centrox+radio*SIN(comangulo),centroy+radio*COS(comangulo),color 
3099   REM dibujo del sector
3100   FOR angulo=comangulo TO finangulo STEP incremento
3110     DRAW centrox+radio*SIN(angulo),centroy+radio*COS(angulo)
3120   NEXT
3129   REM angulo de comienzo del nuevo sector 
3130   comangulo=finangulo
3140 NEXT
3150 RETURN
