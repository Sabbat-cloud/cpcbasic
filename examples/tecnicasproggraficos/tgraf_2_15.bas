10 MODE 1
20 DEFINT c,n,x,y
29 REM matrices para almacenar la definicion del caracter
30 DIM codigo(8,8),simbolo(8)
40 INK 3,20,6
50 nombre$= "??????"
60 numero=240
69 REM
70 GOSUB 1000
80 GOSUB 3000:GOSUB 4000
89 REM esperar la respuesta del teclado
90 respuesta$=""
100 WHILE respuesta$<>"e" AND respuesta$<>"E"
110 xnuevo=x:ynuevo=y
120 respuesta$=INKEY$
129 REM las cuatro lineas siguientes controlan el movimiento del cursor arriba/abajo/izquierda/derecha
130 IF (respuesta$="a" OR respuesta$="A") AND y>ycomienzo THEN ynuevo=y-1
140 IF (respuesta$="z" OR respuesta$="Z") AND y<ycomienzo+7 THEN ynuevo=y+1
150 IF respuesta$="," AND x>xcomienzo THEN xnuevo=x-1
160 IF respuesta$="." AND x<xcomienzo+7 THEN xnuevo=x+1
169 REM se rectifica la posicion si ha cambiado
170 IF xnuevo<>x OR ynuevo<>y THEN GOSUB 2000
179 REM si se aprieta la barra de espacio cambia el color del punto
180 IF respuesta$=" " THEN GOSUB 7000:GOSUB 3000
189 REM si se pulsa 'o' se graba la definicion del simbolo en un fichero
190 IF respuesta$="o" THEN GOSUB 5000:GOSUB 1000:GOSUB 3000:GOSUB 4000
199 REM si se pulsa 'i' se carga la definicion del simbolo desde la cinta
200 IF respuesta$="i" THEN GOSUB 6000:GOSUB 3000:GOSUB 4000
210 PEN 14
220 LOCATE x,y
230 PRINT CHR$(203);
240 WEND
250 END
999 REM definicion del simbolo vacio
1000 CLS
1010 SYMBOL numero,0,0,0,0,0,0,0,0
1020 PEN 1
1030 FOR con=1 TO 8
1040   FOR con1=1 TO 8
1050     codigo(con,con1)=1
1060   NEXT
1070 NEXT
1079 REM impresion de 8*8 cuadrados vacios para representar el caracter 'espacio en blanco'
1080 xcomienzo=2:ycomienzo=2
1090 FOR x=xcomienzo TO xcomienzo+7
1100   FOR y=ycomienzo TO ycomienzo+7
1110     LOCATE x,y
1120     PRINT CHR$(233);
1130   NEXT
1140 NEXT
1150 x=xcomienzo:y=ycomienzo
1160 RETURN
1999 REM impresion del caracter con su color correcto
2000 LOCATE x,y
2010 xcodigo=x-xcomienzo+1:ycodigo=y-ycomienzo+1
2020 PEN codigo(xcodigo,ycodigo)
2030 PRINT CHR$(233);
2040 x=xnuevo:y=ynuevo
2050 RETURN
2999 REM conversion de la matriz codigo en los ocho numeros decimales que definen el caracter
3000 FOR con=1 TO 8
3010   simbolo$="&X"
3020   FOR con1=1 TO 8
3030     simbolo$=simbolo$+MID$(STR$(codigo(con1,con)-1),2,1)
3040   NEXT
3050   simbolo(con)=VAL(simbolo$)
3060 NEXT
3070 SYMBOL numero,simbolo(1),simbolo(2),simbolo(3),simbolo(4),simbolo(5),simbolo(6),simbolo(7),simbolo(8)
3080 PEN 1
3090 LOCATE 1,ycomienzo+10
3100 PRINT "Simbolo: ";CHR$(numero);
3110 LOCATE 1,ycomienzo+12
3120 PRINT "SYMBOL ";numero;simbolo(1);simbolo(2);simbolo(3);simbolo(4);simbolo(5);simbolo(6);simbolo(7);simbolo(8);
3130 RETURN
4000 PEN 1
4010 LOCATE 1,ycomienzo+15
4020 PRINT "Nombre del simbolo: ";nombre$
4030 LOCATE 1,ycomienzo+17
4040 PRINT "Simbolo numero: ";numero
4050 RETURN
4999 REM grabar la definicion en un fichero
5000 LOCATE 1,21
5010 PEN 1
5020 INPUT "Nombre del simbolo";nombre$
5030 OPENOUT nombre$
5040 WRITE #9,nombre$,numero,simbolo(1),simbolo(2),simbolo(3),simbolo(4),simbolo(5),simbolo(6),simbolo(7),simbolo(8)
5050 CLOSEOUT
5059 REM nombre y numero de simbolo para la siguiente definicion
5060 nombre$="??????"
5070 numero=numero+1
5080 RETURN
5999 REM lectura del fichero con la definicion del caracter
6000 LOCATE 1,21
6010 PEN 1
6020 INPUT "Nombre del simbolo";nombre$
6030 OPENIN nombre$
6040 INPUT #9,nombre$,numero,simbolo(1),simbolo(2),simbolo(3),simbolo(4),simbolo(5),simbolo(6),simbolo(7),simbolo(8)
6050 CLOSEIN
6060 CLS
6069 REM conversion a binario de la matriz simbolo para obtener la matriz codigo
6070 FOR con=1 TO 8
6080   simbolo$=BIN$(simbolo(con))
6090   longitud=LEN(simbolo$)
6100   simbolo$=STRING$(8-longitud,"0")+simbolo$
6110   FOR con1=1 TO 8
6120     LOCATE xcomienzo+con1-1,ycomienzo+con-1
6130     codigo=VAL(MID$(simbolo$,con1,1))+1
6140     PEN codigo
6150     PRINT CHR$(233);
6160     codigo(con1,con)=codigo
6170   NEXT
6180 NEXT
6190 RETURN
6999 REM si se aprieta la barra de espacio cambia el color en la posicion del cursor
7000 xcodigo=x-xcomienzo+1:ycodigo=y-ycomienzo+1
7010 IF codigo(xcodigo,ycodigo)=1 THEN codigo(xcodigo,ycodigo)=2 ELSE codigo(xcodigo,ycodigo)=1
7020 RETURN
