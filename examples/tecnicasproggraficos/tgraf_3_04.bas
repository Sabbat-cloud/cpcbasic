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
806 READ tinta0,tinta1
807 INK 0,tinta0
808 INK 1,tinta1
809 PAPER 0:PEN 1
810 cruzx=10
811 cruzy=10
812 unir=1
814 FOR con=1 TO numdepuntos
815   READ x(con):xdib=(x(con)-minx)/puntox
816   x(con)=xdib
820   READ y(con):ydib=(y(con)-miny)/puntoy
821   y(con)=ydib
825   PLOT xdib,ydib
830   MOVER -cruzx,cruzy
840   DRAWR 2*cruzx,-2*cruzy
850   MOVER -2*cruzx,0
860   DRAWR 2*cruzx,2*cruzy
870   MOVER -cruzx,-cruzy
874   REM si unir esta a 1 los puntos se van uniendo
875   IF unir=1 AND con>1 THEN DRAW x(con-1),y(con-1)
880 NEXT
990 RETURN
1000 DATA 5,0,24,200,100,1000,200,1500,300,2500,600,4000,1000