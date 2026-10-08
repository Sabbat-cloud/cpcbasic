10 REM****PROGRAMA OCULTAS2-PARA USAR CON S3DO****
200 lt=(li-1)/3
205 FOR i=1 TO lt
210 INPUT#9,fa(i,1)
215 NEXT i
220 FOR i=1 TO lt
225 INPUT#9,fa(i,2)
230 NEXT i
235 FOR i=3 TO nf
240 INPUT#9,fa(1,i),fa(2,i),fa(3,i),fa(4,i)
245 NEXT i
250 nl(1)=lt:nl(2)=lt
255 FOR i=3 TO nf
260 nl(i)=4
270 NEXT i
