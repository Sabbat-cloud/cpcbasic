30 xcentro=320:ycentro=200
4996 REM el centro de la rotacion se selecciona con a/z/,/. y se fija
4997 REM pulsando la tecla de espacio
5099 REM fijacion del centro de la rotacion 
5100 GOSUB 15000
5500 GOSUB 12000
11999 REM rutina para transformar las coordenadas de la figura por cualquier transformacion matricial con centro arbitrario
12000 xinc=-xcentro:yinc=-ycentro
12010 FOR con=0 TO numdelin
12020   x=x(con):y=y(con):GOSUB 10000:x(con)=x:y(con)=y
12030 NEXT
12040 GOSUB 11000
12050 xinc=xcentro:yinc=ycentro
12060 FOR con=0 TO numdelin
12070   x=x(con):y=y(con):GOSUB 10000:x(con)=x:y(con)=y
12090 NEXT
12100 RETURN
14999 REM rutina de fijacion de un centro de la transformacion
15000 TAG
15004 REM correcciones para centrar un caracter en un punto; la izquierda debe ser 8 en modo 0 y 4 en modo 1
15005 correccionizquierda=2:correccionarriba=4 
15010 MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
15100 WHILE respuesta$<>" "
15110   respuesta$=LOWER$(INKEY$)
15115   xinc=0:yinc=0
15120   IF respuesta$="a" THEN yinc=2:respuesta$="":GOSUB 15500
15130   IF respuesta$="z" THEN yinc=-2:respuesta$="":GOSUB 15500
15140   IF respuesta$="," THEN xinc=-4:respuesta$="":GOSUB 15500
15150   IF respuesta$="." THEN xinc=4:respuesta$="":GOSUB 15500
15200 WEND
15210 respuesta$=""
15220 MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
15230 RETURN
15499 REM borrar antiguo centro y dibujar el nuevo
15500 REM
15510 MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);:xcentro=xcentro+xinc:ycentro=ycentro+yinc:MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
15600 RETURN
