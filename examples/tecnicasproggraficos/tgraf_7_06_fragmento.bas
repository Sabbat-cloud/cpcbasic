2999 REM 'c.' para cizallamiento
3080 IF respuesta$="c" THEN GOSUB 8000
7995 REM rutina de cizallamiento en la direccion de un eje
7996 REM el eje es vertical u horizontal 
7997 REM pasando por el punto que se desee
7998 REM el punto se selecciona con a/z/,/.y se fija
7999 REM al pulsar 'x' o 'y' , lo que selecciona ademas el eje
8000 GOSUB 16000
8099 REM coeficientes de la transformacion 
8100 xtrans1=1:ytrans2=1
8110 IF respuesta$="x" THEN ytrans1=1:xtrans2=0 ELSE xtrans2=1:ytrans1=0
8199 REM borra la figura anterior
8200 GOSUB 2000
8299 REM calcula la figura transformada 
8300 GOSUB 12000
8399 REM dibujo de la figura transformada
8400 GOSUB 2000 
8499 respuesta$="" 
8500 RETURN
