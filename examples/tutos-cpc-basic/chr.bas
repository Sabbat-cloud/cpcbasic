10 cls
20 for x=1 to 39
30 locate x,20
40 frame
50 print " ";chr$(250)
60 next x
70 FOR n=1 TO 300: NEXT n
80 FOR x=39 TO 1 STEP -1
90 LOCATE x,20
100 FRAME
110 PRINT CHR$(251);" "
120 NEXT x
130 FOR n=1 TO 300:NEXT n
140 GOTO 20
