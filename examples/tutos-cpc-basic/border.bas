10 mode 1
30 border int(rnd*26)
40 ink 0,int(rnd*26)
50 ink 1,int(rnd*26)
60 ink 2,int(rnd*26)
70 ink 3,int(rnd*26)
80 x1=2:y1=2:x2=39:y2=24:pencil=1:symb$=chr$(128+rnd*126): gosub 170
90 x1=4:y1=4:x2=37:y2=22:pencil=2:symb$=chr$(128+rnd*126): gosub 170
100 x1=6:y1=6:x2=35:y2=20:pencil=3:symb$=chr$(128+rnd*126): gosub 170
110 locate 14,11
120 print "PRESS ANY KEY"
130 locate 15,14
140 print "TO CONTINUE"
150 while inkey$="": wend
160 goto 30
170 rem DRAW BORDER
180 for l=y1 to y2
190 pen pencil
200 if l=y1 or l=y2 then locate x1,l: print STRING$(x2-x1+1,symb$);
210 if l>y1 and l<y2 then locate x1,l: print symb$;: locate x2,l: print symb$;
220 next l
230 return
240 
