2995 REM 'r' para la rotacion
3040 IF respuesta$="r" THEN GOSUB 5000
4995 REM rutina de rotacion
4998 REM la rotacion es de 5 grados en el sentido del reloj
4999 REM pero puede cambiar estos datos
5000 angulo=5
5010 rotacion=1
5199 REM barra la figura anterior
5200 GOSUB 2000
5299 REM coeficientes de la transformacion 
5300 DEG
5310 xtrans1=COS(angulo):ytrans2=xtrans1:xtrans2=rotacion*SIN(angulo):ytrans1=-xtrans2
5499 REM calcula la figura girada
5500 GOSUB 11000
5599 REM dibuja la figura girada
5600 GOSUB 2000
5699 respuesta$=""
5700 RETURN
10999 REM cambio de datos por transformacion mat ricial
11000 FOR con=0 TO numdelin
11010   almacen=x(con)
11020   x(con)=x(con)*xtrans1+y(con)*xtrans2 
11030   y(con)=almacen*ytrans1+y(con)*ytrans2 
11040 NEXT
11100 RETURN
