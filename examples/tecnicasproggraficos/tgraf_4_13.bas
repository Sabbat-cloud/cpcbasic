10 MODE 1
20 GOSUB 1000
40 END
998 REM datos para un octogono
999 REM pruebe con otras figuras
1000 xcom=0:ycom=0
1001 REM xcom,ycom forman el centro del primer poligono
1010 radio=40
1020 lados=8
1030 paso=2*PI/lados
1040 color=2
1050 GOSUB 3000
1060 RETURN
2998 REM se rellena la pantalla con copias del poligono
2999 REM se detiene cuando las coordenadas del centro se salen de la pantalla
3000 centrox=xcom:centroy=ycom
3010 WHILE centrox<639 OR centroy<399
3020   ORIGIN centrox,centroy
3030   MOVE 0,radio
3040   FOR angulo=0 TO 2*PI STEP paso
3050     DRAW radio*SIN(angulo),radio*COS(angulo),color
3060   NEXT
3069   REM desplazamiento en la direccion de la x 
3070   centrox=centrox+radio*2
3079   REM si se sale de la pantalla se recomienza mas arriba
3080   IF centrox>639 AND centroy<399 THEN centrox=xcom:centroy=centroy+radio*2
3090 WEND
3100 RETURN
