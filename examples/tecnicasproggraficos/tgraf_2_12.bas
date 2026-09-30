10 MODE 0
20 SYMBOL 240,0,4,7,132,124,130,130,0
30 FOR perroaleatorio=1 TO 30 
40   xaleat=INT(19*RND(1)+1) 
50   yaleat=INT(24*RND(1)+1)
60   tintapluma=INT(15*RND(1)+1) 
70   PEN tintapluma
80   LOCATE xaleat,yaleat 
90   PRINT CHR$(240)
100 NEXT
