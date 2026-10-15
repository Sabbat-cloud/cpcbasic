10 DEFINT a-z: MODE 1:CALL &BD1C: DEF FNk(i)=INKEY(i):DEF FNr(x,y,z)=x+SIN(c/y)*z:locate 10,18:PEN 6:?"S P R I N T - 7Lines"
20 randomize time:ink 0,0:border 0:a=0:pc=2:p=0
30 c=c+2:pc=pc+1:CALL &BD19:a=c mod 16:b=pc mod 14:d=FNr(6,16,1.2)
40 locate FNr(18,14,3),b+1:?"   ":locate FNr(18,14,3),b+2:?" "+chr$(171)+" ";
50 locate d,a+1:pen 9+a mod 4:?"       0           O      ";
60 locate FNr(18,16,1.8),15:j=(1*(FNk(1)-FNk(8)))
70 p=p+j:locate 15+p,14:?" "+chr$(171)+" ":goto 30
