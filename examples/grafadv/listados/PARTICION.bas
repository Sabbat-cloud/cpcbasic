10 REM ****PROGRAMA PARTICION****
20 REM DIBUJA UNA TARTA CON ROTULOS EN CUATRO COLORES EN MODO 1
22 REM CON UNA SECCION SEGREGADA ESCOGIDA POR EL USUARIO
30 REM ENTRADA DE DATOS
40 CLS:INK 0,13:INK 1,0:INK 2,6:INK 3,12:MODE 1
60 PRINT"   Bienvenido al programa TARTA"
70 INPUT"NUMERO DE SEGMENTOS A VISUALIZAR";numero
80 INPUT "NUMERO DEL SEGMENTO A SEGREGAR";particion
90 IF particion=numero THEN PRINT"NO PUEDE SEGREGARSE EL ULTIMO SEGMENTO":PRINT"EMPIECE OTRA VEZ":GOTO 80
100 DIM s(numero),h$(numero),punto(numero),cum(numero)
110 total=0:cangulo=0
120 FOR i=1 TO numero
130 PRINT"ESCRIBA EL TITULO DEL SEGMENTO ";i:INPUT h$(i)
140 INPUT"VALOR DEL SEGMENTO";s(i)
150 total=total+s(i)
160 NEXT i
170 TAG
180 FOR i=1 TO numero:REM ajusta los angulos para cada segmento
190 cangulo=cangulo+((s(i)/total)*(2*PI))
200 punto(i)=cangulo-(((s(i)/2)/total)*(2*PI))
210 cum(i)=cangulo
220 NEXT i
230 CLS
240 REM ajusta el tamaño del circulo
250 radio=150
260 xc=320:yc=200
270 a=(2*PI)/300
280 angulo=0
290 x2=xc+radio:y2=yc
300 fl1=0:fl2=0:REM ajusta las banderas indicadoras del segmento segregado
310 FOR i=0 TO 300
320 angulo=angulo+a
330 x1=x2:y1=y2
340 IF angulo>=cum(particion-1) AND fl1=0 THEN GOSUB 630:REM segrega el segmento
350 IF angulo>=cum(particion) AND fl2=0 THEN MOVE xc,yc:DRAW x1,y1
360 IF angulo>=cum(particion) AND fl2=0 THEN xc=xhold:yc=yhold
370 x2=xc+radio*COS(angulo)
380 y2=yc+radio*SIN(angulo)
390 IF angulo>=cum(particion-1) AND fl1=0 THEN x1=x2:y1=y2
400 IF angulo>=cum(particion-1) AND fl1=0 THEN MOVE xc,yc:DRAW x2,y2:fl1=1
410 IF angulo>=cum(particion) AND fl2=0 THEN angulo=angulo-a: x1=x2: y1=y2: fl2=1:GOTO 330
420 MOVE x1,y1
430 DRAW x2,y2
440 NEXT i
450 REM ahora dibuja los segmentos
460 n=-1
470 FOR i=1 TO numero
480 n=n+1:IF n=4 THEN n=0
490 MOVE xc,yc
500 x1=xc+radio*COS(cum(i))
510 y1=yc+radio*SIN(cum(i))
520 DRAW x1,y1
530 x2=xc+(radio/2)*COS(punto(i))
540 y2=yc+(radio/2)*SIN(punto(i))
550 disp=LEN(h$(i))*3
560 MOVE x2,y2
570 FILL n
580 IF x2<xc THEN disp=disp*4
590 MOVE x2-disp,y2
600 NEXT i
610 GOSUB 700:REM Pone los títulos
615 |COPY:END
630 REM calcula las coordenadas del centro para el sector segregado
640 REM primero calcula la direccion del angulo
650 bis=((cum(particion)-cum(particion-1))/2)+cum(particion-1)
660 xhold=xc:yhold=yc:REM almacena los valores normales del centro
670 xc=xhold+20*COS(bis)
680 yc=yhold+20*SIN(bis)
690 RETURN
700 REM ahora dibuja los titulos
710 n=-1
720 FOR i=1 TO numero
730 n=n+1:IF n=4 THEN n=0
740 MOVE xc,yc
750 x1=xc+radio*COS(cum(i))
760 y1=yc+radio*SIN(cum(i))
770 DRAW x1,y1
780 x2=xc+(radio/2)*COS(punto(i))
790 y2=yc+(radio/2)*SIN(punto(i))
800 disp=LEN(h$(i))*3
810 MOVE x2,y2
820 IF x2<xc THEN disp=disp*4
830 MOVE x2-disp,y2
840 PRINT h$(i);
850 NEXT i
870 RETURN
