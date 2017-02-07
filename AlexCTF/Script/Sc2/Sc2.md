# SC2: Cutie cat (150 points)

# Hint
yeah steganography challenges are the worst... that's why we got only ~~one ~~ two steganography challenges .
Hint: It scripting because we need a python library to solve the challenge, one that is made in japan.

So, at first they didn't have the hint about it being a python library. We spent a lot of time trying different steg analysis techniques and gave up.

When I saw that it was just a python library I did search on https://pypi.python.org/pypi?%3Aaction=search&term=steg&submit=search

Found this https://pypi.python.org/pypi/steganography/0.1.1

```
$ sudo pip2 install steganography
$ steganography -d cat_with_secrets.png
ALEXCTF{CATS_HIDE_SECRETS_DONT_THEY}
```
