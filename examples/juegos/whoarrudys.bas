10 mode 2
20 for i=0 to 200
30 reste=i mod 8
40 adr=49152+int(i/8)*80
50 if reste>0 then adr=adr+reste*2048
60 poke adr,255
65 poke adr+1,170
70 next
