10 REM ****PROGAMA PROY3D****
20 REM Demostracion de un sencillo metodo de proyeccion en 2 dimensiones
30 DIM x(50),y(50),z(50),ln(2,50)
40 DIM xp(50),yp(50)
45 CLS
50 REM Toma los datos para dibujar la casa
60 OPENIN "casa.dat"
70 INPUT #9,npts
80 FOR i=1 TO npts
90 INPUT #9,x(i),y(i),z(i)
100 xp(i)=x(i)
110 yp(i)=y(i)
120 NEXT i
122 INPUT #9,li
124 FOR i=1 TO li
126 INPUT #9,ln(1,i),ln(2,i)
128 NEXT i
130 CLOSEIN
140 REM Dibujo de los ejes
150 MOVE 180,280
160 DRAW 180,180
170 DRAW 280,180
180 REM Ahora dibuja la casa
185 REM Observe las coordenadas son respecto al origen con una traslacion de +200
190 FOR i=1 TO li
200 MOVE xp(ln(1,i))+200,yp(ln(1,i))+200
210 DRAW xp(ln(2,i))+200,yp(ln(2,i))+200
220 NEXT i
230 END
