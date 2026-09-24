10 MODE 1
20 numero=1
30 WHILE numero>0
40   INPUT "Teclee el numero decimal ";numero
50   PRINT "Este es el numero binario "BIN$(numero)
54   REM VAL convierte una cadena literal en un numero
55   numerico=VAL(BIN$(numero))
56   PRINT "Este es el numero ";numerico
60 WEND
