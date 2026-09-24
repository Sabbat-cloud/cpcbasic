2074 IF respuesta$="i" THEN GOSUB 7000 
2075 IF respuesta$="o" THEN GOSUB 8000 
6000 CLG
6010 xant=1<(1):yant=y(1)
6020 FOR valor=2 TO con
6030   x=x(valor):y=y(valor)
6040   lineadib=l(valor)
6050   GOSUB 1000
6060   xant=x:yant=y
6070 NEXT
6080 x=320:y=200:lineadib=0
6090 RETURN 
7000 MODE 1
7010 PRINT"Carga de datos de un fichero"
7020 INPUT"Nombre del fichero: ";fichero$
7030 OPENIN fichero$
7040 con=0
7050 WHILE NOT EOF
7060   con=con+1
7070   INPUT #9,con),y(con),l(con)
7080 WEND
7090 CLOSEIN 
7100 MODE 0
7110 WINDOW 1,20,25,25
7120 xant=x(con):yant=y(con)
7130 x=xant:y=yant
7140 GOSUB 6000
7150 RETURN 
8000 MODE 1
8010 PRINT"Grabacion de datos en un fichero" 
8020 INPUT"Nombre del fichero: ";fichero$
8030 OPENOUT fichero$
8040 cuenta=0
8050 WHILE cuenta<=con
8060 WRITE #9,x(cuenta),y(cuenta),l(cuenta) 
8070 cuenta=cuenta+1
8080 WEND
8090 CLOSEOUT 
8100 MODE 0
8110 WINDOW 1,20,25,25
8120 GOSUB 6000
8130 RETURN
