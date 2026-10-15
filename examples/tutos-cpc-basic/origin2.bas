10 'gérer une fenetre avec l'instruction origin
20 mode 1:border 13:tag
21 move 260, 340
22 print "D E M O";
30 origin 0,0,100,540,100,300
40 graphics paper 3:clg'efface uniquement la fenetre
50 for x=550 to -340 step -5
60 move x,206
70 print "Amstrad CPC 6128 ";
80 frame
90 next
100 goto 40
