830 barraancho=xancho-4
831 REM barralado es la anchura del lateral de la barra
832 REM barrasuple es la altura suplementaria de la parte trasera de la barra sobre la delantera
833 REM modifique los valores segun quiera que a parezcan mas o menos profundas
834 barralado=barraancho/4:barrasuple=barralado
835 color=2
840 FOR con=1 TO numerodebarras
844   REM se alterna el color de las barras
845   IF color=3 THEN color=2 ELSE color=3
846   barrasuplecon=0
848   REM tambien hay que rellenar el lateral de 1 a barra
849   REM luego el ancho de la barra es barraanchq 1-barralado
850   FOR barra=0 TO barraancho+barralado STEP charancho/8
859     REM el fin de la linea se dibuja en otro color como ocurrira con todas las aristas de la bar ra
860     PLOT 0+barra,0,1
869     REM la linea hasta arriba de la barra
870     DRAWR 0,y(con)+barrasuplecon,color
871     REM el otro final de la linea tambien en color diferente
872     PLOTR 0,0,1
873     REM la linea siguiente debe ser un poco mas alta
874     REM y asi hasta alcanzar la parte de atras de la barra
875     barrasuplecon=barrasuplecon+charancho/8:IF barrasuplecon>barrasuple THEN barrasuplecon=bartop
880   NEXT
881   REM las aristas de la barra van en otro color
882   y=y(con):MOVE 0,0
883   DRAWR 0,y,1
884   DRAWR barraancho,0
885   DRAWR 0,-y
886   MOVER 0,y
887   DRAWR barralado,barrasuple
888   DRAWR 0,-y-barrasuple
890   ox=ox+xancho
899   REM desplazamiento del origen para dibujar 1 a siguiente barra
900   ORIGIN ox,oy 
910 NEXT
990 RETURN
