# Fore1: Hit the core (50 points)

Running strings I found:
cvqAeqacLtqazEigwiXobxrCrtuiTzahfFreqc{bnjrKwgk83kgd43j85ePgb_e_rwqr7fvbmHjklo3tews_hmkogooyf0vbnk0ii87Drfgh_n kiwutfb0ghk9ro987k5tfb_hjiouo087ptfcv}

Looks like every 5th char is part of the flag. 
The beginning of the string didn't fit the correct format, so I have to pre-pend some junk.

In python.

```
>>> flag = "AA" + "cvqAeqacLtqazEigwiXobxrCrtuiTzahfFreqc{bnjrKwgk83kgd43j85ePgb_e_rwqr7fvbmHjklo3tews_hmkogooyf0vbnk0ii87Drfgh_n kiwutfb0ghk9ro987k5tfb_hjiouo087ptfcv}"
>>> flag[0::5]
'AALEXCTF{K33P_7H3_g00D_w0rk_up}'
```
