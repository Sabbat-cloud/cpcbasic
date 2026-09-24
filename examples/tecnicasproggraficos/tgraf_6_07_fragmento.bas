15 DIM x(300),y(300)
5031 IF rell=1 AND circ=0 AND rectangulo=0 AND triangulo=0 THEN GOSUB 15000
6069 REM debe ser la opcion rellenar/no rellenar 
6070 IF rell=1 THEN rell=0:rell$=CHR$(241) ELSE rell=1:rell$=CHR$(233)
6080 LOCATE 17,24
6090 PRINT rell$;
6100 RETURN
8091 IF rell=1 THEN x=xant:y=yant:GOSUB 15000 
9061 IF rell=1 THEN x=(x+xant)/2:y=(y+yant)/2:GOSUB 15000
10061 IF rell=1 THEN x=(x+xant+x1)/3:y=(y+yant+y1)/3:GOSUB 15000
10071 REM anadir ademas la rutina de rellenar 
10072 REM desde la linea 15000 a la 19020
