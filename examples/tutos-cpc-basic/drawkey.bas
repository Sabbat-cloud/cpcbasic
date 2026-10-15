10 'Dessine avec les flèches
20 'Espace pour changer de pinceau
30 MODE 0: BORDER 0
40 'Redéfinit la palette de couleurs
50 DIM palette%(15)
60 FOR i%=0 TO 15:READ color%:INK i%,color%:NEXT i%
70 DATA 0,1,2,11,20,23,26,25,24,15,16,6,7,8,5,4
80 'Initialise le pinceau actif
90 pinceau%=1
100 MOVE 320,200
110 GRAPHICS PEN pinceau%
120 'Teste les touches
130 IF INKEY(2)=0 THEN DRAWR 0,-1
140 IF INKEY(0)=0 THEN DRAWR 0,1
150 IF INKEY(8)=0 THEN DRAWR -1,0
160 IF INKEY(1)=0 THEN DRAWR 1,0
170 IF INKEY(47)=0 THEN pinceau%=pinceau%+1
180 IF pinceau%>15 then pinceau%=1
190 GOTO 110
