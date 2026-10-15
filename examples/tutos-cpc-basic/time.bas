10 'chronometre
20 MODE 1:DEG
30 DEF FNAngle=(seconde%*-6)+90 
40 seconde%=0
50 EVERY 50,1 GOSUB 80
60 'calcule angle en fonction de la seconde
70 GOTO 70
80 'dessine trait
90 graphics pen 0
100 PLOT 320,200
110 DRAW 320+200*COS(FNAngle),200+200*SIN(FNAngle)
120 seconde%=seconde%+1
130 graphics pen 2
140 PLOT 320,200
150 DRAW 320+200*COS(FNAngle),200+200*SIN(FNAngle)
160 RETURN
