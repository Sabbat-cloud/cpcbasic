120 respuesta$="":moscamuerta=0
126 REM ahora hay que alcanzar con la mosca. la e squina superior izquierda
127 REM lo mas rapidamente posible, puesto que c uenta el tiempo,
128 tiempoinicial=TIME
129 REM se leen caracteres del teclado mientras la mosca siga viva y no se alcance la esquina
130 WHILE (respuesta$="" OR moscamuerta=0) AND (xmosca<600 OR ymosca<300)
140   xnuevo=xmosca:ynuevo=ymosca
150   respuesta$=LOWER$(INKEY$)
159   REM la posicion (xtest,ytest) para comprobacion del color depende de la direccion del movimiento
160   IF respuesta$="a" THEN ynuevo=ymosca+2:xtest=xnuevo+16:ytest=ynuevo+8
170   IF respuesta$="z" THEN ynuevo=ymosca-2:xtest=xnuevo+16:ytest=ynuevo-24
180   IF respuesta$="." THEN xnuevo=xmosca+4:xtest=xnuevo+48:ytest=ynuevo-8
190   IF respuesta$="," THEN xnuevo=xmosca-4:xtest=xnuevo-16:ytest=ynuevo-8
200   IF xnuevo<>xmosca OR ynuevo<>ymosca THEN GOSUB 2000
210 WEND
215 TAGOFF:CLS
220 IF moscamuerta=0 THEN PRINT "Tiempo: "TIME-tiempoinicial
230 END
