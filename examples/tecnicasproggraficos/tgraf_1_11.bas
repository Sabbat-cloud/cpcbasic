10 MODE 1
20 INK 1,3,12 
30 INK 2,12,3 
40 tintapluma=1 
50 FOR x=1 TO 40
60 IF tintapluma=1 THEN tintapluma=2 ELSE tintapluma=1
70 PEN tintapluma
80 LOCATE x,13
90 PRINT CHR$(143);
100 NEXT
