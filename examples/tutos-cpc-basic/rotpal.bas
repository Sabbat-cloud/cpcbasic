10 'rotation de palette
20 MODE 0
30 border 0
40 'init palette
50 DIM palette%(15)
60 restore 230
70 FOR i%=0 TO 15
80 READ color%
90 palette%(i%)=color%
100 INK i%,color%
110 NEXT i%
120 'draw line
130 FOR i%=0 TO 640 STEP 4
140 PLOT i%,0,(i%/4) MOD 16
150 DRAW i%,400,(i%/4) MOD 16
160 NEXT i%
170 'cycle colors
180 i%=0:decalage%=0
190 INK ((i% + decalage%) MOD 16),palette%(i%)
200 i%=(i%+1) MOD 16
210 IF i%=0 THEN decalage%=(decalage%+1 MOD 16)
220 GOTO 190
230 DATA 0,1,2,11,20,23,26,25,24,15,16,6,7,8,5,4
240 
