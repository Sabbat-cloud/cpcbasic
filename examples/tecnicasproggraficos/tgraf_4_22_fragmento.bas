2072 IF respuesta$="b" THEN GOSUB 4000
3998 REM no marcha si se trata de borrar una linea que no existe
3999 REM ya veremos como se arregla en el proximo programa
4000 x=x(con):y=y(con)
4010 con=con-1
4020 xant=x(con):yant=y(con)
4030 GOSUB 1000
4040 RETURN
