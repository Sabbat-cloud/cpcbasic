1 ' inicio
20 print "Prueba de Sprites personalizados"
30 input "Pulsa ENTER para continuar",a
40 mode 0
100 SYMBOL 240,&X00011000,&X00111100,&X01111110,&X11011011,&X01111110,&X01100110,&X11011011,&X10000001
110 SYMBOL 241,&X00000000,&X00000000,&X00000000,&X00100100,&X00000000,&X00011000,&X00000000,&X00000000
150 print chr$(22)+chr$(1)
160 locate 14,10:print chr$(240)
170 pen 3
180 locate 14,10:print chr$(241)
200 print chr$(22)+chr$(1)

