10 'Illustration de la palette
20 FOR indexPalette%=0 TO 26
30 BORDER indexPalette%
40 INK 0,indexPalette%
50 WHILE(INKEY$=""):WEND
60 NEXT indexPalette%
70 INK 0,1:BORDER 1
