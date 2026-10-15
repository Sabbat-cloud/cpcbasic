5 cls:mode 2:print "Simple RLE Encoder - 2019 by Fabrizio Radica www.retroacademy.it"
10 a$="aaaaaoooooobbbppphheeegggggggeeggggguuuuuuuuu"
100 for n=0 to len(a$)
110 c$=mid$(a$,n+1,1):cnt%=cnt%+1
120 if(c$<>l$) then result$=result$+r$ : cnt%=1
150 conv$=chr$(32+cnt%)
180 l$=c$:r$=conv$+l$
200 next
210 print "----":?
220 print "Original: ":print a$:print
230 print "Compressed" :print result$:print
