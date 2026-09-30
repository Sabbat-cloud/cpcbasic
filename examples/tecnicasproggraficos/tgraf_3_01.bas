10 MODE 1
20 GOSUB 500 
30 GOSUB 800 
40 END
499 REM dibujar los ejes
500 ypunto=399
510 xpunto=639
520 MOVE 0,ypunto
530 DRAW 0,0,1
540 DRAW xpunto,0
550 minx=200
560 maxx=4000
570 difx=maxx-minx
580 miny=100
590 maxy=1000
600 dify=maxy-miny
610 puntox=difx/xpunto
620 puntoy=dify/ypunto
690 RETURN
799 REM leer puntos del data y dibujarlos
800 READ numdepuntos
805 DIM x(numdepuntos),y(numdepuntos) 
810 FOR con=1 TO numdepuntos
815   READ x(con):xdib=(x(con)-minx)/puntox 
820   READ y(con):ydib=(y(con)-miny)/puntoy 
825   PLOT xdib,ydib
930 NEXT
990 RETURN
1000 DATA 5,200,100,1000,200,1500,300,2500,600,4000,1000

