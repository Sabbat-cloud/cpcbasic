10 REM ****PROGRAMA MINITARTA****
20 REM Esta modificación dibuja 12 minitartas que sirven para comparar
30 REM los balances durante un periodo de 12 meses
40 REM Cada tarta se rotula con un código de una sola letra
45 REM Para una resolucion mas elevada, se utiliza el modo 2
50 REM Entrada de datos
60 CLS:INK 0,13:INK 1,0
70 MODE 2
80 PRINT" VENTAS RELATIVAS DE LAS LINEAS DE PRODUCTOS A-E DURANTE DOCE MESE"
90 READ numero
100 DIM s(numero,12),h$(numero),punto(numero,12),cum(numero,12),total(12)
110 total=0:cangulo=0
120 FOR i=1 TO numero
130 READ h$(i)
140 REM Los datos de cada mes estan al final del programa
150 REM num de segmentos, codigo del titulo, valores del segmento - para cada uno
160 NEXT i
170 FOR i=1 TO 12
180 FOR ip=1 TO numero
190 READ s(ip,i):total(i)=total(i)+s(ip,i):NEXT ip:NEXT i
200 GOSUB 680:REM ahora escribe los meses
210 TAG
220 REM ahora dibuja las doce tartas
230 xc=0:yc=319:REM centro de la primera tarta
240 FOR ip=1 TO 12:REM comienzo del bucle para las doce tartas
250 FOR i=1 TO numero:REM ajusta los angulos para cada segmento
260 cangulo=cangulo+((s(i,ip)/total(ip))*(2*PI))
270 punto(i,ip)=cangulo-(((s(i,ip)/2)/total(ip))*(2*PI))
280 cum(i,ip)=cangulo
290 NEXT i
300 REM ajusta el tamaño del circulo
310 radio=45
320 xc=xc+127:IF xc>=605 THEN xc=125:yc=yc-110:REM empieza nueva fila
330 a=(2*PI)/100
340 angulo=0
350 x2=xc+radio:y2=yc
360 FOR i=1 TO 103
370 angulo=angulo+a
380 x1=x2:y1=y2
390 x2=xc+radio*COS(angulo)
400 y2=yc+radio*SIN(angulo)
410 MOVE x1,y1
420 DRAW x2,y2
430 NEXT i
440 REM ahora dibuja el segmento
450 n=-1
460 FOR i=1 TO numero
470 n=n+1:IF n=4 THEN n=0
480 MOVE xc,yc
490 x1=xc+radio*COS(cum(i,ip))
500 y1=yc+radio*SIN(cum(i,ip))
510 DRAW x1,y1
520 x2=xc+(radio/2)*COS(punto(i,ip))
530 y2=yc+(radio/2)*SIN(punto(i,ip))
540 MOVE x2,y2+6
550 IF INT(i/2)=i/2 THEN FILL 1
560 NEXT i
570 REM ahora dibuja los titulos
580 n=-1
590 FOR i=1 TO numero
600 n=n+1:IF n=4 THEN n=0
610 x1=xc+(radio/2)*COS(punto(i,ip))
620 y1=yc+(radio/2)*SIN(punto(i,ip))
630 MOVE x1,y1+6
640 PRINT h$(i);
650 NEXT i
660 NEXT ip
670 |COPY:END
680 REM dibuja el mes
690 LOCATE 9,9:PRINT"      ENE            FEB            MAR"
700 LOCATE 9,16:PRINT"      MAY            JUN            JUL            AGO"
710 LOCATE 9,23:PRINT"      SEP            OCT            NOV"
720 RETURN
730 DATA 5:REM
740 DATA "A","B","C","D","E"
750 DATA 20,20,20,20,20:REM ENE
760 DATA 30,10,15,40,12:REM FEB
770 DATA 10,15,30,20,10:REM MAR
780 DATA 12,12,34,12,10:REM ABR
790 DATA 14,31,12,10,19:REM MAY
800 DATA 15,31,12,8,19:REM JUN
810 DATA 13,13,14,15,12:REM JUL
820 DATA 22,15,10,12,18:REM AGO
830 DATA 15,13,10,13,17:REM SEP
840 DATA 14,41,13,24,13:REM OCT
850 DATA 5,12,13,15,13:REM NOV
860 DATA 11,21,31,8,13:REM DIC
