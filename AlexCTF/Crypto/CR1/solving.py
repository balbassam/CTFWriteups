#!/usr/bin/env python3

'''
CR1: Ultracoded
Points: 50

Fady didn't understand well the difference between encryption and encoding, so instead of encrypting some secret message to pass to his friend, he encoded it!
Hint: Fady's encoding doens't handly any special character
'''

import binascii
import base64

fname = 'zero_one'
with open(fname) as f:
    # The file only has one line
    content = f.readline()

# Converting to regular binary string
content = content.replace('ZERO', '0')
content = content.replace('ONE', '1')
content = "".join(content.split())

# splitting 8 bits at a time
content_split = [content[i:i+8] for i in range(0, len(content), 8)]
content_ints = [int(i,2) for i in content_split]
content_ascii = ''.join([chr(i) for i in content_ints])
# print(content)
# print(content_split)
# print(content_ints)

# Just confirmed that this was printable ascii
# print("Min value is: " + str(min(content_ints)))
# print("Max value is: " + str(max(content_ints)))

# Debugging
# for i in content_ints:
#     char = content_ints[i]
#     print("{} is {} = {}".format(i, char, chr(char)))

print("\nThe content converted to ascii")
print(content_ascii)
# When I printed that, it was obvious to me that I was dealing with base64 
# Base64 uses '=' as padding

print("\nBase64 decoding")
b64decoded = base64.b64decode(content_ascii).decode("utf-8")
print(b64decoded)

''' I ended up getting morse code: 
    .- .-.. . -..- -.-. - ..-. - .... .---- ..... --- .---- ... --- ..... ..- .--. ...-- .-. --- ..... . -.-. .-. ...-- - --- - -..- -
    Using an online translater: 
    ALEXCTFTH15O1SO5UP3RO5ECR3TOTXT
    The last step was to replace the 'O' to '_', and insert the brackets.
    Flag: ALEXCTF{TH15_1S_5UP3R_5ECR3T_TXT} '''
