10 m(0)=20*25:m(1)=40*25:m(2)=80*25:c$=CHR$(143)
20 FOR j=0 TO 2
30 CLS:ts=(TIME/300):MODE j:FOR i=1 TO m(j):?c$;:NEXT i:t(j)=(TIME/300)-ts
40 NEXT j
50 cls:FOR j=0 TO 2:?"MODE:";j;m(j);"CHARS TIME";t(j);"PER 1000 CHAR";1000*t(j)/m(j):next j
