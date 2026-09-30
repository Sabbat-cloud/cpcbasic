10 MODE 1
20 x=100:y=100
30 xdistancia=50:ydistancia=100
39 REM se incrementa x en xinc cada vez que se dibuja el rectangulo
40 xinc=4
50 WHILE x<639
59   REM dibujo del rectangulo
60   color=1:GOSUB 1000
69   REM borrado del rectangulo
70   color=0:GOSUB 1000
80   x=x+xinc
90 WEND
100 END
999 REM instrucciones para dibujar el rectangulo 
1000 MOVE x,y
1010 DRAWR xdistancia,0,color
1020 DRAWR 0,ydistancia
1030 DRAWR -xdistancia,0
1040 DRAWR 0,-ydistancia
1050 RETURN

'-- Mejora para diagonal
40 xinc=4:yinc=2
80 x=x+xinc:y=y+yinc

'-- Rebote
45 continue=1
50 WHILE continue=1
59   REM dibujo del rectangulo
60   color=1:GOSUB 1000
69   REM borrado del rectangulo
70   color=0:GOSUB 1000
79   REM actualizar coordenadas y ver si caen fuer a de la pantalla
80   x=x+xinc:y=y+yinc
81   IF x<0 OR x>639 THEN xinc=-xinc:x=x+2*xinc 
88   IF y<0 OR y>399 THEN yinc=-yinc:y=y+2*yinc 
90 WEND
