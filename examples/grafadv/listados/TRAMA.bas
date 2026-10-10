405 xl=xf-8:xr=xf+8:yt=valor:yb=115:REM Carga de las esquinas para tramado
410 MOVE xf,115:GOSUB 5000:REM trama
5000 REM Valores de trama
5005 xa=1:ya=1:sep=2:REM Establece los valores de trama
5010 IF xa/ya>2 THEN 5100
5020 FOR l=xr TO xl STEP -sep*3
5030 x=l
5040 y=yt
5050 PLOT x,y
5060 x=x-a
5070 y=y-a
5080 IF y>=yb AND x>xl THEN 5050
5090 NEXT l
5100 IF ya/xa >2 THEN RETURN
5110 REM Ahora rellena la seccion inferior
5120 FOR l=yt TO yb STEP -sep*3
5130 y=l
5140 x=xr
5150 PLOT x,y
5160 y=y-a
5170 x=x-a
5180 IF y>=yb AND x>xl THEN 5150
5190 NEXT l
5200 RETURN
