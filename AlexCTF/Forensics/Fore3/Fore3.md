# Fore3: USB probing (150 points)

#Hint 
One of our agents managed to sniff important piece of data transferred transmitted via USB, he told us that this pcap file contains all what we need to recover the data can you find it ?


Looking at wireshark it looked like it was a usb hard drive. I had to extract the data with the following commands.

```
$ tshark -r fore2.pcap -T fields -e usb.capdata -Y usb.capdata > contents.txt
$ sed -i 's/://g'  contents.txt
$ xxd -r -p contents.txt  > stuff.bin

$ binwalk stuff.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
53248         0xD000          PNG image, 460 x 130, 8-bit/color RGBA, interlaced
```


I extracted the png and the key was in the image. Somehow it wasn't rendering properly so I had to use `feh` to open it.

`ALEXCTF{SN1FF_TH3_FL4G_0V3R_US8}`
