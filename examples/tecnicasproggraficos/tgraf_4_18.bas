10 MODE 0
20 x=320:y=200
30 color=1
40 MOVE x,y
50 PLOT x,y,color
60 GOSUB 1000
70 END
997 REM examen del teclado - fin cuando se pulsa la tecla 'e'
1000 WHILE respuesta$<>"e"
1010 respuesta$=INKEY$
1019 REM comandos para dibujar la linea:	arriba/abajo=a/z	izquierda/derecha=,/.
1020 IF respuesta$="a" THEN y=y+2
1030 IF respuesta$="z" THEN y=y-2
1040 IF respuesta$="," THEN x=x-4
1050 IF respuesta$="." THEN x=x+4
1060 PLOT x,y,color
1070 WEND
1080 RETURN
