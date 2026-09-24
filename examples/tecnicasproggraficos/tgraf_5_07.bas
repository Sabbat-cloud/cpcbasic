10 MODE 1
19 REM hacer amarillo el color cercano
20 INK 3,24
30 PRINT CHR$(23)CHR$(1);
40 x=100:y=100 
50 xd=50:yd=100 
60 INK 1,24
70 color=1:GOSUB 1000
80 x=100:y=100 
90 xd=100:yd=50 
100 INK 2,20
110 color=2:GOSUB 1000
120 PRINT CHR$(23)CHR$(0);
170 END
999 REM rectangulo relleno de color
1000 FOR xcord=x TO x+xd STEP 2
1010   MOVE xcord,y 
1020   DRAWR 3,yd,color
1030 NEXT
1040 RETURN

'----------
19 REM hacer azul el color cercano
20 INK 3,20
