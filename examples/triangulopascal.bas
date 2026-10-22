10 rem triangulo de pascal
20 defint h,p,q
30 h = 0:while h<=0:input "altura(maximo 9)";h:wend
40 dim b(h,h+1)
50 for p=0 to h:z=1:m=p
60 for q=1 to p+1:b[p,q]=z
70 z=z*m/q: m=m-1
80 next q,p
90 cls:print:print
100 for p=0 to h:print space$(18-p*2);
110 for q=1 to p+1:a$=str$(b[p,q])
120 print space$(4-len(a$));a$;:next q:print
130 print:next p
