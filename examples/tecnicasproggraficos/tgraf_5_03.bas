30 xd=50:yd=100
39 REM poner la tinta 1 con el color del fondo
40 INK 1,1
49 REM dibujar un rectangulo usando la tinta 1 
50 color=1:GOSUB 1000
60 x=300: y=300
70 xd=100:yd=50
79 REM poner la tinta 2 con el color del fondo 
30 INK 2,1
89 REM dibujar un rectangulo usando la tinta 2
90 color=2:GOSUB 1000
100 continue=1
109 REM repetir los dibujos hasta que se apriete
110 WHILE respuesta$<>"e"
119   REM hacer visible la tinta 1 y la tinta 2 de 1 color del fondo
120   INK 1,21
130   INK 2,1
139   REM en espera de que se pulse una tecla
140   respuesta$=""
150   WHILE respuesta$=""
160     respuesta$=LOWER$(INKEY$).
170   WEND
179   REM hacer visible la tinta 2 y la tinta 1 de 1 color del fondo
160   INK 1,1
190   INK 2,24
199   REM en espera de que se pulse una tecla
200   respuesta$=""
210   WHILE respuesta$=""
220     respuesta$=LOWER$(INKEY$)
230   WEND
240 WEND
249 REM tintas del color habitual
250 INK 1,24
260 INK 2,20
270 END
1000 MOVE x,y
1010 DRAWR xd,0,color
1020 DRAWR 0,yd 
1030 DRAWR -xd,0 
1040 DRAWR 0,-yd 
1050 RETURN

'-- Solapados
59 REM esta vez los dos rectangulos se solapan 
60 x=120:y=100
