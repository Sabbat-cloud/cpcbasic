10 mode 0: tag
20 border 0
30 graphics paper 0: clg
40 ink 0,1
50 ink 1,2
60 ink 2,5
70 ink 3,8
80 ink 4,17
90 ink 5,16
100 ink 6,15
110 ink 7,12
120 ink 8,0
121 ink 9,25
130 graphics pen 1: top%=324: gosub 400
140 graphics pen 2: top%=280: gosub 400
150 graphics pen 3: top%=236: gosub 400
160 graphics pen 4: top%=192: gosub 400
170 graphics pen 5: top%=144: gosub 400
180 graphics pen 6: top%=96: gosub 400
190 graphics pen 7: top%=48: gosub 400
200 symbol after 32
210 line1%=&x11111111
220 line2%=&x11101111
230 line3%=&x11111111
240 line4%=&x10110101
250 line5%=&x11111111
260 line6%=&x11011101
270 line7%=&x11111111
280 line8%=&x10110111
290 symbol 239, line1%, line2%, line3%, line4%, line5%, line6%, line7%, line8%
300 graphics pen 8: graphics paper 9
310 for x% = 20 to 600 step 40
320 randomize time
330 h%=rnd*7*16:
340 for y%=0 to h% step 16
350 move x%, 66+y%: print chr$(239);
360 next y%
370 next x%
380 call &bb06
390 mode 1: end
400 'Fill horizontal bar.
410 for y%=top% to top%-48 step -4
420 move 0,y%: draw 640,y%
430 next y% 
440 return
450 
