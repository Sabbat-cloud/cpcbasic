10 MODE 1
20 GOSUB 500
30 GOSUB 800
40 END
499 REM dibujar los ejes
500 ox=100:oy=50
503 REM se oculta la grafica hasta que este completa
504 INK 0,24:INK 1,24
505 ORIGIN ox,oy
510 ypunto=399-oy
515 xpunto=639-ox
520 MOVE 0,ypunto
530 DRAW 0,0,1
540 DRAW xpunto,0
580 miny=100
590 maxy=1000
600 dify=maxy-miny
620 puntoy=dify/ypunto
628 REM numero de marcas; esta vez solo en el eje y
629 REM xcantidad es el numero de barras
630 READ numerodebarras:xcantidad=numerodebarras 
640 ycantidad=9
649 REM distancia grafica entre las marcas
650 xancho=INT(xpunto/xcantidad)
660 yalto=INT(ypunto/ycantidad)
673 REM tamano de los caracteres en el modo 1 (en numero de puntos)
674 REM el ancho debe cambiar a 32 para el modo 0 y a 8 para el modo 2.
675 charancho=16
676 charalto=16
692 maxycadena=4
694 grafycadena=charancho*maxycadena
696 IF ox<grafycadena OR yalto<charalto THEN RETURN
699 REM longitud de las marcas de los ejes
700 xmarca=6
702 ymarca=8
706 TAG
728 REM el rotulo de cada marca sera de un valor yvalor mas alto que el anterior
729 REM se avanza ycantidad veces para obtener el numero de marcas que corresponde
730 yvalor=dify/ycantidad
732 FOR con=0 TO ycantidad
734   MOVE 0,0
736   MOVER 0,yalto*con
738   DRAWR -ymarca,0
740   MOVER -grafycadena,charalto/2
742   numero$=STR$(miny+con*yvalor)
744   numero$=MID$(numero$,2,maxycadena)
746   longitud=LEN(numero$)
748   IF MID$(numero$,longitud)="." THEN numero$=MID$(numero$,1,longitud-1)
749   REM esto es para alinear los numeras junto a las marcas
750   IF LEN(numero$)<maxycadena THEN numero$=STRING$(maxycadena-LEN(numero$)," ")+numero$ 
752   PRINT numero$;
754 NEXT
755 REM rotulos de los ajes
756 xrotulo$="numero de ratones"
758 yrotulo$="gramos de queso roidos"
759 REM longitud del rotulo en puntos graficos
760 xrotulolon=LEN(xrotulo$)*charancho
761 REM espacio antes del rotulo, para que quede centrado
762 xrotulocom=(xpunto-xrotulolon)/2
763 REM colocarse a la altura conveniente debajo del eje x para escribir el rotulo
764 MOVE xrotulocom,-2*charalto
766 PRINT xrotulo$;
767 REM lo mismo para El eje y
768 yrotulolon=LEN(yrotulo$)*charalto
770 yrotulocom=(ypunto+yrotulolon)/2
771 REM hay que escribir separadamente cada letra del rotulo, ya que va en vertical
772 FOR con=1 TO LEN(yrotulo$)
773   REM se extrae un caracter del rotulo
774   char$=MID$(yrotulo$,con,1)
775   REM ponerse convenientemente a la izquierda para imprimir el caracter
776   MOVE -charancho*(maxycadena+2),yrotulocom-charalto*(con-1)
770   PRINT char$;
780 NEXT
790 RETURN
799 REM leer puntos del data y dibujar las barras
800 DIM y(numerodebarras)
806 READ tinta0,tinta1
807 INK 0,tinta0
808 INK 1,tinta1
809 PAPER 0:PEN 1
814 FOR con=1 TO numerodebarras
815   READ y
816   x(con)=xdib
819   REM altura de la barra calculada a la escala conveniente
820   y(con)=(y-miny)/puntoy
825 NEXT
829 REM reducir la anchura de las barras para dejar espacio entre ellas
830 barraancho=xancho-4
840 FOR con=1 TO numerodebarras
850   MOVE 0,0
860   DRAWR 0,y(con),1
870   DRAWR barraancho,0
880   DRAWR 0,-y(con)
890   ox=ox+xancho
899   REM desplazamiento del origen para dibujar la barra siguiente
900   ORIGIN ox,oy
910 NEXT
990 RETURN
999 REM ahora solo se necesita la altura de las barras; la anchura es fija
1000 DATA 10,0,24,350,190,760,440,990,124,846,545,666,222
