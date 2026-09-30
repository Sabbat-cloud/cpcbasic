10 MODE 0
20 DIM x(100),y(100) 
30 xant=320:yant=200 
40 x=320:y=200
50 colorvisible=1
60 PRINT CHR$(23);CHR$(1);
70 GOSUB 1000
80 GOSUB 2000
90 END
999 REM dibujo de la recta
1000 PLOT x,y,colorvisible
1010 DRAW xant,yant
1020 RETURN
2000 WHILE respuesta$<>"e"
2010   GOSUB 1000
2020   respuesta$=LOWER$(INKEY$) 
2030   IF respuesta$="a" THEN y=y+2 
2040   IF respuesta$="z" THEN y=y-2 
2050   IF respuesta$="," THEN x=x-4 
2060   IF respuesta$="." THEN x=x+4
2070   IF respuesta$=" " THEN GOSUB 3000 
2080   GOSUB 1000
2090 WEND
2100 RETURN
2999 REM opcion grafica normal para dibujar de m anera permanente
3000 PRINT CHR$(23);CHR$(0); 
3010 GOSUB 1000
3019 REM vuelta a la opcion XOR 
3020 PRINT CHR$(23);CHR$(1); 
3030 con=con+1
3040 x(con)=x:y(con)=y
3050 xant=x:yant=y
3060 RETURN
