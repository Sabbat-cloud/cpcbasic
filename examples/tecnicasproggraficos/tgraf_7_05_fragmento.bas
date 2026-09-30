2998 REM 'f' para reflexion
3070 IF respuesta$="f" THEN GOSUB 7000
6995 REM rutina de reflexion sobre un eje
6996 REM la reflexion es sobre un eje vertical o sobre un eje horizontal
6997 REM que pasan por el punto que se desee 
6998 REM el punto se selecciona con a/z/,/. y se fija
6999 REM al pulsar 'x' o 'y' , lo que selecciona ademas el eje
7000 GOSUB 16000
7099 REM coeficientes de la transformacion
7100 IF respuesta$="x" THEN xtrans1=1:ytrans2=-1 :xtrans2=0:ytrans1=0 ELSE xtrans1=-1:ytrans2=1:xtrans2=0:ytrans1=0
7199 REM borra la figura anterior
7200 GOSUB 2000
7299 REM calcula la figura transformada
7300 GOSUB 12000
7399 REM dibujo de la figura reflejada
7400 GOSUB 2000
7499 respuesta$=""
7500 RETURN
15999 REM rutina de fijacion de un centro y un eje de la transformacion
16000 TAG
16004 REM correcciones para centrar un caracter en un punto; la izquierda debe ser 8 en modo 0 y 4 en modo 1
16005 correccionizquierda=2:correccionarriba=4 
16010 MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
16100 WHILE respuesta$<>"x" AND respuesta$<>"y" 
16110   respuesta$=LOWER$(INKEY$)
16115   xinc=0:yinc=0
16120   IF respuesta$="a" THEN yinc=2:respuesta$="":GOSUB 16500
16130   IF respuesta$="z" THEN yinc=-2:respuesta$="":GOSUB 16500
16140   IF respuesta$="," THEN xinc=-4:respuesta$="":GOSUB 16500
16150   IF respuesta$="." THEN xinc=4:respuesta$="":GOSUB 16500
16200 WEND
16220 MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
16230 RETURN
16499 REM borrar antiguo centro y dibujar el nue vo
16500 REM
16510 MOVE xcentro-correccionizquierda,yce ntro+correccionarriba:PRINT CHR$(129);:xcentro=xcentro+xinc:ycentro=ycentro+yinc:MOVE xcentro-correccionizquierda,ycentro+correccionarriba:PRINT CHR$(129);
16600 RETURN