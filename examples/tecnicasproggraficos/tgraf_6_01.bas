10 MODE 0
20 GOSUB 1000
30 GOSUB 2000
40 END
1000 xant=320:yant=200
1010 x=xant:y=yant
1020 colorvisible=1
1030 lineadib=0
1037 REM imprimir el simbolo de la esquina inferior izquierda
1038 REM para que se tenga a la vista la situacion actual
1039 REM info$ es una linea amarilla al principio, que es la opcion de entrada
1040 info$=CHR$(47)
1050 LOCATE 1,24
1060 PRINT info$;
1070 menux=5:menuy=24
1079 REM definir simbolo para triangulo y para relleno/no relleno
1080 SYMBOL 240,0,2,6,10,18,34,66,254
1090 SYMBOL 241,255,129,129,129,129,129,129,255 
1099 REM dibujar muestras de color de las tintas 0 a 7
1100 LOCATE menux,menuy
1110 PRINT CHR$(241);
1120 FOR color=1 TO 7
1130   PEN color
1140   PRINT CHR$(143);
1150 NEXT
1160 PEN 1
1169 REM dibujar simbolos de linea,circunferencia,rectangulo,triangulo y no relleno
1170 PRINT CHR$(47)CHR$(79)CHR$(232)CHR$(240)CHR$(241);
1180 PRINT CHR$(23)CHR$(1);
1900 RETURN
1999 REM cursor a la posicion inicial 
2000 GOSUB 3000
2009 REM repetir hasta que se pulse 'e' 
2010 WHILE respuesta$<>"e"
2019   REM borrar el cursor con XOR 
2020   GOSUB 3000
2029   REM leer la entrada del teclado 
2030   GOSUB 4000
2039   REM dibujar el cursor
2040   GOSUB 3000
2900 WEND
2910 RETURN
2999 REM rutina de dibujo/borrado de lineas
3000 PLOT x,y,colorvisible
3010 IF lineadib=0 THEN RETURN 
3020 DRAW xant,yant
3030 RETURN
3999 REM rutina para examinar el teclado y tomar la decision apropiada
4000 respuesta$=LOWER$(INKEY$) 
4010 IF respuesta$="a" THEN y=y+2 
4020 IF respuesta$="z" THEN y=y-2
4030 IF respuesta$="," THEN x=x-4 
4040 IF respuesta$="." THEN x=x+4
4048 REM la barra de espacio fija el punto
4049 REM si la coordenada y corresponde a la zona de dibujo
4050 IF respuesta$=" " AND y>31 THEN GOSUB 5000: lineadib=colorvisible
4059 REM si no, la barra de espacio selecciona opcion del menu
4060 IF respuesta$=" " AND y<32 THEN GOSUB 6000 
4069 REM conmutar entre si/no el dibujo de la li nea
4070 IF respuesta$="1" THEN IF lineadib=0 THEN lineadib=colorvisible ELSE lineadib=0
4900 RETURN
4999 REM dibujar de manera permanente una linea 
5000 PRINT CHR$(23)CHR$(0);
5010 GOSUB 3000
5020 PRINT CHR$(23)CHR$(1):
5030 xant=x:yant=y
5900 RETURN
5999 REM elegir opcion del menu; se rechaza si no esta en el menu
6000 IF x<128 OR x>543 OR y<16 THEN RETURN 
6010 SOUND 7,400
6019 REM x<384 significa que la opcion es un cambio de color
6020 IF x<384 THEN colorvisible=TEST(x,y):GOSUB 7000:RETURN
6029 REM deducir opcion segun sea la coordenada
6030 IF x<416 THEN info$=CHR$(47):GOSUB 7000:RETURN
6040 IF x<448 THEN info$=CHR$(79):GOSUB 7000:RETURN
6050 IF X<480 THEN info$=CHR$(232):GOSUB 7000:RETURN
6060 IF x<512 THEN info$=CHR$(240):GOSUB 7000:RETURN
6069 REM debe ser la opcion de conmutar relleno/no relleno
6070 GOSUB 15000
6080 RETURN
7000 PEN colorvisible
7010 LOCATE 1,24
7020 PRINT info$
7030 RETURN
15000 REM a completar despues
15010 RETURN
