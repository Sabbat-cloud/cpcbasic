2996 REM 'g' para alargamiento
2997 REM 'p' para reduccion
3050 IF respuesta$="g" THEN GOSUB 6000
3060 IF respuesta$="p" THEN GOSUB 6100
5995 REM rutina de alargamiento o reduccion a escala
5996 REM el centro se selecciona con a/z/,/. y se fija
6010 GOTO 6200
6098 REM esta es la rutina de reduccion
6099 REM reduccion a escala 0.9 en ambos ejes; cambie el coeficiente si lo desea
6100 escalax=0.9:escalay=0.9
6199 REM fijacion del centro de alargamiento/reduccion
6200 GOSUB 15000
6299 REM borra la figura anterior
6310 GOSUB 2000
6399 REM coeficientes de la transformacion
6400 xtrans1=escalax:ytrans2=escalay:xtrans2=0:ytrans1=0
6499 REM calcula la figura transformada
6500 GOSUB 12000
6599 REM dibuja la figura transformada
6600 GOSUB 2000
6699 respuesta$=""
6700 RETURN
