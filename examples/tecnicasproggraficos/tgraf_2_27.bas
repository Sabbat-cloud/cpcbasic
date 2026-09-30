1 REM para aumentar la velocidad
5 DEFINT c,x,y
10 MODE 0
19 REM caracteres mosca y arana
20 SYMBOL 240,0,36,90,90,90,36,0,0
30 SYMBOL 241,145,82,52,31,248,44,74,137
40 mosca$=CHR$(240) 
50 arana$=CHR$(241) 
60 GOSUB 1000
70 xmosca=300:ymosca=200
80 xnuevo=xmosca:ynuevo=ymosca
90 xtest=xmosca:ytest=ymosca
100 MOVE mosca,ymosca:PLOT xmosca,ymosca,1
110 GOSUB 2000
120 respuesta$="":moscamuerta=0
129 REM se leen caracteres del teclado mientras la mosca siga viva
130 WHILE respuesta$="" OR moscamuerta=0 
140   xnuevo=xmosca:ynuevo=ymosca
150   respuesta$=LOWER$(INKEY$)
159   REM la posicion (xtest,ytest) para comprobacion del color depende de la direccion del movimiento
160   IF respuesta$="a" THEN ynuevo=ymosca+2:xtest=xnuevo+16:ytest=ynuevo+8
170   IF respuesta$="z" THEN ynuevo=ymosca-2:xtest=xnuevo+16:ytest=ynuevo-24
180   IF respuesta$="." THEN xnuevo=xmosca+4:xtest=xnuevo+48:ytest=ynuevo-8
190   IF respuesta$="," THEN xnuevo=xmosca-4:xtest=xnuevo-16:ytest=ynuevo-8
200   IF xnuevo<>xmosca OR ynuevo<>ymosca THEN GOSUB 2000
210 WEND
220 MODE 1
230 END
999 REM color rosa
1000 MOVE 0,0
1010 DRAW 0,0,11
1020 TAG
1029 REM dibujar 10 aranas aleatoriamente 
1030 FOR aranas=1 TO 10
1040   xarana=INT(600*RND(1)+20)
1050   yarana=INT(300*RND(1)+20)
1060   MOVE xarana,yarana
1070   PRINT arana$;
1080 NEXT
1090 RETURN
1999 REM se comprueba el color de la siguiente p osicion del caracter
2000 color=TEST(xtest,ytest)
2008 REM si es rosa, muere la mosca
2009 REM no se considera tocar la arana el tocar solo la suprficie
2010 IF color=11 THEN moscamuerta=1:SOUND 7,2000 2019 REM dibujo de la mosca en la nueva posicion 
2020 xmosca=xnuevo:ymosca=ynuevo
2050 MOVE xmosca,ymosca
2060 PRINT mosca$;
2070 RETURN
