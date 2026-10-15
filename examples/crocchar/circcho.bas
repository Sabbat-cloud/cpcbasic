10 ' CONFIG
20 rpi=199 ' plot/draw circle size
30 scpi=1 ' plot/draw precision: higher better
40 scp=3 ' character cos/sin precision: higher better
50 pp=0.3 ' character pythagore precision: lower better
60 louvre=0 ' 0=run the benchmark all the way until the end, 1=stop at each step 
70 ' START
80 DEG:DIM s%(90),c%(90),rt(30),r$(30):ri%=0
90 FOR j=0 TO 2
100 m=j
110 IF m=0 THEN xp=1:yp=2:yo=13:xo=13:r=6:c$="X":ci$="0"
120 IF m=1 THEN xp=1:yp=1:yo=13:xo=21:r=12:c$="X":ci$="0"
130 IF m=2 THEN xp=2:yp=1:yo=13:xo=41:r=12:c$="X":ci$="0"
140 MODE m:r%=8*r
150 'PYTHAGORE
160 CLS:LOCATE 1,1:?"PYTHAGORE":?"MODE ";USING "#";m:ts%=INT(TIME/300):ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" PYTHAGORE "
170 FOR i=0 TO r STEP pp 'Higher step => increase speed / decrease quality
180 xt=SQR(r^2-i^2):yt=i
190 GOSUB 740
200 NEXT i
210 rt(ri%)=(INT(TIME/300)-ts%)
220 IF louvre THEN LOCATE 1,3:?USING "##";rt(ri%):?"SEC":INPUT "",k$
230 'SIN/COS - BEST RESULT
240 CLS:LOCATE 1,1:?"SIN/COS":?"MODE ";USING "#";m:ts%=INT(TIME/300):ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS "
250 FOR n%=0 TO 90 STEP scp 'Higher step => descrease speed / increase quality
260 s%(n%)=SIN(n%)*r%:c%(n%)=COS(n%)*r%
270 xt=s%(n%)/8:yt=c%(n%)/8:GOSUB 740
280 NEXT n%
290 rt(ri%)=(INT(TIME/300)-ts%)
300 IF louvre THEN LOCATE 1,3:?USING "##";rt(ri%):?"SEC":INPUT "",k$
310 'SIN/COS - PRECALC
320 CLS:ts%=INT(TIME/300):LOCATE 1,1:?"SIN/COS":?"PRE CALC":?"MODE ";USING "#";m:ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS PRECALC "
330 FOR n%=0 TO 90 STEP scp 'Higher step => descrease speed / increase quality
340 xt=s%(n%)/8:yt=c%(n%)/8:GOSUB 740
350 NEXT n%
360 rt(ri%)=(INT(TIME/300)-ts%)
370 IF louvre THEN LOCATE 1,4:?USING "##";rt(ri%):?"SEC":INPUT "",k$
380 'SIN/COS - PLOT
390 xop=320:yop=200:ORIGIN xop,yop
400 CLS:ts%=INT(TIME/300):LOCATE 1,1:?"SIN/COS":?"PLOT":?"MODE ";USING "#";m:ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS PLOT "
410 FOR n%=0 TO 360 STEP scpi 'Higher step => increase speed / decrease quality
420 PLOT SIN(n%)*rpi,COS(n%)*rpi
430 NEXT n%
440 rt(ri%)=(INT(TIME/300)-ts%)
450 IF louvre THEN LOCATE 1,4:?USING "##";rt(ri%):?"SEC":INPUT "",k$
460 'SIN/COS - PLOT - par 4
470 CLS:ts%=INT(TIME/300):LOCATE 1,1:?"SIN/COS":?"PLOT 4":?"MODE ";USING "#";m:ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS PLOT 4 "
480 FOR n%=0 TO 90 STEP scpi 'Higher step => increase speed / decrease quality
490 xip=SIN(n%)*rpi:yip=COS(n%)*rpi
500 PLOT xip,yip:PLOT xip,-yip:PLOT -xip,yip:PLOT -xip,-yip
510 NEXT n%
520 rt(ri%)=(INT(TIME/300)-ts%)
530 IF louvre THEN LOCATE 1,4:?USING "##";rt(ri%):?"SEC":INPUT "",k$
540 'SIN/COS - DRAW
550 PLOT xop/8,yop
560 CLS:ts%=INT(TIME/300):LOCATE 1,1:?"SIN/COS":?"DRAW":?"MODE ";USING "#";m:ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS DRAW "
570 FOR n%=0 TO 360 STEP scpi 'Higher step => increase speed / decrease quality
580 DRAW SIN(n%)*rpi,COS(n%)*rpi
590 NEXT n%
600 rt(ri%)=(INT(TIME/300)-ts%)
610 IF louvre THEN LOCATE 1,4:?USING "##";rt(ri%):?"SEC":INPUT "",k$
620 'SIN/COS - DRAW - par 4
630 PLOT xop/8,yop
640 CLS:ts%=INT(TIME/300):LOCATE 1,1:?"SIN/COS":?"DRAW 4":?"MODE ";USING "#";m:ri%=ri%+1:r$(ri%)="MODE "+STR$(m)+" SIN/COS DRAW 4 "
650 FOR n%=0 TO 90 STEP scpi 'Higher step => increase speed / decrease quality
660 xip=SIN(n%)*rpi:yip=COS(n%)*rpi
670 DRAW xip,yip:PLOT xip,-yip:PLOT -xip,yip:PLOT -xip,-yip
680 NEXT n%
690 rt(ri%)=(INT(TIME/300)-ts%)
700 IF louvre THEN LOCATE 1,4:?USING "##";rt(ri%):?"SEC":INPUT "",k$
710 NEXT j
720 CLS:?"REPORT":FOR i=1 TO ri%:?r$(i);"TIME";rt(i);"SEC":NEXT i
730 END
740 'common optimization for character
750 LOCATE xo+xp*xt,yo+yp*yt:?c$;:LOCATE xo+xt,yo+yt:?ci$;
760 LOCATE xo-xp*xt,yo+yp*yt:?c$;:LOCATE xo-xt,yo+yt:?ci$;
770 LOCATE xo-xp*xt,yo-yp*yt:?c$;:LOCATE xo-xt,yo-yt:?ci$;
780 LOCATE xo+xp*xt,yo-yp*yt:?c$;:LOCATE xo+xt,yo-yt:?ci$;
790 RETURN
