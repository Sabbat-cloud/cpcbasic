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

1051 IF respuesta$="d" THEN color=1 
1052 IF respuesta$="f" THEN color=0

35 colorvisible=1
1005 PLOT x,y,color
1060 PLOT x,y,colorvisible

1053 IF respuesta$="c" THEN color=1+(color+1) MOD 3