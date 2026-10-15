10 randomize time
20 mode 1: pen 2
30 locate 4,3
40 sol% = rnd*100
50 print "DEVINE UN NOMBRE ENTRE 0 ET 100"
60 locate 1,9
70 gosub 170
80 locate 4,9
90 pen 1
100 input "Ton choix ? ", guess%
110 if guess%<sol% then gosub 260
120 if guess%>sol% then gosub 210
130 if guess%=sol% then gosub 310
140 goto 60
150 end
160 rem DELETE TWO LINES
170 for i=1 to 80
180 print " ";
190 next i
200 return 
210 rem TOO BIG
220 pen 3
230 locate 14, 6
240 print "Trop grand"
250 return
260 rem TOO SMALL
270 pen 3
280 locate 14, 6
290 print "Trop petit"
300 return
310 rem YOU WIN
320 pen 1
330 locate 14, 6
340 print " BRAVO !!! "
350 while inkey$="": wend
360 goto 20
370 
