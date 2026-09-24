830 barraancho=xancho-4
835 color=2
840 FOR con=1 TO numerodebarras
844   REM se alterna el color de las barras
845   IF color=3 THEN color=2 ELSE color=3
848   REM las barras se rellenan mas rapidamente t omando un paso
849   REM adecuado a la resolucion del modo de pan talla, para no repetir lineas
850   FOR barra=0 TO barraancho STEP charancho/8 
860     MOVE 0+barra,0
870     DRAWR 0,y(con),color
880   NEXT
890   ox=ox+xancho
899   REM desplazamiento del origen para dibujar la siguiente barra
900   ORIGIN ox,oy
910 NEXT
990 RETURN
