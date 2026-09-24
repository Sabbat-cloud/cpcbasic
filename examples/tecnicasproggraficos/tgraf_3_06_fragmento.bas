503 REM se oculta la grafica hasta que este completa
504 INK 0,24:INK 1,24
628 REM numero de marcas en los ejes x e y
629 REM sin incluir la del origen
630 xcantidad=5
640 ycantidad=10
649 REM distancia grafica entre las marcas
650 xancho=INT(xpunto/xcantidad)
660 yalto=INT(ypunto/ycantidad)
668 REM cantidad maxima de caracteres de los numeros del eje x
669 REM esto tendra que cambiarlo para adaptarlo a sus propios datos
670 maxxcadena=4
673 REM tamano de los caracteres en el modo 1 (en numero de puntos)
674 REM el ancho debe Cambiar a 32 para el modo 0 y a 8 para el modo 2
675 charancho=16
676 charalto=16
679 REM se calcula la maxima longitud de la cadena en puntos graficos
680 grafxcadena=charancho*maxxcadena
688 REM no se rotulan los ejes cuando habria que poner numeros demasiado grandes
689 REM o cuando la distancia entre marcas es menor que el temario de un caracter
690 IF xancho<grafxcadena OR xancho<charancho THEN RETURN
691 REM lo mismo para el eje y
692 maxycadena=4
694 grafycadena=charancho*maxycadena
696 IF ox<grafycadena OR yalto<charalto THEN RETURN
699 REM longitud de las marcas de los ejes
700 xmarca=6
702 ymarca=8
703 REM el rotulo de cada marca sera de un valor xvalor mas alto que el anterior
704 xvalor=difx/xcantidad
706 TAG
707 REM se avanza x cantidad veces para obtener el numero de marcas que corresponde
708 FOR con=0 TO xcantidad
710   MOVE 0,0
711   REM avance en el eje hasta en comienzo de la marca
712   MOVE xancho*con,0
713   REM dibujo de la marca
714   DRAWR 0,-xmarca
728 NEXT
729 REM lo mismo para el eje y
730 yvalor=dify/ycantidad
732 FOR con=0 TO ycantidad
734   MOVE 0,0
736   MOVER 0,yalto*con 
738   DRAWR -ymarca,0 
754   NEXT
790 RETURN
