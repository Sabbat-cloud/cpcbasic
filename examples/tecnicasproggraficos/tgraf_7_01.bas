10 MODE 2
20 DIM x(100),y(100),z(100)
69 REM cargar la figura
70 GOSUB 1000
74 REM modalidad grafica
75 PRINT CHR$(23)CHR$(1);
79 REM dibujar la figura
80 GOSUB 2000
89 REM opcion
90 GOSUB 3000
800 MODE 1
900 END
999 REM lectura de los datos de la figura
1000 READ numdelin
1010 FOR con=0 TO numdelin 
1020   READ x(con),y(con),l(con) 
1030 NEXT
1040 RETURN
1498 REM en nuestro ejemplo es un hexagono
1499 REM sustituya la figura y sus datos por los que usted desee
1500 DATA 6,300,100,0,400,100,1,490,190,1,400,290,1,300,280,1,210,190,1,300,100,1
1999 REM rutina de dibujar/borrar
2000 MOVE x(0),y(0)
2010 FOR con=1 TO numdelin
2020   IF l(con)>0 THEN DRAW x(con),y(con) ELSE MOVE x(con),y(con)
2030 NEXT
2040 RETURN
2993 REM rutina de seleccion de la opcion; 'e' para terminar
2994 REM 't' para la traslacion
3000 respuesta$=""
3010 WHILE respuesta$<>"e"
3020   respuesta$=LOWER$(INKEY$)
3030   IF respuesta$="t" THEN GOSUB 4000
3500 WEND
3510 RETURN
3997 REM rutina de traslacion
3999 REM la traslacion se realiza con las teclas a/z/,/. y
3999 REM la figura trasladada se fija pulsando la tecla de espacio
4000 WHILE respuesta$<>" "
4005   respuesta$=LOWER$(INKEY$)
4010   xinc=0:yinc=0
4020   IF respuesta$="a" THEN yinc=2:respuesta$="":GOSUB 4500
4030   IF respuesta$="z" THEN yinc=-2:respuesta$="":GOSUB 4500
4040   IF respuesta$="," THEN xinc=-4:respuesta$="":GOSUB 4500
4050   IF respuesta$="." THEN xinc=4:respuesta$ ="":GOSUB 4500
4100 WEND
4110 respuesta$=""
4120 RETURN
4499 REM efectua la traslacion
4500 GOSUB 2000
4510 FOR con=0 TO numdelin
4520   x=x(con):y=y(con):GOSUB 10000:x(con)=x:y(con)=y
4530 NEXT
4540 GOSUB 2000
4550 RETURN
9999 REM cambio de datos por traslacion
10000 x=x+xinc:y=y+yinc
10010 RETURN
