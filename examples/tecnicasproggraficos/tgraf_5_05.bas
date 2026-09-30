10 MODE 1
20 INK 3,24
30 DEFINT c,t,x,y
40 x=100:y=100 
50 x1=100:y1=200
60 color=1:color1=24
70 tipo=3:tono=1 
80 GOSUB 1000 
90 GOSUB 2000
100 tipo=3:tono=2 
110 WHILE x<639 
120   x=x+4:x1=x1+4 
130   GOSUB 2000 
140   GOSUB 1000 
150   x=x-4:x1=x1-4
160   GOSUB 2000:x=x+4:x1=x1+4
170   IF tono=2 THEN tono=1 ELSE tono=2
180 WEND
189 REM tintas de los colores usuales
190 INK 1,24
200 INK 2,20
210 INK 3,6
220 END
998 REM conmutacion de las tintas: la del color del fondo pasa a visible
999 REM y la de color visible pasa al del fondo 
1000 IF color=1 THEN color=24:color1=1 ELSE color=1:color1=24
1010 INK 1,color
1020 INK 2,color1
1030 RETURN
1993 REM la rutina borra y dibuja cuando el triangulo no es visible
1999 REM (o sea, cuando esta del color del fondo)
2000 PRINT CHR$(23);CHR$(tipo);
2010 MOVE x,y
2020 DRAW x1,y1,tono
2030 DRAW x1+50,y1
2040 DRAW x+50,y1
2050 DRAW x,y
2060 IF tipo=2 THEN tipo=3 ELSE tipo=2
2070 RETURN
