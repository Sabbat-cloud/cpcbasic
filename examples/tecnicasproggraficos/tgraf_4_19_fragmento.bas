15 WINDOW 1,40,24,25
16 PRINT "Color: "
17 PRINT "x:	y: "

1051 IF respuesta$="d" THEN color=colorvisible 
1052 IF respuesta$="f" THEN colorvisible=color:color=0
1053 IF respuesta$="c" THEN color=1+(color+1) MOD 3
1060 PLOT x,y,colorvisible
1065 GOSUB 2000
1070 WEND
1080 RETURN
2000 IF colorviejo<>color THEN LOCATE 9,1:PRINT color
2010 IF xviejo<>x THEN LOCATE 4,2:PRINT x; 
2020 IF yviejo<>y THEN LOCATE 12,2:PRINT y; 
2030 colorviejo=color
2040 xviejo=x:yviejo=y
2050 RETURN

