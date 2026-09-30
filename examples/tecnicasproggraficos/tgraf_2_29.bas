10 MODE 0
20 GOSUB 1000
30 GOSUB 2000
40 END
1000 PAPER 12
1010 PEN 0
1020 CLS
1025 SYMBOL 242,255,255,255,255,255,255,255,255
1029 REM dibujo de la pista
1030 ladox=3:ladoy=7
1040 FOR y=ladoy TO ladoy+11
1050   LOCATE ladox,y
1060   PRINT CHR$(242)CHR$(242);
1070   LOCATE ladox+15,y
1080   PRINT CHR$(242)CHR$(242);
1090 NEXT
1100 xcom=7:ycom=5
1109 FOR con=-1 TO 1
1110   LOCATE xcom,ycom+con
1120   PRINT STRING$(8,CHR$(242));
1121   LOCATE xcom,ycom-1
1130   LOCATE xcom,ycom+15+con
1140   PRINT STRING$(8,CHR$(242));
1141 NEXT
1150 TAG
1160 color=0
1170 xizq=32:xder=576
1180 yabajo=150:yarriba=330
1190 ycambio=6:xcambio=32
1200 PLOT xizq+xcambio,yarriba+ycambio,color
1210 FOR con=1 TO 4
1220   yycambio=ycambio*con
1230   xxcambio=xcambio*con
1240   MOVE xizq+xxcambio,yarriba+yycambio
1250   PRINT CHR$(242);
1260   GOSUB 1600
1280   MOVE xder-xxcambio,yarriba+yycambio
1290   PRINT CHR$(242);
1300   GOSUB 1600
1320   MOVE xizq+xxcambio,yabajo-yycambio+8
1330   PRINT CHR$(242);
1340   GOSUB 1600
1360   MOVE xder-xxcambio,yabajo-yycambio+8
1370   PRINT CHR$(242);
1380   GOSUB 1600
1400 NEXT
1408 REM dos caracteres representando un coche
1409 REM uno para movimiento arriba/abajo; otro para movimiento izquierda/derecha
1410 SYMBOL 240,0,102,36,126,126,36,102,0
1420 SYMBOL 241,0,90,126,24,24,126,90,0
1430 lado$=CHR$(240)
1440 arriba$=CHR$(241)
1450 coche$=lado$
1460 xcoche=400:ycoche=338
1470 PLOT xcoche+16,ycoche-4,3
1480 MOVE xcoche,ycoche
1485 PEN 1: PAPER 0
1490 PRINT coche$;
1500 RETURN
1600 FOR con1=1 TO 4
1610   MOVER -32,-16
1620   PRINT CHR$(242);
1630 NEXT
1640 RETURN
1999 REM examen del teclado
2000 golpe=0
2010 xcambio=0:ycambio=0
2020 WHILE golpe=0
2030   respuesta$=LOWER$(INKEY$)
2040   IF respuesta$="a" THEN xcambio=0:ycambio=2:coche$=arriba$:testx=-16:testy=2
2050   IF respuesta$="z" THEN xcambio=0:ycambio=-2:coche$=arriba$:testx=-16:testy=-16
2060   IF respuesta$="." THEN xcambio=4:ycambio=0:coche$=lado$:testx=0:testy=-8
2070   IF respuesta$="," THEN xcambio=-4:ycambio=0:coche$=lado$:testx=-36:testy=-8
2079   REM la barra de espacio para parar el coche
2080   IF respuesta$=" " THEN xcambio=0:ycambio=0
2089   REM solo se dibuja el coche si se ha movido
2090   IF xcambio<>0 OR ycambio<>0 THEN GOSUB 3000
2100 WEND
2110 RETURN
2999 REM se comprueba el color del punto siguiente a la posicion actual
3000 color=TESTR(testx,testy)
3009 REM si no es el de ink 0 el coche esta fuera de la pista
3010 IF color<>0 THEN golpe=1:SOUND 7,500
3020 xcoche=xcoche+xcambio:ycoche=ycoche+ycambio
3030 MOVE xcoche,ycoche
3035 PEN 1: PAPER 0
3040 PRINT coche$;
3050 RETURN
