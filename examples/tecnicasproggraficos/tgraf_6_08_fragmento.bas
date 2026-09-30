4080 IF respuesta$="i" THEN GOSUB 11000 
4090 IF respuesta$="o" THEN GOSUB 12000
10999 REM abrir una ventana que no estropee el dibujo
11000 WINDOW 1,20,24,25:PEN 1
11010 PRINT "Para carga"
11020 INPUT "nombre: ";dibujo$
11030 LOAD dibujo$
11040 CLS
11049 REM de nuevo la pantalla normal
11050 WINDOW 1,20,1,25 
11060 GOSUB 1000
11070 RETURN
12000 WINDOW 1,20,24,25:PEN 1
12010 PRINT "Para grabacion"
12020 INPUT "nombre: ";dibujo$
12029 REM almacenamiento de la pantalla
12030 SAVE dibujo$,b,&C000,&3FCF
12040 CLS
12050 WINDOW 1,20,1,25 
12055 rell=0:GOSUB 7030 
12060 GOSUB 1000
12070 RETURN
