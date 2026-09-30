10 MODE 1
20 GOSUB 1000 
30 GOSUB 2000 
40 GOSUB 3000 
50 END
999 REM muchas variables pueden ser enteras - esto aumenta la velocidad
1000 DEFINT a,c,n,r,v
1005 READ centrox,centroy
1010 READ radio 
1020 READ numdeval
1030 DIM valor(numdeval),angulo(numdeval)
1039 REM sumar todos los valores para calcular las divisiones del circulo
1040 totalvalor=0
1050 FOR con=1 TO numdeval
1060   READ valor(con)
1070   totalvalor=totalvalor+valor(con)
1080 NEXT
1090 RETURN
1100 DATA 200,200,120,4,1,2,3,4
1998 REM radval influye en la velocidad del dibujo y en la densidad del rellenado
1999 REM si se toma radio*3 mejora la velocidad aunque quedan puntos sin rellenar
2000 radval=radio*10
2001 totangulo=0
2005 FOR con=1 TO numdeval
2010   angulo(con)=radval*valor(con)/totalvalor
2015   totangulo=totangulo+angulo(con)
2020 NEXT
2030 RETURN
3000 ORIGIN centrox,centroy
3010 DEFINT c 
3020 contangulo=0
3030 color=1
3033 REM solo se necesita calcular un seno y un coseno por este metodo
3034 REM esto da mas velocidad
3035 elseno=SIN(2*PI/radval):elcoseno=COS(2*PI/radval)
3036 x1=radio:y1=0
3037 REM calculo de las coordenadas de los punto s de la circunferencia
3038 LOCATE 5,10:PRINT "espere, por favor":GOSUB 4000:CLS
3039 REM para modo 0 hacer numdecol=15 (sin cont ar el color del fondo)
3040 numdecol=3
3050 FOR con=1 TO numdeval
3069   REM color del sector
3070   color=1+(color+1)MOD numdecol
3079   REM asegurarse de que el primero y el ultim o sector son de colores diferentes
3080   IF con=numdeval AND numdeval MOD numdecol=1 THEN color=1+(color+1)MOD numdecol
3090   REM
3099   REM dibujo del sector
3100   FOR con1=contangulo TO contangulo+angulo(con)
3114     MOVE 0,0:DRAW x(con1),y(con1),color 
3120   NEXT
3124   REM posicion inicial del siguiente sector 
3125   contangulo=contangulo+angulo(con)
3140 NEXT
3150 RETURN
3997 REM normalmente convendra realizar este calculo en los programas largos
3998 REM en algun momento del programa en el que la espera
3999 REM no resulte excesivamente larga
4000 DIM x(totangulo),y(totangulo)
4010 FOR con=1 TO totangulo
4020   x=x1*elcoseno-y1*elseno
4030   y=x1*elseno+y1*elcoseno
4040   x(con)=x
4050   y(con)=y
4060   x1=x:y1=y
4070 NEXT
4080 RETURN
