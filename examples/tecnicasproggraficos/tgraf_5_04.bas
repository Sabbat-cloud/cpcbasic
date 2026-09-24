10 MODE 0
19 REM posicion de comienzo de la esquina del rectangulo
20 xcom=260:ycom=180
29 REM loggitud de los lados
30 longitudx=20:longitudy=20
39 REM diferencia del tamano de los sucesivos rectangulos
40 incx=8:incy=6
50 tintacom=1:tintafin=15
60 GOSUB 1000
70 GOSUB 2000
80 END
998 REM dibujar 15 rectangulos del color del fondo
999 REM uno dentro de otro
1000 FOR con=tintacom TO tintafin
1010   INK con,1
1020   movex=con*incx
1030   movey=con*incy
1040   ladox=longitudx+2*movex
1050   ladoy=longitudy+2*movey
1060   MOVE xcom-movex,ycom-movey
1070   DRAWR ladox,0,con
1080   DRAWR 0,ladoy
1090   DRAWR -ladox,0
1100   DRAWR 0,-ladoy
1110 NEXT
1120 RETURN
1999 REM ciclo de cambio del color de las tintas para que aparezca un reetangulo cada vez
2000 continue=1
2010 tintacom=1:tintasig=2
2019 REM continuar indefinidamente
2020 WHILE continue=1
2029   REM se espera la pulsacion de una tecla
2030   respuesta$=""
2040   WHILE respuesta$=""
2050     respuesta$=INKEY$
2060   WEND
2069   REM cambiar el rectangulo anterior al color del fondo
2070   INK tintacom,1
2079   REM cambiar el siguiente rectangulo a color visible
2080   INK tintasig,24
2088   REM incrementar el numero de tinta para rep etir el ciclo de instrucciones
2089   REM la actual pasa al color del fondo y la siguiente a color visible
2090   tintacom=(tintacom+1) MOD 16
2100   IF tintacom=0 THEN tintacom=1
2110   tintasig=(tintasig+1) MOD 16
2120   IF tintasig=0 THEN tintasig=1
2130 WEND
2140 RETURN

'----
15 PRINT CHR$(23)CHR$(1); 
265 PRINT CHR$(23)CHR$(0);

'-----
11 REM tinta 3 de color amarillo
12 INK 3,24
261 REM tinta 3 a su color normal
262 INK 3,6
