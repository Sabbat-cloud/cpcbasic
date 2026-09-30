5 rem draws a fractal line in Locomotive basic 1.1
10 mode 1
20 paper 0
30 pen 1
40 cls
50 L = 10
60 I = 10
70 rem ink 1, 0
100 gosub 1000
900 stop
1000 rem draws curve
1001 move 320, 200
1010 while I > 0
1030 gosub 2000
1040 gosub 3000
1050 gosub 4000
1060 gosub 5000
1090 gosub 10000 
1100 I = I - 1
1150 cls
1200 WEND
1500 return
2000 rem draws left
2010 if I = 0 then goto 2070 
2020 I = I - 1
2030 gosub 5000 
2040 gosub 2000
2050 gosub 3000
2060 I = I + 1
2070 drawr 0, -L
2500 return
3000 rem draws bottom
3010 if I = 0 then goto 3090 
3020 I = I - 1
3030 gosub 2000
3040 gosub 3000
3050 gosub 4000
3060 I = I + 1
3090 drawr L, 0
3500 return
4000 rem draws right
4010 if I = 0 then goto 4070 
4020 I = I - 1
4030 gosub 3000
4040 gosub 4000
4050 gosub 5000
4060 I = I + 1
4070 drawr 0, L
4500 return
5000 rem draws top
5010 if I = 0 then goto 5070 
5020 I = I - 1
5030 gosub 4000 
5040 gosub 5000
5050 gosub 2000 
5060 I = I + 1
5070 drawr -L, 0
5090 return
10000 rem waits for a while
10010 starttime = time
10020 while (time - starttime < 500) 
10030 wend
10040 return
