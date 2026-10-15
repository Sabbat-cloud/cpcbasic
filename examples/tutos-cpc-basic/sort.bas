10 'PEOPLE LIST SORTED BY BIRTH YEAR'
20 mode 2
30 t0 = time
40 maxpeople=10
50 dim people$(maxpeople,3)
60 restore 420
70 'READ DATA INTO ARRAY
80 for i=1 to maxpeople
90 read firstname$, lastname$, birthyear%
100 people$(i,0)=firstname$
110 people$(i,1)=lastname$
120 people$(i,2)=str$(birthyear%)
130 next
140 'DISPLAY HEADER
150 print "FIRSTNAME","LASTNAME","BIRTH " + chr$(241)
160 print "---------","--------","-------"
170 'CALL SORT
180 gosub 270
190 'DISPLAY DATA
200 for i=1 to maxpeople
210 print people$(i,0), people$(i,1), people$(i,2)
220 next
230 t=(TIME-t0)/300
240 print string$(33, "-")
250 print "Execution : ";t;"sec"
260 end
270 'SORT LOGIC
280 for i = 1 to maxpeople
290 currentyear = val(people$(i,2))
300 for j = 1 to maxpeople
310 nextyear = val(people$(j,2))
320 if currentyear < nextyear then gosub 360
330 next j
340 next i
350 return
360 'SWAP ROWS
370 tmp0$=people$(i,0): tmp1$=people$(i,1): tmp2$=people$(i,2)
380 people$(i,0)=people$(j,0): people$(i,1)=people$(j,1): people$(i,2)=people$(j,2)
390 people$(j,0)=tmp0$: people$(j,1)=tmp1$: people$(j,2)=tmp2$
400 return
410 'DATA'
420 data Fabrice,Kauffmann,1972
430 data Isaac,Newton,1643
440 data Albert,Einstein,1879
450 data Neil,Armstrong,1930
460 data Buzz,Aldrin,1930
470 data Keanu,Reeves,1964
480 data Patrick,Stewart,1940
490 data Fidel,Castro,1926
500 data Yasser,Arafat,1929
510 data Philip K.,Dick,1928
520 
