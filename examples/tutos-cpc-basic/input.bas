10 mode 2
20 pen 1
30 input "Entrez un texte: ", text$
40 mode 0
50 col%=1
60 for l=1 to 25
70 for i=1 to len(text$)
71 pen col%
80 c$ = upper$(mid$(text$,i,1))
100 if not c$=" " then col%=col%+1
110 if col%>14 then col%=1
130 print c$;
140 next i
150 print " ";
160 next l
170 while inkey$="": wend
180 goto 10
190
