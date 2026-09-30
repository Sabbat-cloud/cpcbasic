2000 radval=radio*4
2005 FOR con=1 TO numdeval
2010   angulo(con)=radval*valor(con)/totalvalor 
2020 NEXT
2030 RETURN
3000 ORIGIN centrox,centroy
3009 REM al emplear enteros en el bucle aumenta la velocidad
3010 DEFINT c
3030 color=1
3035 elseno=SIN(2*PI/radval):elcoseno=COS(2*PI/radval)
3037 x1=radio:y1=0
3039 REM para modo 0 hacer numdecol=15 (sin cont ar el color del fondo)
3040 numdecol=3
3050 FOR con=1 TO numdeval
3069   REM color del sector
3070   color=1+(color+1) MOD numdecol
3079   REM asegurarse de que el primero y el ultim o sector son de colores diferentes
3080   IF con=numdeval AND numdeval MOD numdecol=1 THEN color=1+(color+1) MOD numdecol
3090   REM
3099   REM dibujo del sector
3100   FOR con1=1 TO angulo(con)
3110     x=x1*elcoseno-y1*elseno
3112     y=x1*elseno+y1*elcoseno
3114     PLOT x,y,color
3116     x1=x:y1=y
3120   NEXT
3129   REM trazar la linea hasta el centro para es te sector
3130   MOVE 0,0:DRAW x,y
3140 NEXT
3150 RETURN
