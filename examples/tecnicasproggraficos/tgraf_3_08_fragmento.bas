755 REM rotulos de los ejes
756 xrotulo$="numero de ratones"
758 yrotulo$="gramos de queso roidos"
759 REM longitud del rotulo en puntos graficos
760 xrotulolon=LEN(rotulo$)*charancho
761 REM espacio antes del rotulo, para que quede centrado
762 xrotulocom=(xpunto-xrotulolon)/2
763 REM colocarse a la altura conveniente debajo del eje x para escribir el rotulo
764 MOVE xrotulocom,-2*charalto
766 PRINT xrotulo$;
767 REM lo mismo para el eje y
768 yrotulolon=LEN(yrotulo$)*charalto
770 yrotulocom=(ypunto+yrotulolon)/2
771 REM hay que escribir separadamente cada letr a del rotulo, ya que va en vertical
772 FOR con=1 TO LEN(yrotulo$)
773   REM se extrae un caracter del rotulo
774   char$=MID$(yrotulo$,con,1)
775   REM ponerse convenientemente a la izquierda para imprimir el caracter
776   MOVE -charancho*(maxycadena+2),yrotulocom-charalto*(con-1)
778   PRINT char$;
780 NEXT
790 RETURN
