10 'INIT
20 patnb%=17:patcharnb%=3:DIM pat%(patnb%,patcharnb%)
50 FOR i=0 TO patnb%
60 FOR j=0 TO patcharnb%
70 pat%(i,j)=32
80 NEXT j
90 NEXT i
100 curpat%=0:gc$="X":m%=2:MODE m%
130 SYMBOL AFTER 0:MEMORY (HIMEM-1)
140 'MAIN MENU
150 CLS:startchar%=0
170 ?"-------------------"
180 ?"|    CrocChar     |"
190 ?"-------------------"
200 ?
210 ?"-------------------"
220 ?"RET QUICK LIST"
230 ?"-------------------"
240 ?"1   TYPE CHAR"
250 ?"2   TYPE CHAR(NUM)"
260 ?"-------------------"
270 ?"21  PATTERN"
280 ?"22  SHOWTIME!"
290 ?"-------------------"
300 ?"31 EXPORT 32 IMPORT"
310 ?"-------------------"
320 ?"41  MODE"
330 ?"42  QUIT"
340 ?"-------------------"
350 ?"66  GNU LICENSE"
360 ?"-------------------"
370 ?
380 INPUT "YOUR CHOICE: ",sel
390 IF sel=0 THEN GOSUB 2140
400 IF sel=1 THEN GOSUB 500
410 IF sel=2 THEN c$="":GOSUB 530
420 IF sel=21 THEN c$="":GOSUB 2790
430 IF sel=22 THEN ?:INPUT "AUTO(0) or KEY(1) mode?",showmode:GOSUB 3320
440 IF sel=31 THEN c$="":GOSUB 3490
450 IF sel=32 THEN c$="":GOSUB 3630
460 IF sel=41 THEN ?:INPUT "MODE (0,1,2): ",m%:MODE m%
470 IF sel=42 THEN END
480 IF sel=66 THEN pm%=m%:m%=2:MODE m%:GOSUB 2620:m%=pm%:MODE m%
490 GOTO 150
500 'MAIN CHARACTER MENU
510 c$=""
520 ?:INPUT "CHARACTER: ",c$
530 IF c$="" THEN c$=" ":?:INPUT "CHAR NUMBER:",cnum% ELSE cnum%=ASC(c$)
540 c$=CHR$(cnum%)
550 l=1
560 FOR n=HIMEM+cnum%*8+1 TO HIMEM+cnum%*8+8
570 lt(l)=PEEK(n)
580 plt(l)=lt(l)
590 l=l+1
600 NEXT n
610 'PLAY WITH CHARACTER
620 CLS:ft=1:startcol%=24
630 IF m%=2 and ft=1 THEN GOSUB 3150:ft=0 
640 SYMBOL cnum%,lt(1),lt(2),lt(3),lt(4),lt(5),lt(6),lt(7),lt(8)
650 'HEADER
660 locate 1,1
670 ?"DEC ";
680 IF m%>0 THEN ?" ";
690 ?" GRAPH ";
700 IF m%>0 THEN ?" ";
710 ?" BIN";
720 ?DEC$(cnum%,"###")" ";
730 ?CHR$(1)c$
740 ?"--------------------";
750 IF m%>0 THEN ?"--" ELSE ?
760 'DISPLAY DEC
770 FOR n=1 TO 8
780 a=lt(n)
790 ?DEC$(a,"###")" ";
800 IF m%>0 THEN ?" ";
810 'DISPLAY GRAPHIC
820 FOR b=7 TO 0 STEP -1
830 IF (a AND 2^b)=2^b THEN ?gc$; ELSE ?" ";
840 NEXT b
850 '?" ";
860 IF m%>0 THEN ?" ";
870 'DISPLAY BIN
880 FOR b=7 TO 0 STEP -1
890 IF (a AND 2^b)=2^b THEN ?"1"; ELSE ?"0";
900 NEXT b
910 IF m%>0 THEN ?
920 l=l+1
930 NEXT n
940 ?
950 ?"1-UPSIDE  ";
960 ?"2-SIDE   "
970 ?"3-ROTATE  ";
980 ?"4-INVERT "
990 ?"5-BIN     ";
1000 ?"6-DEC    "
1010 ?"11-EMPTY  ";
1020 ?"12-COPY"
1030 ?"13-TABLE  ";
1040 ?"14-HELP  "
1050 ?"21-ODEC   ";
1060 ?"22-OBIN  "
1070 ?"31-MODE   ";
1080 ?"32-GRAPH "
1090 ?"41-CANCEL ";
1100 ?"RET-BACK "
1110 locate 1,23:?"                    ":?"                    ";:locate 1,23
1120 k$=""
1130 input "YOUR CHOICE:",k$
1140 'Return to Menu 
1150 IF k$="" THEN RETURN
1160 'Turn character upside/down
1170 IF k$="1" THEN GOSUB 1550
1180 'Turn the character sideway
1190 IF k$="2" THEN GOSUB 1870
1200 'Rotate the character
1210 IF k$="3" THEN GOSUB 2010
1220 'Invert colors
1230 IF k$="4" THEN GOSUB 1960
1240 'Edit character binary
1250 IF k$="5" THEN GOSUB 1630
1260 'Edit character decimals values
1270 IF k$="6" THEN GOSUB 1730
1280 'Wipe the character
1290 IF k$="11" THEN FOR i=1 TO 8:lt(i)=0:NEXT i
1300 'Copy another character
1310 IF k$="12" THEN INPUT "CHAR(NUM): ",sc%:GOSUB 1480
1320 'Display character set
1330 IF k$="13" AND m%<2 THEN pm%=m%:m%=2:MODE m%:GOSUB 2140:m%=pm%:MODE m%
1340 IF k$="13" AND m%=2 THEN GOSUB 3150
1350 'Display help
1360 IF k$="14" THEN pm%=m%:m%=2:MODE m%:GOSUB 2360:m%=pm%:MODE m%
1370 'Display character decimals values
1380 IF k$="21" THEN ft=0:GOSUB 1770
1390 'Display character binary
1400 IF k$="22" THEN ft=1:GOSUB 1770
1410 'Change display mode
1420 IF k$="31" THEN INPUT "MODE (0,1,2): ",m%:MODE m%
1430 'Change the character used to display a pixel
1440 IF k$="32" THEN INPUT "CHAR(NUM): ",gc%:gc$=CHR$(gc%)
1450 'Cancel all changes
1460 IF k$="41" THEN FOR i=1 TO 8:lt(i)=plt(i):NEXT i
1470 GOTO 640
1480 'COPY
1490 ll=1
1500 FOR n=HIMEM+sc%*8+1 TO HIMEM+sc%*8+8
1510 lt(ll)=PEEK(n)
1520 ll=ll+1
1530 NEXT n
1540 RETURN
1550 'UP/DOWN MIRROR
1560 FOR i=1 TO 8
1570 tlt(i)=lt(8-i+1)
1580 NEXT i
1590 FOR i=1 TO 8
1600 lt(i)=tlt(i)
1610 NEXT i
1620 RETURN
1630 'EDIT BINARY LINE
1640 INPUT "PICK LINE: ",pl
1650 INPUT "VALUE/BIN: ",v$
1660 nb=0
1670 FOR i=1 TO 8
1680 j$=MID$(v$,i,1)
1690 IF j$="1" OR j$="X" THEN nb=nb+2^(8-i)
1700 NEXT i
1710 lt(pl)=nb
1720 RETURN
1730 'EDIT DEC LIST(,)
1740 INPUT "DEC(8) SPLIT by ,: ",p1,p2,p3,p4,p5,p6,p7,p8
1750 lt(1)=p1:lt(2)=p2:lt(3)=p3:lt(4)=p4:lt(5)=p5:lt(6)=p6:lt(7)=p7:lt(8)=p8
1760 RETURN
1770 'OUTPUT DEC/BIN
1780 CLS
1790 FOR i=1 TO 8
1800 IF ft=0 THEN ?STR$(lt(i)); ELSE ?"&X"BIN$(lt(i));
1810 IF i<>8 THEN ?",";
1820 NEXT i
1830 ?
1840 ?
1850 INPUT "PRESS KEY!",k
1860 RETURN
1870 'SIDE MIRROR
1880 FOR n=1 TO 8
1890 t=0
1900 FOR b=0 TO 7
1910 IF (lt(n) AND 2^b)=2^b THEN t=t+2^(7-b)
1920 NEXT b
1930 lt(n)=t
1940 NEXT n
1950 RETURN
1960 'INVERT
1970 FOR n=1 TO 8
1980 lt(n)=lt(n) XOR 255
1990 NEXT n
2000 RETURN
2010 'ROTATE
2020 FOR n=1 TO 8
2030 tlt(n)=0
2040 NEXT n
2050 FOR n=1 TO 8
2060 FOR b=0 TO 7
2070 IF (lt(n) AND 2^b)=2^b THEN tlt(b+1)=tlt(b+1)+2^(n-1)
2080 NEXT b
2090 NEXT n
2100 FOR i=1 TO 8
2110 lt(i)=tlt(i)
2120 NEXT i
2130 RETURN
2140 'QUICK CHAR SEARCH
2150 S=25
2160 IF m%=0 THEN S=5:L=10
2170 IF m%=1 THEN S=12:L=10
2180 IF m%=2 THEN S=25:L=25
2190 LC=0:PRINT ""
2200 FOR I=0 TO 255 STEP S
2210 IF m%=0 AND LC=0 THEN CLS:PRINT "L/C|00|01|02|03|04";
2220 IF m%=1 AND LC=0 THEN CLS:PRINT "L/C|00|01|02|03|04|05|06|07|08|09|10|11";
2230 IF m%=2 AND LC=0 THEN CLS:PRINT "L/C|00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24";
2240 IF m%=0 THEN PRINT "---|--|--|--|--|--"
2250 IF m%=1 THEN PRINT "---|--|--|--|--|--|--|--|--|--|--|--|--"
2260 IF m%=2 THEN PRINT "---|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--"
2270 PRINT "";USING "###";I;
2280 FOR J=0 TO S-1
2290 IF I+J<256 THEN PRINT "| ";CHR$(1);CHR$(I+J);
2300 NEXT J
2310 LC=LC+1
2320 IF LC>L OR I+J>255 THEN LC=0:PRINT "":?"---------":INPUT "PRESS KEY",k
2330 NEXT I
2340 PRINT ""
2350 RETURN
2360 'HELP
2370 ?"1-UPSIDE : Mirror the character upside down"
2380 ?"2-SIDE   : Mirror the character side way"
2390 ?"3-ROTATE : Simple character rotation"
2400 ?"4-INVERT : Invert the character, 0<->1"
2410 ?"5-BIN    : Edit one given character binary line."
2420 ?"           1 or X will be understood as 1 value."
2430 ?"           Any other character will be understood as 0."
2440 ?"           You need to input exactly 8 characters."
2450 ?"6-DEC    : Edit the complete character giving a series of"
2460 ?"           8 Decimal values separated by a comma (,)."
2470 ?"           Each value has to be between 0 and 255"
2480 ?"11-EMPTY : Make the character blank"
2490 ?"12-COPY  : Copy a character by giving the character source decimal value"
2500 ?"           Value has to be between 0 and 255"
2510 ?"13-TABLE : Show character set"
2520 ?"14-HELP  : Display this help"
2530 ?"21-ODEC  : Display character decimal values"
2540 ?"22-OBIN  : Display character binary values in Basic format"
2550 ?"31-MODE  : Change the display mode (0,1,2)"
2560 ?"32-GRAPH : Change the character used to paint the character."
2570 ?"           Value has to be between 0 and 255"
2580 ?"41-CANCEL: Cancel all changes done."
2590 ?"           All changes will be permanent if you return to main menu."
2600 ?"---------":INPUT "PRESS KEY",k
2610 RETURN
2620 'LICENSE
2630 ?"CROCOCHAR: Amstrad Basic character editor"
2640 ?"Copyright (C) 2023  Cyril Raphanel"
2650 ?
2660 ?"This program is free software: you can redistribute it and/or modify"
2670 ?"it under the terms of the GNU General Public License as published by"
2680 ?"the Free Software Foundation, version 3 of the License."
2690 ?
2700 ?"This program is distributed in the hope that it will be useful,"
2710 ?"but WITHOUT ANY WARRANTY; without even the implied warranty of"
2720 ?"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
2730 ?"GNU General Public License for more details."
2740 ?
2750 ?"Copy of the GNU General Public License"
2760 ?"see <https://www.gnu.org/licenses/>. "
2770 ?"---------":INPUT "PRESS KEY",k
2780 RETURN
2790 'PATTERN
2800 CLS:ft=1:k$=""
2810 if m%=2 then locate 1,1 else CLS
2820 FOR i=0 TO patnb%
2830 if pat%(i,0)=32 AND pat%(i,1)=32 AND pat%(i,2)=32 AND pat%(i,2)=32 then chkm$="_" else chkm$="X"  
2840 IF i=curpat% THEN PAPER 1:PEN 0:?chkm$:PAPER 0:PEN 1 ELSE ?chkm$
2850 NEXT i
2860 FOR i=0 TO 3
2870 IF i=0 OR i=1 THEN li=1 ELSE li=9
2880 IF i=0 OR i=2 THEN co=3 ELSE co=11
2890 FOR n=HIMEM+pat%(curpat%,i)*8+1 TO HIMEM+pat%(curpat%,i)*8+8
2900 LOCATE co,li
2910 o=PEEK(n)
2920 FOR b=7 TO 0 STEP -1
2930 IF (o AND 2^b)=2^b THEN ?gc$; ELSE ?" ";
2940 NEXT b
2950 li=li+1:?
2960 NEXT n
2970 NEXT i
2980 LOCATE 1,19
2990 ?"-------------------"
3000 ?CHR$(1)CHR$(pat%(curpat%,0))CHR$(1)CHR$(pat%(curpat%,1))"|"DEC$(pat%(curpat%,0),"###")" "DEC$(pat%(curpat%,1),"###")"|"
3010 ?CHR$(1)CHR$(pat%(curpat%,2))CHR$(1)CHR$(pat%(curpat%,3))"|"DEC$(pat%(curpat%,2),"###")" "DEC$(pat%(curpat%,3),"###")"|"
3020 ?"-------------------"
3030 ?"1-NEX 2-EDI 3-PRE"
3040 ?"4-TAB 5-HEL 6-EXI"
3050 startcol%=20
3060 IF m%=2 and ft=1 THEN GOSUB 3150:ft=0
3070 k$="":i=curpat%
3080 while k$="":k$=INKEY$:wend
3090 IF k$="1" AND curpat%<patnb% THEN curpat%=curpat%+1 ELSE curpat%=0
3100 IF k$="3" AND i>0 THEN curpat%=i-1
3110 IF k$="2" THEN locate 1,23:?"                   ":?"                   ":locate 1,23:INPUT "V:",pat%(i,0),pat%(i,1),pat%(i,2),pat%(i,3):curpat%=i
3120 IF k$="4" THEN ft=1:pm%=m%:m%=2:MODE m%:GOSUB 2140:m%=pm%:MODE m%
3130 IF k$="6" THEN RETURN
3140 GOTO 2810
3150 'TABLE LIST / MODE 2
3160 curline%=1
3170 maxlinemod2%=25
3180 curcol%=startcol%
3190 LOCATE curcol%,curline%
3200 FOR i%=startchar% TO 255
3210 curlen%=4:curstr$="#"
3220 IF i%>9 AND i%<100 THEN curlen%=5:curstr$="##"
3230 IF i%>99 THEN curlen%=6:curstr$="###"
3240 IF (curcol%+curlen%)>80 THEN curline%=curline%+1:curcol%=startcol%
3250 if curline%>maxlinemod2% then startchar%=i%:return else LOCATE curcol%,curline%
3260 ?DEC$(i%,curstr$);
3270 curcol%=curcol%+curlen%
3280 ?":"CHR$(1)CHR$(i%)"|";
3290 NEXT i%
3300 startchar%=0
3310 RETURN
3320 'SHOWTIME
3330 for j=0 to 2
3340 mode j
3350 for i=0 to 255
3360 'DISPLAY GRAPHIC
3370 CLS
3380 FOR n=HIMEM+i*8+1 TO HIMEM+i*8+8
3390 a=PEEK(n)
3400 FOR b=7 TO 0 STEP -1
3410 IF (a AND 2^b)=2^b THEN ?CHR$(1)CHR$(i); ELSE ?" ";
3420 NEXT b
3430 ?
3440 NEXT n
3450 if showmode=1 then INPUT "PRESS KEY!",k
3460 next i
3470 next j
3480 return
3490 'EXPORT
3500 INPUT "File Name: ",fin$
3510 finn$=fin$+".LIB"
3520 OPENOUT finn$
3530 for i=0 to 255 
3540 l=1
3550 FOR n=HIMEM+i*8+1 TO HIMEM+i*8+8
3560 lt(l)=PEEK(n)
3570 l=l+1
3580 NEXT n
3590 WRITE #9,i,lt(1),lt(2),lt(3),lt(4),lt(5),lt(6),lt(7),lt(8)
3600 next i
3610 CLOSEOUT
3620 return
3630 'IMPORT
3640 INPUT "File Name: ",fin$
3650 OPENIN fin$
3660 WHILE NOT EOF
3670 INPUT #9,i%,lt%(1),lt%(2),lt%(3),lt%(4),lt%(5),lt%(6),lt%(7),lt%(8)
3680 SYMBOL i%,lt%(1),lt%(2),lt%(3),lt%(4),lt%(5),lt%(6),lt%(7),lt%(8)
3690 WEND
3700 CLOSEIN
3710 return
