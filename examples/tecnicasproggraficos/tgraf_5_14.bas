10 MODE 0
20 GOSUB 1000 
30 GOSUB 2000 
40 GOSUB 3000
50 PRINT CHR$(23)CHR$(0);
60 MODE 1
70 END
999 REM tintas con las colores apropiados
1000 INK 3,20 
1010 INK 5,26 
1020 INK 6,26 
1030 INK 7,26 
1040 RETURN
1999 REM dibujar tres rectangulos uno encima de otro
2000 xamarillo=100:yamarillo=40:ladoamarillo=300 
2010 xcyan=150:ycyan=80:ladocyan=220
2020 xblanco=200:yblanco=120:ladoblanco=140 
2029 REM opcion XOR
2030 PRINT CHR$(23)CHR$(1);
2040 color=1:x=xamarillo:y=yamarillo:lado=ladoamarillo
2050 GOSUB 4000
2060 color=2:x=xcyan:y=ycyan:lado=ladocyan 
2070 GOSUB 4000
2080 color=4:x=xblanco:y=yblanco:lado=ladoblanco 
2090 GOSUB 4000
2100 RETURN
3000 WINDOW 1,20,25,25
3009 REM peticion de comando
3010 WHILE respuesta$<>"e"
3020   INPUT"Comando (a/c/b/e) ",respuesta$ 
3029   REM dibujo o borrado del amarillo
3030   IF respuesta$="a" THEN color=1:x=xamarillo:y=yamarillo:lado=ladoamarillo:GOSUB 4000 
3039   REM dibujo o borrado del cyan
3040   IF respuesta$="c" THEN color=2:x=xcyan:y=ycyan:lado=ladocyan:GOSUB 4000
3049   REM dibujo o borrado del blanco
3050   IF respuesta$="b" THEN color=4:x=xblanco:y=yblanco:lado=ladoblanco:GOSUB 4000
3890 WEND
3900 RETURN
4000 FOR xcord=x TO x+lado STEP 4
4010   MOVE xcord,y
4020   DRAWR 0,lado,color
4030 NEXT
4040 RETURN
