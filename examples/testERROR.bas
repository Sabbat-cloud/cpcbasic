100 ps%=1:maxit%=15:colesc%=1:INK 1,26:colunclear%=0:INK 0,13
102 MODE 1:CLS:LOCATE 1,1
104 PRINT"reliable exterior Mandelbrot z^2+c IA"
106 PRINT"Marc Meidlinger, March-April 2022"
108 PRINT"Locomotive Basic Schneider CPC 464"
110 IF ps%>0 THEN PRINT"pointSampling" ELSE PRINT"pixel with area"
112 DIM bigOA$(9)
114 fpi%=24:fpf%=8
116 bip%=2*(fpi%+fpf%)+1
118 IF bip%>250 THEN PRINT"err1":END
120 epss=1:epsi$="0":epsf$="1"
122 FOR i%=1 TO (fpf%-1):epsf$="0"+epsf$:NEXT
124 fpaddflag=0:REM 30400
126 fppaddingflag=0:REM 31400
128 fpaddabsflag=0:REM 31600
130 fpabsvglflag=0:REM 31800
132 fpsubabsagrglbflag=0:REM 32200
134 bigintmulflag=0:REM 32800
136 bigintposaddflag=0:REM 32600
138 fpmulflag=0:REM 33000
140 fpiaaddflag=0:REM 34000
142 fpiamulflag=0:REM 34900
144 fpvglflag=0:REM 35200
146 fpiasubflag=0:REM 38200
148 REM tiling
150 cx0s=-1:cx0i$="2":cx0f$="0"
152 cx1s=cx0s:cx1i$=cx0i$:cx1f$=cx0f$
154 cy0s=-1:cy0i$="2":cy0f$="0"
156 cy1s=cy0s:cy1i$=cy0i$:cy1f$=cy0f$
158 pixh0s=0:pixh0i$="0":pixh0f$="0"
160 pixh1s=1:pixh1i$="0"
162 ye%=50:pixh1f$="08"
164 pixw0s=0:pixw0i$="0":pixw0f$="0"
166 pixw1s=1:pixw1i$="0"
168 xe%=50:pixw1f$="08"
170 IF ps%<=0 THEN GOTO 190
172 pixw0s=pixw1s:pixw0i$=pixw1i$:pixw0f$=pixw1f$
174 pixh0s=pixh1s:pixh0i$=pixh1i$:pixh0f$=pixh1f$
190 PRINT"width =";pixw0i$;".";pixw0f$;"..";pixw1i$;".";pixw1f$
192 PRINT"height=";pixh0i$;".";pixh0f$;"..";pixh1i$;".";pixh1f$
194 yendH%=ye% \ 2
196 cybase0s=cy0s:cybase0i$=cy0i$:cybase0f$=cy0f$
198 cybase1s=cy1s:cybase1i$=cy1i$:cybase1f$=cy1f$
200 cxbase0s=cx0s:cxbase0i$=cx0i$:cxbase0f$=cx0f$
202 cxbase1s=cx1s:cxbase1i$=cx1i$:cxbase1f$=cx1f$
204 FOR xloop%=1 TO xe%
206 cx0s=cx1s:cx0i$=cx1i$:cx0f$=cx1f$
208 fpiaaddA0s=cx0s:fpiaaddA0i$=cx0i$:fpiaaddA0f$=cx0f$
210 fpiaaddA1s=cx1s:fpiaaddA1i$=cx1i$:fpiaaddA1f$=cx1f$
212 fpiaaddB0s=pixw0s:fpiaaddB0i$=pixw0i$:fpiaaddB0f$=pixw0f$
214 fpiaaddB1s=pixw1s:fpiaaddB1i$=pixw1i$:fpiaaddB1f$=pixw1f$
216 GOSUB 34000
218 cx0s=fpiaaddT0s:cx0i$=fpiaaddT0i$:cx0f$=fpiaaddT0f$
220 cx1s=fpiaaddT1s:cx1i$=fpiaaddT1i$:cx1f$=fpiaaddT1f$
222 cy0s=cybase0s:cy0i$=cybase0i$:cy0f$=cybase0f$
224 cy1s=cybase1s:cy1i$=cybase1i$:cy1f$=cybase1f$
226 FOR yloop%=1 TO yendH%
228 cy0s=cy1s:cy0i$=cy1i$:cy0f$=cy1f$
230 fpiaaddA0s=cy0s:fpiaaddA0i$=cy0i$:fpiaaddA0f$=cy0f$
232 fpiaaddA1s=cy1s:fpiaaddA1i$=cy1i$:fpiaaddA1f$=cy1f$
234 fpiaaddB0s=pixh0s:fpiaaddB0i$=pixh0i$:fpiaaddB0f$=pixh0f$
236 fpiaaddB1s=pixh1s:fpiaaddB1i$=pixh1i$:fpiaaddB1f$=pixh1f$
238 GOSUB 34000
240 cy0s=fpiaaddT0s:cy0i$=fpiaaddT0i$:cy0f$=fpiaaddT0f$
242 cy1s=fpiaaddT1s:cy1i$=fpiaaddT1i$:cy1f$=fpiaaddT1f$
244 esc%=0:use%=1
246 REM cp
248 zx0s=0:zx0i$="0":zx0f$="0"
250 zx1s=0:zx1i$="0":zx1f$="0"
252 zy0s=0:zy0i$="0":zy0f$="0"
254 zy1s=0:zy1i$="0":zy1f$="0"
256 LOCATE 1,7
258 IF cx0s<0 THEN PRINT"-";
260 PRINT cx0i$;".";cx0f$;"..";
262 IF cx1s<0 THEN PRINT"-";
264 PRINT cx1i$;".";cx1f$;" / "
266 IF cy0s<0 THEN PRINT"-";
268 PRINT cy0i$;".";cy0f$;"..";
270 IF cy1s<0 THEN PRINT"-";
272 PRINT cy1i$;".";cy1f$;" / "
274 FOR iter%=1 TO maxit%
276 GOSUB 34300:REM over 10-square
278 IF use%<=0 THEN iter%=maxit%+1:GOTO 546
280 GOSUB 34600:REM escaping 10-square
282 IF esc%>0 THEN iter%=maxit%+1:GOTO 546
284 tmp10s=zx0s:tmp10i$=zx0i$:tmp10f$=zx0f$
286 tmp11s=zx1s:tmp11i$=zx1i$:tmp11f$=zx1f$
288 fpiamulA0s=tmp10s:fpiamulA0i$=tmp10i$:fpiamulA0f$=tmp10f$
290 fpiamulA1s=tmp11s:fpiamulA1i$=tmp11i$:fpiamulA1f$=tmp11f$
292 fpiamulB0s=zx0s:fpiamulB0i$=zx0i$:fpiamulB0f$=zx0f$
294 fpiamulB1s=zx1s:fpiamulB1i$=zx1i$:fpiamulB1f$=zx1f$
296 GOSUB 34900
298 tmp20s=fpiamulT0s:tmp20i$=fpiamulT0i$:tmp20f$=fpiamulT0f$
300 tmp21s=fpiamulT1s:tmp21i$=fpiamulT1i$:tmp21f$=fpiamulT1f$
302 tmp10s=zy0s:tmp10i$=zy0i$:tmp10f$=zy0f$
304 tmp11s=zy1s:tmp11i$=zy1i$:tmp11f$=zy1f$
306 fpiamulA0s=tmp10s:fpiamulA0i$=tmp10i$:fpiamulA0f$=tmp10f$
308 fpiamulA1s=tmp11s:fpiamulA1i$=tmp11i$:fpiamulA1f$=tmp11f$
310 fpiamulB0s=zy0s:fpiamulB0i$=zy0i$:fpiamulB0f$=zy0f$
312 fpiamulB1s=zy1s:fpiamulB1i$=zy1i$:fpiamulB1f$=zy1f$
314 GOSUB 34900
316 tmp30s=fpiamulT0s:tmp30i$=fpiamulT0i$:tmp30f$=fpiamulT0f$
318 tmp31s=fpiamulT1s:tmp31i$=fpiamulT1i$:tmp31f$=fpiamulT1f$
320 fpiasubA0s=tmp20s:fpiasubA0i$=tmp20i$:fpiasubA0f$=tmp20f$
322 fpiasubA1s=tmp21s:fpiasubA1i$=tmp21i$:fpiasubA1f$=tmp21f$
324 fpiasubB0s=tmp30s:fpiasubB0i$=tmp30i$:fpiasubB0f$=tmp30f$
326 fpiasubB1s=tmp31s:fpiasubB1i$=tmp31i$:fpiasubB1f$=tmp31f$
328 GOSUB 38200
330 tmp10s=fpiasubT0s:tmp10i$=fpiasubT0i$:tmp10f$=fpiasubT0f$
332 tmp11s=fpiasubT1s:tmp11i$=fpiasubT1i$:tmp11f$=fpiasubT1f$
334 fpiaaddA0s=tmp10s:fpiaaddA0i$=tmp10i$:fpiaaddA0f$=tmp10f$
336 fpiaaddA1s=tmp11s:fpiaaddA1i$=tmp11i$:fpiaaddA1f$=tmp11f$
338 fpiaaddB0s=cx0s:fpiaaddB0i$=cx0i$:fpiaaddB0f$=cx0f$
340 fpiaaddB1s=cx1s:fpiaaddB1i$=cx1i$:fpiaaddB1f$=cx1f$
342 GOSUB 34000
344 zxneu0s=fpiaaddT0s:zxneu0i$=fpiaaddT0i$:zxneu0f$=fpiaaddT0f$
346 zxneu1s=fpiaaddT1s:zxneu1i$=fpiaaddT1i$:zxneu1f$=fpiaaddT1f$
348 fpiamulA0s=zx0s:fpiamulA0i$=zx0i$:fpiamulA0f$=zx0f$
350 fpiamulA1s=zx1s:fpiamulA1i$=zx1i$:fpiamulA1f$=zx1f$
352 fpiamulB0s=zy0s:fpiamulB0i$=zy0i$:fpiamulB0f$=zy0f$
354 fpiamulB1s=zy1s:fpiamulB1i$=zy1i$:fpiamulB1f$=zy1f$
356 GOSUB 34900
358 tmp10s=fpiamulT0s:tmp10i$=fpiamulT0i$:tmp10f$=fpiamulT0f$
360 tmp11s=fpiamulT1s:tmp11i$=fpiamulT1i$:tmp11f$=fpiamulT1f$
362 tmp20s=tmp10s:tmp20i$=tmp10i$:tmp20f$=tmp10f$
364 tmp21s=tmp11s:tmp21i$=tmp11i$:tmp21f$=tmp11f$
366 fpiaaddA0s=tmp20s:fpiaaddA0i$=tmp20i$:fpiaaddA0f$=tmp20f$
368 fpiaaddA1s=tmp21s:fpiaaddA1i$=tmp21i$:fpiaaddA1f$=tmp21f$
370 fpiaaddB0s=tmp10s:fpiaaddB0i$=tmp10i$:fpiaaddB0f$=tmp10f$
372 fpiaaddB1s=tmp11s:fpiaaddB1i$=tmp11i$:fpiaaddB1f$=tmp11f$
374 GOSUB 34000
376 tmp30s=fpiaaddT0s:tmp30i$=fpiaaddT0i$:tmp30f$=fpiaaddT0f$
378 tmp31s=fpiaaddT1s:tmp31i$=fpiaaddT1i$:tmp31f$=fpiaaddT1f$
380 fpiaaddA0s=tmp30s:fpiaaddA0i$=tmp30i$:fpiaaddA0f$=tmp30f$
382 fpiaaddA1s=tmp31s:fpiaaddA1i$=tmp31i$:fpiaaddA1f$=tmp31f$
384 fpiaaddB0s=cy0s:fpiaaddB0i$=cy0i$:fpiaaddB0f$=cy0f$
386 fpiaaddB1s=cy1s:fpiaaddB1i$=cy1i$:fpiaaddB1f$=cy1f$
388 GOSUB 34000
390 zyneu0s=fpiaaddT0s:zyneu0i$=fpiaaddT0i$:zyneu0f$=fpiaaddT0f$
392 zyneu1s=fpiaaddT1s:zyneu1i$=fpiaaddT1i$:zyneu1f$=fpiaaddT1f$
394 zx0s=zxneu0s:zx0i$=zxneu0i$:zx0f$=zxneu0f$
396 zx1s=zxneu1s:zx1i$=zxneu1i$:zx1f$=zxneu1f$
398 zy0s=zyneu0s:zy0i$=zyneu0i$:zy0f$=zyneu0f$
400 zy1s=zyneu1s:zy1i$=zyneu1i$:zy1f$=zyneu1f$
546 NEXT iter%
548 color%=colunclear%
550 IF use%>0 AND esc%>0 THEN color%=colesc%
552 LOCATE 1,9:PRINT xloop%;",";yloop%;" / "
554 PLOT xloop%-1,yloop%-1,color%
556 PLOT xloop%-1,ye%-yloop%,color%:REM symmetry
558 NEXT yloop%:NEXT xloop%
560 FOR wt=1 TO 10000:NEXT:GOTO 560
562 END
30400 REM fpadd
30402 IF fpaddflag>0 THEN PRINT"err-multiple fpadd":END
30404 fpaddflag=1
30406 fppaddingAs=fpaddAs:fppaddingAi$=fpaddAi$:fppaddingAf$=fpaddAf$
30408 GOSUB 31400
30410 fpaddAs=fppaddingTs:fpaddAi$=fppaddingTi$:fpaddAf$=fppaddingTf$
30412 fppaddingAs=fpaddBs:fppaddingAi$=fpaddBi$:fppaddingAf$=fpaddBf$
30414 GOSUB 31400
30416 fpaddBs=fppaddingTs:fpaddBi$=fppaddingTi$:fpaddBf$=fppaddingTf$
30418 IF fpaddAs=0 THEN fpaddTs=fpaddBs:fpaddTi$=fpaddBi$:fpaddTf$=fpaddBf$:fpaddflag=0:RETURN
30420 IF fpaddBs=0 THEN fpaddTs=fpaddAs:fpaddTi$=fpaddAi$:fpaddTf$=fpaddAf$:fpaddflag=0:RETURN
30422 IF fpaddAs>0 AND fpaddBs>0 THEN GOTO 30500
30426 IF fpaddAs>0 AND fpaddBs<0 THEN GOTO 30600
30428 IF fpaddAs<0 AND fpaddBs>0 THEN GOTO 30900
30430 IF fpaddAs<0 AND fpaddBs<0 THEN GOTO 31200
30432 PRINT"err23":END
30500 REM A>0 B>0 => A+B=|A|+|B|
30502 fpaddabsAs=fpaddAs:fpaddabsAi$=fpaddAi$:fpaddabsAf$=fpaddAf$
30504 fpaddabsBs=fpaddBs:fpaddabsBi$=fpaddBi$:fpaddabsBf$=fpaddBf$
30506 GOSUB 31600
30508 fpaddTs=fpaddabsTs:fpaddTi$=fpaddabsTi$:fpaddTf$=fpaddabsTf$
30510 fpaddflag=0:RETURN
30600 REM 4) A>0 B<0 => A+B=|A|-|B|
30602 fpabsvglAs=fpaddAs:fpabsvglAi$=fpaddAi$:fpabsvglAf$=fpaddAf$
30604 fpabsvglBs=fpaddBs:fpabsvglBi$=fpaddBi$:fpabsvglBf$=fpaddBf$
30606 GOSUB 31800
30608 IF fpabsvglT < 0 THEN GOTO 30800
30700 REM 4a: A>0,B<0 => A+B=|A|-|B| and |A| >= |B|: fpsubabsovgl A,B
30702 fpsubabsagrglbAs=fpaddAs:fpsubabsagrglbAi$=fpaddAi$:fpsubabsagrglbAf$=fpaddAf$
30704 fpsubabsagrglbBs=fpaddBs:fpsubabsagrglbBi$=fpaddBi$:fpsubabsagrglbBf$=fpaddBf$
30706 GOSUB 32200
30708 fpaddTs=fpsubabsagrglbTs:fpaddTi$=fpsubabsagrglbTi$:fpaddTf$=fpsubabsagrglbTf$
30710 fpaddflag=0:RETURN
30800 REM 4b: A>0,B<0 => A+B=|A|-|B| and |A| < |B|: -fpsubabsovgl B,A
30802 fpsubabsagrglbAs=fpaddBs:fpsubabsagrglbAi$=fpaddBi$:fpsubabsagrglbAf$=fpaddBf$
30804 fpsubabsagrglbBs=fpaddAs:fpsubabsagrglbBi$=fpaddAi$:fpsubabsagrglbBf$=fpaddAf$
30806 GOSUB 32200
30808 fpaddTs=-fpsubabsagrglbTs:fpaddTi$=fpsubabsagrglbTi$:fpaddTf$=fpsubabsagrglbTf$
30810 fpaddflag=0:RETURN
30900 REM 5) A<0 B>0 => A+B=-|A|+|B|=|B|-|A|
30902 fpaddtmps=fpaddAs:fpaddtmpi$=fpaddAi$:fpaddtmpf$=fpaddAf$
30904 fpaddAs=fpaddBs:fpaddAi$=fpaddBi$:fpaddAf$=fpaddBf$
30906 fpaddBs=fpaddtmps:fpaddBi$=fpaddtmpi$:fpaddBf$=fpaddtmpf$
30908 GOTO 30600
31200 REM 6) A<0 B<0 => A+B=-|A|-|B|=-(|A|+|B|)
31202 fpaddabsAs=1:fpaddabsAi$=fpaddAi$:fpaddabsAf$=fpaddAf$
31204 fpaddabsBs=1:fpaddabsBi$=fpaddBi$:fpaddabsBf$=fpaddBf$
31206 GOSUB 31600
31208 fpaddTs=-fpaddabsTs:fpaddTi$=fpaddabsTi$:fpaddTf$=fpaddabsTf$
31210 fpaddflag=0:RETURN
31400 REM fppadding
31402 IF fppaddingflag > 0 THEN PRINT"error. multiple padding ":END
31404 fppaddingflag=1
31406 fppaddingfl%=LEN(fppaddingAf$)
31408 fppaddingTs=fppaddingAs:fppaddingTi$=fppaddingAi$:fppaddingTf$=fppaddingAf$
31410 FOR fppaddingloop%=(fppaddingfl%+1) TO fpf% STEP 1:fppaddingTf$=fppaddingTf$+"0":NEXT
31412 fppaddingflag=0:RETURN
31600 REM fpaddabs
31602 IF fpaddabsflag>0 THEN PRINT"err19":END
31604 IF LEN(fpaddabsAf$)<>fpf% OR LEN(fpaddabsBf$)<>fpf% THEN PRINT"error. fpaddabs arguments not padded":END
31606 IF LEN(fpaddabsAi$)>=(fpi%-2) OR LEN(fpaddabsBi$)>=(fpi%-2) THEN PRINT"eror. fpaddabs result would overflow":END
31608 fpaddabscarry%=0:fpaddabsTs=0:fpaddabsTf$=""
31610 FOR fpaddabsloop%=fpf% TO 1 STEP -1
31612 fpaddabsdigit%=ASC(MID$(fpaddabsAf$,fpaddabsloop%,1))-48+ASC(MID$(fpaddabsBf$,fpaddabsloop%,1))-48+fpaddabscarry%
31614 IF fpaddabsdigit%>9 THEN fpaddabscarry%=1:fpaddabsdigit%=fpaddabsdigit%-10 ELSE fpaddabscarry%=0
31616 IF fpaddabsdigit%>9 THEN PRINT"error. adding to large carry over":END
31618 fpaddabsTf$=CHR$(48+fpaddabsdigit%)+fpaddabsTf$
31620 IF fpaddabsdigit%>0 THEN fpaddabsTs=1
31622 NEXT
31624 fpaddabsAlen%=LEN(fpaddabsAi$):fpaddabsBlen%=LEN(fpaddabsBi$)
31626 fpaddabsmaxlen%=fpaddabsAlen%
31628 IF fpaddabsBlen%>fpaddabsmaxlen% THEN fpaddabsmaxlen%=fpaddabsBlen%
31630 fpaddabsApadd%=fpaddabsmaxlen-fpaddabsAlen%:fpaddabsBpadd%=fpaddabsmaxlen-fpaddabsBlen%
31632 FOR fpaddabsloop%=(fpaddabsAlen%+1) TO fpaddabsmaxlen% STEP 1
31634 fpaddabsAi$="0"+fpaddabsAi$:NEXT
31636 FOR fpaddabsloop%=(fpaddabsBlen%+1) TO fpaddabsmaxlen% STEP 1
31638 fpaddabsBi$="0"+fpaddabsBi$:NEXT
31640 fpaddabsTi$=""
31642 FOR fpaddabsloop%=fpaddabsmaxlen% TO 1 STEP -1
31644 fpaddabsdigit%=ASC(MID$(fpaddabsAi$,fpaddabsloop%,1))-48+ASC(MID$(fpaddabsBi$,fpaddabsloop%,1))-48+fpaddabscarry%
31646 IF fpaddabsdigit%>9 THEN fpaddabscarry%=1:fpaddabsdigit%=fpaddabsdigit%-10 ELSE fpaddabscarry%=0
31648 IF fpaddabsdigit%>9 THEN PRINT"error. adding to large carry over":END
31650 fpaddabsTi$=CHR$(48+fpaddabsdigit%)+fpaddabsTi$
31652 IF fpaddabsdigit%>0 THEN fpaddabsTs=1
31654 NEXT
31656 IF fpaddabscarry%>1 THEN PRINT"err20":END
31658 IF fpaddabscarry%=1 THEN fpaddabsTs=1:fpaddabsTi$=CHR$(48+fpaddabscarry%)+fpaddabsTi$
31660 fpaddabsflag=1
31662 fpaddabsflag=0:RETURN
31800 REM fpabsvgl
31802 IF fpabsvglflag>0 THEN PRINT"err15":END
31804 fpabsvglflag=1
31806 IF fpabsvglAs=0 AND fpabsvglBs=0 THEN GOTO 32000
31810 IF fpabsvglAs=0 THEN GOTO 31900
31814 IF fpabsvglBs=0 THEN GOTO 32100
31818 IF LEN(fpabsvglAi$)>LEN(fpabsvglBi$) THEN GOTO 32100
31822 IF LEN(fpabsvglAi$)<LEN(fpabsvglBi$) THEN GOTO 31900
31826 FOR fpabsvglloop%=1 TO LEN(fpabsvglAi$)
31828 fpabsvglAdig%=ASC(MID$(fpabsvglAi$,fpabsvglloop%,1))
31830 fpabsvglBdig%=ASC(MID$(fpabsvglBi$,fpabsvglloop%,1))
31832 IF fpabsvglAdig%>fpabsvglBdig% THEN GOTO 32100
31836 IF fpabsvglAdig%<fpabsvglBdig% THEN GOTO 31900
31840 NEXT
31842 FOR fpabsvglloop%=1 TO LEN(fpabsvglAf$)
31844 fpabsvglAdig%=ASC(MID$(fpabsvglAf$,fpabsvglloop%,1))
31846 fpabsvglBdig%=ASC(MID$(fpabsvglBf$,fpabsvglloop%,1))
31848 IF fpabsvglAdig%>fpabsvglBdig% THEN GOTO 32100
31852 IF fpabsvglAdig%<fpabsvglBdig% THEN GOTO 31900
31856 NEXT
31858 fpabsvglT=0:fpabsvglflag=0:RETURN
31900 fpabsvglT=-1:fpabsvglflag=0:RETURN
32000 fpabsvglT=0:fpabsvglflag=0:RETURN
32100 fpabsvglT=1:fpabsvglflag=0:RETURN
32200 REM fpsubabsagrglb
32202 IF fpsubabsagrglbflag>0 THEN PRINT"err16":END
32204 fpsubabsagrglbflag=1
32206 IF LEN(fpsubabsagrglbAf$)<>fpf% OR LEN(fpsubabsagrglbBf$)<>fpf% THEN PRINT"error. fpsubabs arguments not padded":END
32208 fpsubabsagrglbcarry%=0:fpsubabsagrglbTs=0:fpsubabsagrglbTf$=""
32210 FOR fpsubabsagrglbloop%=fpf% TO 1 STEP -1
32212 fpsubabsagrglbdigitA%=ASC(MID$(fpsubabsagrglbAf$,fpsubabsagrglbloop%,1))-48
32214 fpsubabsagrglbdigitB%=ASC(MID$(fpsubabsagrglbBf$,fpsubabsagrglbloop%,1))-48+fpsubabsagrglbcarry%
32216 fpsubabsagrglbcarry%=0
32218 IF fpsubabsagrglbdigitA%<fpsubabsagrglbdigitB% THEN fpsubabsagrglbdigitA%=fpsubabsagrglbdigitA%+10:fpsubabsagrglbcarry%=1
32220 fpsubabsagrglbresult%=fpsubabsagrglbdigitA%-fpsubabsagrglbdigitB%
32222 IF fpsubabsagrglbresult%>9 THEN PRINT"err17":END
32224 fpsubabsagrglbTf$=CHR$(48+fpsubabsagrglbresult%)+fpsubabsagrglbTf$
32226 IF fpsubabsagrglbresult%>0 THEN fpsubabsagrglbTs=1
32228 NEXT
32230 fpsubabsagrglbAlen%=LEN(fpsubabsagrglbAi$):fpsubabsagrglbBlen%=LEN(fpsubabsagrglbBi$)
32232 fpsubabsagrglbmaxlen%=fpsubabsagrglbAlen%
32234 IF fpsubabsagrglbBlen%>fpsubabsagrglbmaxlen% THEN fpsubabsagrglbmaxlen%=fpsubabsagrglbBlen%
32236 fpsubabsagrglbApadd%=fpsubabsagrglbmaxlen-fpsubabsagrglbAlen%:fpsubabsagrglbBpadd%=fpsubabsagrglbmaxlen-fpsubabsagrglbBlen%
32238 FOR fpsubabsagrglbloop%=(fpsubabsagrglbAlen%+1) TO fpsubabsagrglbmaxlen% STEP 1
32240 fpsubabsagrglbAi$="0"+fpsubabsagrglbAi$:NEXT
32242 FOR fpsubabsagrglbloop%=(fpsubabsagrglbBlen%+1) TO fpsubabsagrglbmaxlen% STEP 1
32244 fpsubabsagrglbBi$="0"+fpsubabsagrglbBi$:NEXT
32246 fpsubabsagrglbTi$=""
32248 FOR fpsubabsagrglbloop%=fpsubabsagrglbmaxlen% TO 1 STEP -1
32250 fpsubabsagrglbdigitA%=ASC(MID$(fpsubabsagrglbAi$,fpsubabsagrglbloop%,1))-48
32252 fpsubabsagrglbdigitB%=ASC(MID$(fpsubabsagrglbBi$,fpsubabsagrglbloop%,1))-48+fpsubabsagrglbcarry%
32254 fpsubabsagrglbcarry%=0
32256 IF fpsubabsagrglbdigitA%<fpsubabsagrglbdigitB% THEN fpsubabsagrglbdigitA%=fpsubabsagrglbdigitA%+10:fpsubabsagrglbcarry%=1
32258 fpsubabsagrglbresult%=fpsubabsagrglbdigitA%-fpsubabsagrglbdigitB%
32260 IF fpsubabsagrglbresult%>9 THEN PRINT"error. subtracting to large carry over":END
32262 fpsubabsagrglbTi$=CHR$(48+fpsubabsagrglbresult%)+fpsubabsagrglbTi$
32264 IF fpsubabsagrglbresult%>0 THEN fpsubabsagrglbTs=1
32266 NEXT
32268 IF fpsubabsagrglbscarry%<>0 THEN PRINT"err18":END
32270 fpsubabsagrglbnz%=-1
32272 FOR fpsubabsagrglbloop%=1 TO LEN(fpsubabsagrglbTi$)
32274 IF fpsubabsagrglbnz%<0 THEN IF ASC(MID$(fpsubabsagrglbTi$,fpsubabsagrglbloop%,1))<>48 THEN fpsubabsagrglbnz%=fpsubabsagrglbloop%
32276 NEXT
32278 IF fpsubabsagrglbnz%<0 THEN fpsubabsagrglbnz%=LEN(fpsubabsagrglbTi$)
32280 fpsubabsagrglbTi$=MID$(fpsubabsagrglbTi$,fpsubabsagrglbnz%,LEN(fpsubabsagrglbTi$)-fpsubabsagrglbnz%+1)
32282 fpsubabsagrglbflag=0:RETURN
32400 REM fpsub: A-B=A+(-B)
32402 IF fpsubflag>0 THEN PRINT"err21":END
32404 fpsubflag=1
32406 fpaddAs=fpsubAs:fpaddAi$=fpsubAi$:fpaddAf$=fpsubAf$
32408 fpaddBs=-fpsubBs:fpaddBi$=fpsubBi$:fpaddBf$=fpsubBf$
32410 GOSUB 30400
32412 fpsubTs=fpaddTs:fpsubTi$=fpaddTi$:fpsubTf$=fpaddTf$
32414 fpsubflag=0:RETURN
32600 REM bigintposadd - exact, adds two non-negative bigint numbers
32602 IF bigintposaddflag > 0 THEN PRINT "error. multiple calls bigintposadd":END
32604 bigintposaddflag=1
32606 bigintposaddmaxlen%=LEN(bigintposaddA$)
32608 IF LEN(bigintposaddB$)>bigintposaddmaxlen% THEN bigintposaddmaxlen%=LEN(bigintposaddB$)
32610 IF (bigintposaddmaxlen%+1)>=bip% THEN PRINT"err10":END
32612 bigintposaddTs=bigintposaddBs
32614 IF bigintposaddAs=0 THEN bigintposaddT$=bigintposaddB$:bigintposaddflag=0:RETURN
32616 bigintposaddTs=bigintposaddAs
32618 IF bigintposaddBs=0 THEN bigintposaddT$=bigintposaddA$:bigintposaddflag=0:RETURN
32620 bigintposaddAlen%=LEN(bigintposaddA$):bigintposaddBlen%=LEN(bigintposaddB$)
32622 bigintposaddApadd%=bigintposaddmaxlen-bigintposaddAlen%:bigintposaddBpadd%=bigintposaddmaxlen-bigintposaddBlen%
32624 FOR bigintposaddloop%=(bigintposaddAlen%+1) TO bigintposaddmaxlen% STEP 1
32626 bigintposaddA$="0"+bigintposaddA$:NEXT
32628 FOR bigintposaddloop%=(bigintposaddBlen%+1) TO bigintposaddmaxlen% STEP 1
32630 bigintposaddB$="0"+bigintposaddB$:NEXT
32632 bigintposaddT$="":bigintposaddTs=0
32634 bigintposaddcarry%=0
32636 FOR bigintposaddloop%=bigintposaddmaxlen% TO 1 STEP -1
32638 bigintposadddigit%=ASC(MID$(bigintposaddA$,bigintposaddloop%,1))-48+ASC(MID$(bigintposaddB$,bigintposaddloop%,1))-48+bigintposaddcarry%
32640 IF bigintposadddigit%>9 THEN bigintposaddcarry%=1:bigintposadddigit%=bigintposadddigit%-10 ELSE bigintposaddcarry%=0
32642 IF bigintposadddigit%>9 THEN PRINT"err11":END
32644 bigintposaddT$=CHR$(48+bigintposadddigit%)+bigintposaddT$
32646 IF bigintposadddigit%>0 THEN bigintposaddTs=1
32648 NEXT
32650 IF bigintposaddcarry%>1 THEN PRINT"err12":END
32652 IF bigintposaddcarry%=1 THEN bigintposaddTs=1:bigintposaddT$=CHR$(48+bigintposaddcarry%)+bigintposaddT$
32654 bigintposaddflag=0:RETURN
32800 REM bigintmul,exact
32802 IF bigintmulflag>0 THEN PRINT"err7":END
32804 bigintmulflag=1
32806 IF (LEN(bigintmulA$)+LEN(bigintmulB$))>=bip% THEN PRINT"err9":END
32808 bigintmulTs=0:bigintmulT$="0"
32810 IF bigintmulAs=0 OR bigintmulBs=0 THEN bigintmulflag=0:RETURN
32812 bigOA$(1)=bigintmulA$
32814 bigintposaddAs=1:bigintposaddA$=bigintmulA$
32816 FOR bigintmulloop%=2 TO 9
32818 bigintposaddBs=1:bigintposaddB$=bigOA$(bigintmulloop%-1)
32820 GOSUB 32600
32824 bigOA$(bigintmulloop%)=bigintposaddT$
32826 NEXT
32828 bigintmulBlen%=LEN(bigintmulB$)
32830 bigintmulshift%=bigintmulBlen%
32832 bigintmulTs=0:bigintmulT$=""
32834 FOR bigintmulloop%=1 TO bigintmulBlen%
32836 bigintmulshift%=bigintmulshift%-1
32838 bigintmuldigitB%=ASC(MID$(bigintmulB$,bigintmulloop%,1))-48
32840 IF bigintmuldigitB% = 0 THEN GOTO 32900
32900 bigintposaddA$="":bigintposaddAs=1
32902 FOR bigintmulloop2%=1 TO bigintmulshift%
32904 bigintposaddA$=bigintposaddA$+"0"
32906 NEXT
32908 bigintposaddA$=bigOA$(bigintmuldigitB%)+bigintposaddA$
32910 bigintposaddBs=bigintmulTs:bigintposaddB$=bigintmulT$
32912 GOSUB 32600
32916 bigintmulTs=bigintposaddTs:bigintmulT$=bigintposaddT$
32918 NEXT
32920 IF bigintmulAs=bigintmulBs THEN bigintmulTs=1 ELSE bigintmulTs=-1
32922 bigintmulflag=0:RETURN
33000 REM fpmul,rounded
33002 IF fpmulflag>0 THEN PRINT"err6":END
33004 fpmulflag=1
33006 fpmulTs=0:fpmulTi$="0":fpmulTf$="0"
33008 IF fpmulAs=0 OR fpmulBs=0 THEN fpmulflag=0:RETURN
33010 IF LEN(fpmulAf$)=fpf% THEN GOTO 33100
33012 fppaddingAs=fpmulAs:fppaddingAi$=fpmulAi$:fppaddingAf$=fpmulAf$
33016 GOSUB 31400
33018 fpmulAs=fppaddingTs:fpmulAi$=fppaddingTi$:fpmulAf$=fppaddingTf$
33100 IF LEN(fpmulBf$)=fpf% THEN GOTO 33200
33102 fppaddingAs=fpmulBs:fppaddingAi$=fpmulBi$:fppaddingAf$=fpmulBf$
33106 GOSUB 31400
33108 fpmulBs=fppaddingTs:fpmulBi$=fppaddingTi$:fpmulBf$=fppaddingTf$
33200 bigintmulAs=fpmulAs:bigintmulA$=fpmulAi$+fpmulAf$
33202 bigintmulBs=fpmulBs:bigintmulB$=fpmulBi$+fpmulBf$
33204 GOSUB 32800
33208 fpmultmp%=LEN(bigintmulT$)
33210 FOR fpmulloop%=fpmultmp% TO (2*fpf%)
33212 bigintmulT$="0"+bigintmulT$
33214 NEXT
33216 IF bigintmulTs=0 THEN fpmulTs=0:fpmulTi$="0":fpmulTf$="0":fpmulflag=0:RETURN
33218 bigintmulexacts=bigintmulTs
33220 fpmultruncs=bigintmulTs
33222 fpmultruncf$=RIGHT$(bigintmulT$,2*fpf%)
33224 fpmultruncf$=LEFT$(fpmultruncf$,fpf%)
33226 fpmultrunci$=LEFT$(bigintmulT$,LEN(bigintmulT$)-(2*fpf%))
33228 fpmultmp%=-1:fpmultrunclen%=LEN(fpmultrunci$)
33230 FOR fpmulloop%=1 TO fpmultrunclen%
33232 IF fpmultmp%<=0 THEN IF ASC(MID$(fpmultrunci$,fpmulloop%,1))<>48 THEN fpmultmp%=fpmulloop%
33234 NEXT
33236 IF fpmultmp%<=0 THEN fpmultmp%=fpmultrunclen%
33238 fpmultrunci$=MID$(fpmultrunci$,fpmultmp%,fpmultrunclen%-fpmultmp%+1)
33240 REM chck exact zero
33242 fpmulnotzero%=0
33244 FOR fpmulloop%=1 TO LEN(fpmultrunci$)
33246 IF fpmulnotzero%<=0 THEN IF ASC(MID$(fpmultrunci$,fpmulloop%,1))<>48 THEN fpmulnotzero%=1
33248 NEXT
33250 FOR fpmulloop%=1 TO LEN(fpmultruncf$)
33252 IF fpmulnotzero%<=0 THEN IF ASC(MID$(fpmultruncf$,fpmulloop%,1))<>48 THEN fpmulnotzero%=1
33254 NEXT
33256 IF fpmulnotzero%<=0 THEN fpmultruncs=0:fpmultrunci$="0":fpmultruncf$="0"
33258 REM round by result sign and round mode
33260 IF bigintmulexacts<0 AND fpmulrdmode<0 THEN GOTO 33400
33264 IF bigintmulexacts<0 AND fpmulrdmode>0 THEN GOTO 33500
33266 IF bigintmulexacts>0 AND fpmulrdmode<0 THEN GOTO 33600
33268 IF bigintmulexacts>0 AND fpmulrdmode>0 THEN GOTO 33700
33272 PRINT"err6":END
33400 REM exacts<0,round down
33402 fpsubAs=fpmultruncs:fpsubAi$=fpmultrunci$:fpsubAf$=fpmultruncf$
33404 fpsubBs=epss:fpsubBi$=epsi$:fpsubBf$=epsf$
33406 GOSUB 32400
33408 fpmulTs=fpsubTs:fpmulTi$=fpsubTi$:fpmulTf$=fpsubTf$
33410 fpmulflag=0:RETURN
33412 fpmulflag=0:RETURN
33500 REM exacts<0,round up
33502 fpmulTs=fpmultruncs:fpmulTi$=fpmultrunci$:fpmulTf$=fpmultruncf$
33504 fpmulflag=0:RETURN
33600 REM exacts>0,round dowh
33602 fpmulTs=fpmultruncs:fpmulTi$=fpmultrunci$:fpmulTf$=fpmultruncf$
33604 fpmulflag=0:RETURN
33700 REM exacts>0,round up
33702 fpaddAs=fpmultruncs:fpaddAi$=fpmultrunci$:fpaddAf$=fpmultruncf$
33704 fpaddBs=epss:fpaddBi$=epsi$:fpaddBf$=epsf$
33706 GOSUB 30400
33708 fpmulTs=fpaddTs:fpmulTi$=fpaddTi$:fpmulTf$=fpaddTf$
33710 fpmulflag=0:RETURN
34000 REM fpiaadd
34002 IF fpiaaddflag>0 THEN PRINT"err4":END
34004 fpiaaddflag=1
34006 fppaddingAs=fpiaaddA0s:fppaddingAi$=fpiaaddA0i$:fppaddingAf$=fpiaaddA0f$
34008 GOSUB 31400
34010 fpiaaddA0s=fppaddingTs:fpiaaddA0i$=fppaddingTi$:fpiaaddA0f$=fppaddingTf$
34012 fppaddingAs=fpiaaddA1s:fppaddingAi$=fpiaaddA1i$:fppaddingAf$=fpiaaddA1f$
34014 GOSUB 31400
34016 fpiaaddA1s=fppaddingTs:fpiaaddA1i$=fppaddingTi$:fpiaaddA1f$=fppaddingTf$
34018 fppaddingAs=fpiaaddB0s:fppaddingAi$=fpiaaddB0i$:fppaddingAf$=fpiaaddB0f$
34020 GOSUB 31400
34022 fpiaaddB0s=fppaddingTs:fpiaaddB0i$=fppaddingTi$:fpiaaddB0f$=fppaddingTf$
34024 fppaddingAs=fpiaaddB1s:fppaddingAi$=fpiaaddB1i$:fppaddingAf$=fpiaaddB1f$
34026 GOSUB 31400
34028 fpiaaddB1s=fppaddingTs:fpiaaddB1i$=fppaddingTi$:fpiaaddB1f$=fppaddingTf$
34030 fpaddAs=fpiaaddA0s:fpaddAi$=fpiaaddA0i$:fpaddAf$=fpiaaddA0f$
34032 fpaddBs=fpiaaddB0s:fpaddBi$=fpiaaddB0i$:fpaddBf$=fpiaaddB0f$
34034 GOSUB 30400
34036 fpiaaddT0s=fpaddTs:fpiaaddT0i$=fpaddTi$:fpiaaddT0f$=fpaddTf$
34038 fpaddAs=fpiaaddA1s:fpaddAi$=fpiaaddA1i$:fpaddAf$=fpiaaddA1f$
34040 fpaddBs=fpiaaddB1s:fpaddBi$=fpiaaddB1i$:fpaddBf$=fpiaaddB1f$
34042 GOSUB 30400
34044 fpiaaddT1s=fpaddTs:fpiaaddT1i$=fpaddTi$:fpiaaddT1f$=fpaddTf$
34046 fpiaaddflag=0:RETURN
34300 REM chk orb encompasses 10-square
34302 use%=1
34304 IF NOT ((zx0s<0) AND (zx1s>0)) THEN RETURN
34306 IF NOT ((zy0s<0) AND (zy1s>0)) THEN RETURN
34308 IF (LEN(zx0i$)<=1) OR (LEN(zx1i$)<=1) THEN RETURN
34310 IF (LEN(zy0i$)<=1) OR (LEN(zy1i$)<=1) THEN RETURN
34312 use%=0:RETURN
34600 REM orbit escapes fully 10-square
34602 esc%=1
34604 IF (zx0s>0) AND (LEN(zx0i$)>=2) THEN RETURN
34606 IF (zx1s<0) AND (LEN(zx1i$)>=2) THEN RETURN
34608 IF (zy0s>0) AND (LEN(zy0i$)>=2) THEN RETURN
34610 IF (zy1s<0) AND (LEN(zy1i$)>=2) THEN RETURN
34612 esc%=0:RETURN
34900 REM fpiamul
34902 IF fpiamulflag>0 THEN PRINT"err3":END
34904 fpiamulflag=1
34906 IF fpiamulA0s>0 AND fpiamulB0s>0 THEN GOTO 35800
34908 IF fpiamulA1s<0 AND fpiamulB0s>0 THEN GOTO 36400
34910 IF fpiamulA0s>0 AND fpiamulB1s<0 THEN GOTO 36100
34912 IF fpiamulA1s<0 AND fpiamulB1s<0 THEN GOTO 36700
34914 IF fpiamulA0s<0 AND fpiamulA1s>0 AND fpiamulB1s<0 THEN GOTO 37000
34916 IF fpiamulA0s<0 AND fpiamulA1s>0 AND fpiamulB0s>0 THEN GOTO 37300
34918 IF fpiamulB0s<0 AND fpiamulB1s>0 AND fpiamulA0s>0 THEN GOTO 37900
34920 IF fpiamulB0s<0 AND fpiamulB1s>0 AND fpiamulA1s<0 THEN GOTO 37600
34922 REM general IA mult
34924 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
34926 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
34928 fpmulrdmode=-1:GOSUB 33000
34930 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
34932 fpaddAs=fpiamulT0s:fpaddAi$=fpiamulT0i$:fpaddAf$=fpiamulT0f$
34934 fpaddBs=epss:fpaddBi$=epsi$:fpaddBf$=epsf$
34936 GOSUB 30400
34938 fpiamulT1s=fpaddTs:fpiamulT1i$=fpaddTi$:fpiamulT1f$=fpaddTf$
34940 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
34942 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
34944 fpmulrdmode=-1:GOSUB 33000
34946 fpiamultmps=fpmulTs:fpiamultmpi$=fpmulTi$:fpiamultmpf$=fpmulTf$
34948 fpvglAs=fpiamultmps:fpvglAi$=fpiamultmpi$:fpvglAf$=fpiamultmpf$
34950 fpvglBs=fpiamulT0s:fpvglBi$=fpiamulT0i$:fpvglBf$=fpiamulT0f$
34952 GOSUB 35200
34954 IF fpvglT<0 THEN fpiamulT0s=fpiamultmps:fpiamulT0i$=fpiamultmpi$:fpiamulT0f$=fpiamultmpf$
34956 fpaddAs=fpiamulTs:fpaddAi$=fpiamulTi$:fpaddAf$=fpiamulTf$
34958 fpaddBs=epss:fpaddBi$=epsi$:fpaddBf$=epsf$
34960 GOSUB 30400
34962 fpiamultmp2s=fpaddTs:fpiamultmp2i$=fpaddTi$:fpiamultmp2f$=fpaddTf$
34964 fpvglAs=fpiamultmp2s:fpvglAi$=fpiamultmp2i$:fpvglAf$=fpiamultmp2f$
34966 fpvglBs=fpiamulT1s:fpvglBi$=fpiamulT1i$:fpvglBf$=fpiamulT1f$
34968 GOSUB 35200
34970 IF fpvglT>0 THEN fpiamulT1s=fpiamultmp2s:fpiamulT1i$=fpiamultmp2i$:fpiamulT1f$=fpiamultmp2f$
34972 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
34974 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
34976 fpmulrdmode=-1:GOSUB 33000
34978 fpiamultmps=fpmulTs:fpiamultmpi$=fpmulTi$:fpiamultmpf$=fpmulTf$
34980 fpvglAs=fpiamultmps:fpvglAi$=fpiamultmpi$:fpvglAf$=fpiamultmpf$
34982 fpvglBs=fpiamulT0s:fpvglBi$=fpiamulT0i$:fpvglBf$=fpiamulT0f$
34984 GOSUB 35200
34986 IF fpvglT<0 THEN fpiamulT0s=fpiamultmps:fpiamulT0i$=fpiamultmpi$:fpiamulT0f$=fpiamultmpf$
34988 fpaddAs=fpiamulTs:fpaddAi$=fpiamulTi$:fpaddAf$=fpiamulTf$
34990 fpaddBs=epss:fpaddBi$=epsi$:fpaddBf$=epsf$
34992 GOSUB 30400
34994 fpiamultmp2s=fpaddTs:fpiamultmp2i$=fpaddTi$:fpiamultmp2f$=fpaddTf$
34996 fpvglAs=fpiamultmp2s:fpvglAi$=fpiamultmp2i$:fpvglAf$=fpiamultmp2f$
34998 fpvglBs=fpiamulT1s:fpvglBi$=fpiamulT1i$:fpvglBf$=fpiamulT1f$
35000 GOSUB 35200
35002 IF fpvglT>0 THEN fpiamulT1s=fpiamultmp2s:fpiamulT1i$=fpiamultmp2i$:fpiamulT1f$=fpiamultmp2f$
35004 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
35006 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
35008 fpmulrdmode=-1:GOSUB 33000
35010 fpiamultmps=fpmulTs:fpiamultmpi$=fpmulTi$:fpiamultmpf$=fpmulTf$
35012 fpvglAs=fpiamultmps:fpvglAi$=fpiamultmpi$:fpvglAf$=fpiamultmpf$
35014 fpvglBs=fpiamulT0s:fpvglBi$=fpiamulT0i$:fpvglBf$=fpiamulT0f$
35016 GOSUB 35200
35018 IF fpvglT<0 THEN fpiamulT0s=fpiamultmps:fpiamulT0i$=fpiamultmpi$:fpiamulT0f$=fpiamultmpf$
35020 fpaddAs=fpiamulTs:fpaddAi$=fpiamulTi$:fpaddAf$=fpiamulTf$
35022 fpaddBs=epss:fpaddBi$=epsi$:fpaddBf$=epsf$
35024 GOSUB 30400
35026 fpiamultmp2s=fpaddTs:fpiamultmp2i$=fpaddTi$:fpiamultmp2f$=fpaddTf$
35028 fpvglAs=fpiamultmp2s:fpvglAi$=fpiamultmp2i$:fpvglAf$=fpiamultmp2f$
35030 fpvglBs=fpiamulT1s:fpvglBi$=fpiamulT1i$:fpvglBf$=fpiamulT1f$
35032 GOSUB 35200
35034 IF fpvglT>0 THEN fpiamulT1s=fpiamultmp2s:fpiamulT1i$=fpiamultmp2i$:fpiamulT1f$=fpiamultmp2f$
35036 fpiamulflag=0:RETURN
35200 REM fpvgl
35202 IF fpvglflag>0 THEN PRINT"err2":END
35204 fpvglflag=1
35206 IF fpvglAs=0 THEN fpvglT=-fpvglBs:fpvglflag=0:RETURN
35208 IF fpvglBs=0 THEN fpvglT=fpvglAs:fpvglflag=0:RETURN
35210 IF fpvglAs<0 AND fpvglBs>0 THEN fpvglT=-1:fpvglflag=0:RETURN
35212 IF fpvglAs>0 AND fpvglBs<0 THEN fpvglT=1:fpvglflag=0:RETURN
35214 fpabsvglAs=fpvglAs:fpabsvglAi$=fpvglAi$:fpabsvglAf$=fpvglAf$
35216 fpabsvglBs=fpvglBs:fpabsvglBi$=fpvglBi$:fpabsvglBf$=fpvglBf$
35218 GOSUB 31800
35220 IF fpvglAs<0 AND fpvglBs<0 THEN fpvglT=-fpabsvglT:fpvglflag=0:RETURN
35222 IF fpvglAs>0 AND fpvglBs>0 THEN fpvglT=fpabsvglT:fpvglflag=0:RETURN
35224 PRINT"err.fpvgl/2":END
35800 REM Apos,Bpos
35802 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
35804 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
35806 fpmulrdmode=-1:GOSUB 33000
35808 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
35810 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
35812 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
35814 fpmulrdmode=1:GOSUB 33000
35816 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
35818 fpiamulflag=0:RETURN
36100 REM Apos,Bneg
36102 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
36104 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
36106 fpmulrdmode=-1:GOSUB 33000
36108 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
36110 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
36112 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
36114 fpmulrdmode=1:GOSUB 33000
36116 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
36118 fpiamulflag=0:RETURN
36400 REM Aneg,Bpos
36402 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
36404 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
36406 fpmulrdmode=-1:GOSUB 33000
36408 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
36410 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
36412 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
36414 fpmulrdmode=1:GOSUB 33000
36416 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
36418 fpiamulflag=0:RETURN
36700 REM Aneg,Bneg
36702 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
36704 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
36706 fpmulrdmode=1:GOSUB 33000
36708 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
36710 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
36712 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
36714 fpmulrdmode=-1:GOSUB 33000
36716 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
36718 fpiamulflag=0:RETURN
37000 REM Astradd,Bneg
37002 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
37004 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
37006 fpmulrdmode=-1:GOSUB 33000
37008 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
37010 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
37012 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
37014 fpmulrdmode=1:GOSUB 33000
37016 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
37018 fpiamulflag=0:RETURN
37300 REM Astradd,Bpos
37302 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
37304 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
37306 fpmulrdmode=-1:GOSUB 33000
37308 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
37310 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
37312 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
37314 fpmulrdmode=1:GOSUB 33000
37316 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
37318 fpiamulflag=0:RETURN
37600 REM Aneg,Bstradd
37602 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
37604 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
37606 fpmulrdmode=-1:GOSUB 33000
37608 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
37610 fpmulAs=fpiamulA0s:fpmulAi$=fpiamulA0i$:fpmulAf$=fpiamulA0f$
37612 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
37614 fpmulrdmode=1:GOSUB 33000
37616 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
37618 fpiamulflag=0:RETURN
37900 REM Apos,Bstradd
37902 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
37904 fpmulBs=fpiamulB0s:fpmulBi$=fpiamulB0i$:fpmulBf$=fpiamulB0f$
37906 fpmulrdmode=-1:GOSUB 33000
37908 fpiamulT0s=fpmulTs:fpiamulT0i$=fpmulTi$:fpiamulT0f$=fpmulTf$
37910 fpmulAs=fpiamulA1s:fpmulAi$=fpiamulA1i$:fpmulAf$=fpiamulA1f$
37912 fpmulBs=fpiamulB1s:fpmulBi$=fpiamulB1i$:fpmulBf$=fpiamulB1f$
37914 fpmulrdmode=1:GOSUB 33000
37916 fpiamulT1s=fpmulTs:fpiamulT1i$=fpmulTi$:fpiamulT1f$=fpmulTf$
37918 fpiamulflag=0:RETURN
38200 REM fpiasub
38202 IF fpiasubflag>0 THEN PRINT"err5":END
38204 fpiasubflag=1
38206 fppaddingAs=fpiasubA0s:fppaddingAi$=fpiasubA0i$:fppaddingAf$=fpiasubA0f$
38208 GOSUB 31400
38210 fpiasubA0s=fppaddingTs:fpiasubA0i$=fppaddingTi$:fpiasubA0f$=fppaddingTf$
38212 fppaddingAs=fpiasubA1s:fppaddingAi$=fpiasubA1i$:fppaddingAf$=fpiasubA1f$
38214 GOSUB 31400
38216 fpiasubA1s=fppaddingTs:fpiasubA1i$=fppaddingTi$:fpiasubA1f$=fppaddingTf$
38218 fppaddingAs=fpiasubB0s:fppaddingAi$=fpiasubB0i$:fppaddingAf$=fpiasubB0f$
38220 GOSUB 31400
38222 fpiasubB0s=fppaddingTs:fpiasubB0i$=fppaddingTi$:fpiasubB0f$=fppaddingTf$
38224 fppaddingAs=fpiasubB1s:fppaddingAi$=fpiasubB1i$:fppaddingAf$=fpiasubB1f$
38226 GOSUB 31400
38228 fpiasubB1s=fppaddingTs:fpiasubB1i$=fppaddingTi$:fpiasubB1f$=fppaddingTf$
38230 fpsubAs=fpiasubA0s:fpsubAi$=fpiasubA0i$:fpsubAf$=fpiasubA0f$
38232 fpsubBs=fpiasubB1s:fpsubBi$=fpiasubB1i$:fpsubBf$=fpiasubB1f$
38234 GOSUB 32400
38236 fpiasubT0s=fpsubTs:fpiasubT0i$=fpsubTi$:fpiasubT0f$=fpsubTf$
38238 fpsubAs=fpiasubA1s:fpsubAi$=fpiasubA1i$:fpsubAf$=fpiasubA1f$
38240 fpsubBs=fpiasubB0s:fpsubBi$=fpiasubB0i$:fpsubBf$=fpiasubB0f$
38242 GOSUB 32400
38244 fpiasubT1s=fpsubTs:fpiasubT1i$=fpsubTi$:fpiasubT1f$=fpsubTf$
38246 fpiasubflag=0:RETURN
