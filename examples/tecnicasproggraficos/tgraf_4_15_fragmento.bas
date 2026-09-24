3079 REM si se sale de la pantalla se recomienza mas arriba
3080 IF centrox>639 AND centroy<399 THEN GOSUB 4000
3090 WEND
3100 RETURN
3999 REM se escalona el comienzo de cada fila de poligonos
4000 IF xcom=0 THEN xcom=radio ELSE xcom=0 
4010 centrox=xcom:centroy=centroy+radio*2 
4020 RETURN
