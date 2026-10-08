10 REM **** PROGRAMA TARTA****
20 REM DIBUJA UNA GRAFICA DE TARTA CON ROTULOS EN CUATRO COLORES, EN MODO 1
30 REM ENTRADA DE DATOS
40 CLS:INK 0,13:INK 1,0:INK 2,3:INK 3,7
50 MODE 1
60 PRINT"   Bienvenido al programa TARTA"
65 INPUT"TITULO PRINCIPAL";m$
66 p1=LEN(m$):p1=20-(p1/2)
70 INPUT"Cuantos segmentos deben visualizarse";numero
72 DIM s(numero),h$(numero),punto(numero),cum(numero)
73 total=0:cangulo=0
75 FOR i=1 TO numero
80 INPUT "TITULO DE ESTE SEGMENTO";h$(i)
85 INPUT "VALOR DEL SEGMENTO";s(i)
87 total=total+s(i)
90 NEXT i
100 FOR i=1 TO numero:REM ajusta los angulos para cada segmento
110 cangulo=cangulo+((s(i)/total)*(2*PI))
120 punto(i)=cangulo-(((s(i)/2)/total)*(2*PI))
122 cum(i)=cangulo
130 NEXT i
135 CLS
200 LOCATE p1,1:PRINT m$
205 TAG
220 REM ajusta el tamaño del circulo
230 radio=150
240 xc=320:yc=200
250 a=(2*PI)/100
260 angulo=0
270 x2=xc+radio:y2=yc
280 FOR i=1 TO 100
290 angulo=angulo+a
300 x1=x2:y1=y2
310 x2=xc+radio*COS(angulo)
320 y2=yc+radio*SIN(angulo)
330 MOVE x1,y1
340 DRAW x2,y2
350 NEXT i
400 REM ahora dibuja los segmentos
405 n=-1
410 FOR i=1 TO numero
415 n=n+1:IF n=4 THEN n=0
420 MOVE xc,yc
430 x1=xc+radio*COS(cum(i))
440 y1=yc+radio*SIN(cum(i))
450 DRAW x1,y1
460 x2=xc+(radio/2)*COS(punto(i))
470 y2=yc+(radio/2)*SIN(punto(i))
472 disp=LEN(h$(i))+15
475 MOVE x2,y2
480 FILL n
482 IF x2<xc THEN disp=disp+10
485 MOVE x2-disp,y2
487 PRINT h$(i);
490 NEXT i
