10 REM****PROGRAMA SKETCH3DO****
110 s(1,2)=0
800 REM Ahora crea un fichero que contiene los datos
810 OPENOUT n$
815 GOSUB 1200:REM Toma los valores de traslacion
817 PRINT"la cuantia del desplazamiento en X es",xh-xl
818 PRINT"la cuantia del desplazamiento en Y es",yh-yl
819 INPUT"introduzca la cuantia del desplazamiento en Z",zz
820 PRINT #9,na*2
830 FOR i=1 TO na
840 PRINT #9,xp(i)+xtrans
850 PRINT #9,yp(i)+ytrans
860 PRINT #9,-(zz/2)
870 NEXT i
875 REM sobreescribir esta linea
880 FOR i=1 TO na
890 PRINT #9,xp(i)+xtrans
900 PRINT #9,yp(i)+ytrans
910 PRINT #9,(zz/2)
915 REM sobreescribir esta linea
920 NEXT i
930 REM IF s(1,2)=0 THEN s(1,2)=lb
940 PRINT #9,(3*lb)+1
950 FOR i=1 TO lb
960 PRINT #9,ln(1,i),ln(2,i)
965 REM sobreescribir esta linea
970 NEXT i
980 FOR i=1 TO lb
990 PRINT #9,ln(1,i)+na
1000 PRINT #9,ln(2,i)+na
1010 NEXT i
1020 FOR i=1 TO lb
1030 PRINT #9,i
1040 PRINT #9,i+na
1050 NEXT i
1060 PRINT #9,lb+1
1070 PRINT #9,lb+1+na
1080 PRINT #9,lb+2
1090 FOR i=1 to lb
1100 PRINT #9,i
1110 NEXT i
1120 FOR i=1 TO lb
1130 PRINT #9,i+lb
1140 NEXT i
1150 FOR i=1 TO lb+1
1160 PRINT #9,i,i+(2*lb),i+lb,i+(2*lb)+1
1170 NEXT i
1180 PRINT #9,lb:PRINT #9,lb
1185 FOR i=1 TO lb
1190 PRINT #9,4
1192 NEXT i
1194 CLOSEOUT:END
1200 REM Rutina para trasladar los valores X,Y hacia el origen
1205 xl=640:yl=400:xh=0:yh=0
1210 FOR i= 1 TO na
1220 IF xp(i)<xl THEN xl=xp(i)
1230 IF xp(i)>xh THEN xh=xp(i)
1240 IF yp(i)<yl THEN yl=yp(i)
1250 IF yp(i)>yh THEN yh=yp(i)
1260 NEXT i
1270 xtrans=-((xh+xl)/2): ytrans=-((yh+yl)/2): RETURN
