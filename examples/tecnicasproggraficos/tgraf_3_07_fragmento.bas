708 FOR con=0 TO xcantidad
710   MOVE 0,0
711   REM avance en el eje hasta en comienzo de la marca.
712   MOVE xancho*con,0
713   REM dibujo de la marca
714   DRAWR 0,-xmarca
715   REM posicion para escribir el rotulo de la marca
716   MOVER -charancho/2,-xmarca
718   numero$=STR$(minx+con*xvalor)
719   REM se trunca el numero si es demasiado largo
720   numero$=MID$(numero$,2,maxxcadena)
722   longitud=LEN(numero$)
723   REM se suprime el punto decimal si es el ultimo caracter
724   IF MID$(numero$,longitud)="." THEN numero$=MID$(numero$,1,longitud-1)
726   PRINT numero$;
728 NEXT
729 REM lo mismo para el eje y
730 yvalor=dify/ycantidad
732 FOR con=0 TO ycantidad
734   MOVE 0,0
736   MOVER 0,yalto*con
738   DRAWR -ymarca,0
740   MOVER -grafycadena,charalto/2
742   numero$=STR$(minyl-con*yvalor)
744   numero$=MID$(numero$,2,maxycadena)
746   longitud=LEN(numero$)
748   IF MID$(numero$,longitud)="." THEN numero$=MID$(numero$,1,1ongitud-1)
749   REM esto es para alinear los numeros junto a las marcas
750   IF LEN(numero$)<maxycadena THEN numero$=STRING$(maxycadena-LEN(numero$)," ")+numero$
752   PRINT numero$;
754 NEXT
790 RETURN
