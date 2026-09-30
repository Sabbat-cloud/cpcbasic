4999 REM comprobacion de la eleccion circ/rectangulo/triangulo.
5000 PRINT CHR$(23)CHR$(0);
5001 IF circ>0 THEN GOSUB 8000
5002 IF rectangulo>0 THEN GOSUB 9000
5003 IF triangulo>0 THEN GOSUB 10000
5010 GOSUB 3000
5020 PRINT CHR$(23)CHR$(1);
5030 xant=x:yant=y
5700 RETURN
5999 REM elegir opcion del menu; se rechaza si no esta en el menu
6000 IF x<128 OR x>543 OR y<16 THEN RETURN 
6010 SOUND 7,400
6019 REM x<784 significa que la opcion es un cambio de color
6020 IF x<384 THEN colorvisible=TEST(x,y):GOSUB 7000:RETURN
6029 REM deducir opcion segun sea la coordenada
6030 IF x<416 THEN info$=CHR$(47):GOSUB 7000:RETURN
6040 IF x<448 THEN info$=CHR$(79):GOSUB 7000:circ=1:RETURN
6050 IF x<490 THEN info$=CHR$(232):GOSUB 7000:rectangulo=1:RETURN
6060 IF x<512 THEN info$=CHR$(240):GOSUB 7000:triangulo=1:RETURN
6069 REM debe ser la opcion de conmutar relleno/no relleno
6070 GOSUB 15000
6080 RETURN
7000 PEN colorvisible
7010 LOCATE 1,24
7020 PRINT info$
7025 IF x<384 THEN RETURN
7029 REM opcion anulada; nueva eleccion
7030 circ=0
7040 triangulo=0 
7050 rectangulo=0 
7060 RETURN
7999 REM dibujo de la circunferencia: se requiere el centro y un punto de la circunferencia
8000 IF circ=1 THEN circ=2:RETURN
8009 REM ahora tenemos los dos puntos y podemos calcular el radio
8010 xd=ABS(x-xant):yd=ABS(y-yant)
8020 radio=SQR(xd*xd+yd*yd)
8030 MOVE xant,yant+radio
8040 FOR angulo=0 TO 2*PI STEP PI/60
8050   DRAW xant+radio*SIN(angulo),yant+radio*COS(angulo)
8060 NEXT
8070 DRAW xant,yant+radio
8080 PLOT xant,yant,0
8089 REM poner el indicador de circ a 1 para la siguiente circunferencia 
8090 circ=1
8100 RETURN
8999 REM rutina de dibujo del rectangulo; se requieren dos vertices
9000 IF rectangulo=1 THEN rectangulo=2:RETURN 
9010 MOVE xant,yant
9020 DRAWR x-xant,0,colorvisible
9030 DRAWR 0,y-yant 
9040 DRAWR xant-x,0 
9050 DRAWR 0,yant-y
9059 REM poner el indicador rectangulo a 1 para el rectangulo siguiente
9060 rectangulo=1 
9070 RETURN
9999 REM rutina de dibujo del triangulo; se nece sitan los tres vertices
10000 IF triangulo=1 THEN triangulo=2:x1=x:y1=y:RETURN
10010 IF triangulo=2 THEN triangulo=3:RETURN 
10020 MOVE x,y
10030 DRAW xant,yant,colorvisible
10040 DRAW x1,y1
10050 DRAW x,y
10059 REM poner el indicador triangulo a 1 para el siguiente triangulo
10060 triangulo=1
10070 RETURN
15000 REM a completar despues
15010 RETURN
