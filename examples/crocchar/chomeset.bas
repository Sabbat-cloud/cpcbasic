10 MODE 1:lmax%=24:l%=1
20 SYMBOL AFTER 0:MEMORY (HIMEM-1)
30 FOR i=0 TO 255
40 IF l%>lmax% THEN INPUT "",k$:l%=1
50 ?CHR$(1)CHR$(i);" ";USING "###";i;
60 FOR n=HIMEM+i*8+1 TO HIMEM+i*8+8:?",";USING "###";PEEK(n);:NEXT n
70 l%=l%+1:?
80 NEXT i
