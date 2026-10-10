10 REM****PROGRAMA FICHERO3DO****
20 REM Programa para almacenar datos coordenados
25 CLS
30 INPUT"NOMBRE DEL FICHERO";h$
40 OPENOUT h$
50 INPUT"NUMERO DE PUNTOS";npts
55 WRITE #9,npts
60 PRINT "INTRODUZCA LAS TERNAS X,Y,Z"
70 FOR i=1 TO npts
80 INPUT"X,Y,Z=";x,y,z
90 WRITE #9,x
100 WRITE #9,y
105 WRITE #9,z
110 NEXT i
120 INPUT"NUMERO DE LINEAS";li
130 WRITE #9,li
140 PRINT"Numero de puntos de union"
150 FOR i=1 TO li
160 INPUT "numeros de los puntos de comienzo,final";sn,fi
170 WRITE #9,sn
180 WRITE #9,fi
190 NEXT i
200 REM Ahora toma los datos de las superficies.
210 INPUT"Numero de superficies";nf
215 PRINT #9,nf
220 REM Dimensionamiento de las matrices de superficie
230 DIM fa(12,nf),nl(nf)
240 PRINT"Escriba las lineas que limitan cada superficie, en sentido horario"
260 FOR i=1 TO nf
270 INPUT "Numero de lineas de esta superficie";nlf
275 nl(i)=nlf
280 FOR j=1 TO nlf
290 INPUT"LINEA=";lnum
300 fa(j,i)=lnum
310 PRINT #9,lnum
320 NEXT j
330 REM Ahora llena la matriz con ceros hasta el numero maximo de linea
340 IF nlf=12 THEN 390
350 FOR k=j TO 12
360 fa(k,i)=0
370 PRINT #9,0
380 NEXT k
390 NEXT i
400 REM Ahora almacena la matriz de "lineas por superficie"
410 FOR i=1 TO nf
420 PRINT #9,nl(i)
430 NEXT i
440 CLOSEOUT
450 END
