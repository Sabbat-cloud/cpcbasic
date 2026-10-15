10 'test de scroll
15 RANDOMIZE TIME
16 border 0:MODE 0:INK 0,0:INK 1,26:INK 3,6
20 maxStars%=2:largeurEcran%=20:xRocket%=largeurEcran%/2
30 CLS
40 GOSUB 100
44 PRINT CHR$(11);CHR$(11);CHR$(11);CHR$(11);
47 FRAME
50 LOCATE xRocket%,25:PEN 3:PRINT CHR$(239);
60 IF (INKEY(1)=0 AND xRocket%<largeurEcran%) THEN xRocket%=xRocket%+1
70 IF (INKEY(8)=0 AND xRocket%>1) THEN xRocket%=xRocket%-1
90 GOTO 40
100 'genere starfield random
110 ligne$=STRING$(largeurEcran%," ")
120 nbStars%=RND*maxStars%
130 FOR i%=1 TO nbStars%
140 x%=RND*(largeurEcran%-1)
150 MID$(ligne$,x%+1,1)=chr$(144)
160 NEXT i%
165 PEN 1
168 LOCATE 1,1
170 PRINT ligne$
180 RETURN
