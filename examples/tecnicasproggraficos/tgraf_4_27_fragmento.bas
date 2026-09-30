2073 IF respuesta$="s" THEN GOSUB 5000
5000 WINDOW 1,20,25,25
5010 INPUT"Escala: ";escala
5018 REM multiplica los valores por el factor de escala
5019 REM tomando como centro el punto donde esta el cursor
5020 FOR valor=1 TO con
5030   x(valor)=escala*(x(valor)-x)+320
5040   y(valor)=escala*(y(valor)-y)+200
5050 NEXT
5060 GOSUB 6000
5070 RETURN
