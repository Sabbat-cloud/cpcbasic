155 color=1:DRAW 0,radio,color 
160 FOR con1=1 TO lados-1
170   FOR con2=con1+1 TO lados
173     REM experimente con los colores en la linea 175
174     REM cambie el MOD para ver el efecto
175     color=1+(color+1) MOD 3 
180     MOVE x(con1),y(con1)
190     DRAW x(con2),y(con2),color 
200   NEXT
210 NEXT
