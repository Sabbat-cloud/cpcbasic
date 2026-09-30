10 MODE 1
19 REM los tres caracteres que definen el cohete
20 SYMBOL 240,0,24,24,24,24,36,36,36
30 SYMBOL 241,36,36,36,36,36,36,36,36
40 SYMBOL 242,66,129,129,129,129,153,195,129
50 cohete$=CHR$(240)+CHR$(8)+CHR$(10)+CHR$(241)+CHR$(8)+CHR$(10)+CHR$(242)
60 TAG
70 xgrafico=300:ygrafico=100
80 FOR y=ygrafico TO 350
89    REM se borra la base del antiguo cohete
90   MOVE xgrafico,y-24
100   PRINT " ";
109   REM imprimir el nuevo cohete(que birria)
110   MOVE xgrafico,y
120   PRINT cohete$;
130 NEXT
