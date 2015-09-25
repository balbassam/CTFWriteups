200 airport
----------

Unzipping this folder revealed a "for_release" and a "__MACOSX" folder.

The __MACOSX folder was empty. In case you are wondering here is some info about why it exists http://old.floatingsun.net/2007/02/07/whats-with-__macosx-in-zip-files/index.html

The for_release folder had the following contents:
```
1.png  2.png  3.png  4.png  steghide.jpg
```

Seeing the steghide.jpg *STRONGLY* suggested that this was basic steganography using steghide. Steghide encrypts and hides a file within another file. However, we needed a key. 

The png files 1-4 looked like some international airports. A few of us searched google maps for these airports based on the street names which were visible in these images. The airports were:

File | Airport
-----|------
1.png|José Martí International Airport 
2.png|Hong Kong International Airport
3.png|Los Angeles International Airport
4.png|Toronto Pearson International Airport

The airport codes were HAV, HKG, LAX and YYZ. We concatinated the codes together to make the string "HAVHKGLAXYYZ" and used steghide to extract the information using the following command.

```sh
steghide extract -sf steghide.jpg -p HAVHKGLAXYYZ 
wrote extracted data to "key.txt".
````

The contents of key.txt was "iH4t3A1rp0rt5"
