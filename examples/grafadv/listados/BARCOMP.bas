10 REM **** BAR - AMPLIACIONES DEL PROGRAMA TABLA ****
20 REM Dibuja un diagrama de barras con dos conjuntos de datos para compararlos
25 REM para cada mes se leen a la vez dos puntos de dato
260 REM Ahora dibuja las barras
265 READ mxx
270 xf=129
275 TAG:MOVE 105,360:PRINT mxx;
280 MOVE 105,253:PRINT mxx/2;
285 MOVE 105,112:PRINT 0;
290 FOR i=1 TO 12
295 READ valor
300 valor=((valor/mxx)*250)+112
305 xf=xf+32
310 REM ahora dibuja el primer rectangulo
315 MOVE xf-8,valor:DRAW xf+8,valor
320 DRAW xf+8,112
325 DRAW xf-8,112
330 DRAW xf-8,valor
335 MOVE xf,115:FILL 1
340 REM ahora dibuja el segundo rectangulo para este mes
345 READ valor
350 valor=((valor/mxx)*250)+112
355 xf=xf+6
360 REM desplaza 6 pixels con respecto al primer rectangulo
365 MOVE xf-8,valor:DRAW xf+8,valor
370 DRAW xf+8,112
375 DRAW xf-8,112
380 DRAW xf-8,valor
385 xf=xf-6
390 NEXT i
400 REM sobreescribe esta linea
420 REM sobreescribe esta linea
520 DATA 100
530 DATA 50,40, 60,20, 70,10, 65,45, 45,75, 10,67
540 DATA 40,75, 50,50, 60,23, 56,43, 45,67, 54,10
