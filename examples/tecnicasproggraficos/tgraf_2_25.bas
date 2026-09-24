10 MODE 1
19 REM los tres caracteres que definen el cohete
20 SYMBOL 240,0,24,24,24,24,36,36,36
30 SYMBOL 241,36,36,36,36,36,36,36,36
40 SYMBOL 242,66,129,129,129,129,153,195,129
50 cohetearriba$=CHR$(240)
51 cohetemedio$=CHR$(241)
52 coheteabajo$=CHR$(242) 
60 TAG
70 xgrafico=300:ygrafico=100 
80 FOR y=ygrafico TO 350
89    REM se borra la base del antigua cohete
90    MOVE xgrafico,y-48 
100   PRINT " ";
110   MOVE xgrafico,y
120   PRINT cohetearriba$;
121   MOVE xgrafico,y-16
122   PRINT cohetemedio$;
123   MOVE xgrafico,y-32
124   PRINT coheteabajo$; 
130 NEXT
