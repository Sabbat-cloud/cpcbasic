3000 ORIGIN centrox,centroy
3090 MOVE 0,0:DRAW radio*SIN(comangulo),radio*COS(comangulo),color
3099 REM dibujo del sector
3100 FOR angulo=comangulo TO finangulo STEP incremento
3110   DRAW radio*SIN(angulo),radio*COS(angulo) 
3120 NEXT
