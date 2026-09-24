2070 IF respuesta$=" " THEN GOSUB 3000:lineadib=colorvisible
2071 IF respuesta$="1" THEN IF lineadib=0 THEN lineadib=colorvisible ELSE lineadib=0
2076 IF respuesta$="c" THEN colorvisible=1+(colorvisible+1) MOD 3
3045 IF lineadib>0 THEN l(con)=colorvisible 
4025 IF lineadib>0 THEN colorvisible=lineadib
