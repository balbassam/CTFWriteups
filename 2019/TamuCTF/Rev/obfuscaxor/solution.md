We figured out that this binary had an encrypt function which was obfuscated
with the [obfy obfuscator](https://github.com/fritzone/obfy).
Having spent a couple of hours trying to manually reverse the operations we
found that the loop body seemed simple. After doing so, we finally saw that
the `verify_key` function strcmp the output of the encryption function to a
hardcoded string.

```gdb
disassemble verify_key(char*)
Dump of assembler code for function _Z10verify_keyPc:
   0x0000555555556059 <+0>:	push   rbp
   0x000055555555605a <+1>:	mov    rbp,rsp
   0x000055555555605d <+4>:	sub    rsp,0x20
   0x0000555555556061 <+8>:	mov    QWORD PTR [rbp-0x18],rdi
   0x0000555555556065 <+12>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000555555556069 <+16>:	mov    rdi,rax
   0x000055555555606c <+19>:	call   0x555555555420 <strlen@plt>
   0x0000555555556071 <+24>:	cmp    rax,0x9
   0x0000555555556075 <+28>:	jbe    0x555555556089 <verify_key(char*)+48>
   0x0000555555556077 <+30>:	mov    rax,QWORD PTR [rbp-0x18]
   0x000055555555607b <+34>:	mov    rdi,rax
   0x000055555555607e <+37>:	call   0x555555555420 <strlen@plt>
   0x0000555555556083 <+42>:	cmp    rax,0x40
   0x0000555555556087 <+46>:	jbe    0x555555556090 <verify_key(char*)+55>
   0x0000555555556089 <+48>:	mov    eax,0x0
   0x000055555555608e <+53>:	jmp    0x5555555560c3 <verify_key(char*)+106>
   0x0000555555556090 <+55>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000555555556094 <+59>:	mov    rdi,rax
   0x0000555555556097 <+62>:	call   0x555555555cb1 <enc(char const*)>
   0x000055555555609c <+67>:	mov    QWORD PTR [rbp-0x10],rax
   0x00005555555560a0 <+71>:	lea    rax,[rip+0x1b59]        # 0x555555557c00
   0x00005555555560a7 <+78>:	mov    QWORD PTR [rbp-0x8],rax
   0x00005555555560ab <+82>:	mov    rdx,QWORD PTR [rbp-0x10]
   0x00005555555560af <+86>:	mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555560b3 <+90>:	mov    rsi,rdx
   0x00005555555560b6 <+93>:	mov    rdi,rax
=> 0x00005555555560b9 <+96>:	call   0x555555555490 <strcmp@plt>
   0x00005555555560be <+101>:	test   eax,eax
   0x00005555555560c0 <+103>:	sete   al
   0x00005555555560c3 <+106>:	leave
   0x00005555555560c4 <+107>:	ret
End of assembler dump.
```

One thing we also discovered was that there was a minimum length needed for our
input. So, breaking at the strcmp line we ran the following.


``` gdb
$ break *verify_key+96
Breakpoint 1 at 0x20b9

$ commands
Type commands for breakpoint(s) 1, one per line.
End with a line saying just "end".
>echo "RDI: \n"
>x/4xg $rdi
>echo "RSI: \n"
>x/4xg $rsi
>end
gdb-peda$ r
Starting program: /home/gh0s1/Documents/CTF/CTFWriteups/2019/TamuCTF/Rev/obfuscaxor/obfuscaxor

Please Enter a product key to continue:
AAAAAAAAA
"RDI:
"0x555555557c00:	0x81d3c7ab9cff9eae	0xae8def9d8afbeee7
0x555555557c10:	0x0000000000000000	0x20657361656c500a
"RSI:
"0x55555576e280:	0xaeffec9faeffec9f	0x000000000000009f
0x55555576e290:	0x0000000000000000	0x0000000000000000
[----------------------------------registers-----------------------------------]
```

It was suspected that this was a straight XOR so, to test we compared the
output to our input and retested.

```python
def toAns(got, expected):
...     return (chr(got ^ ord("A") ^ expected))
```

```gdb
Starting program: /home/gh0s1/Documents/CTF/CTFWriteups/2019/TamuCTF/Rev/obfuscaxor/obfuscaxor

Please Enter a product key to continue:
p3AAAAAAA
"RDI:
"0x555555557c00:	0x81d3c7ab9cff9eae	0xae8def9d8afbeee7
0x555555557c10:	0x0000000000000000	0x20657361656c500a
"RSI:
"0x55555576e280:	0xaeffec9faeff9eae	0x000000000000009f
0x55555576e290:	0x0000000000000000	0x0000000000000000
```

Looks like we are in the right path. Continuing down we got the flag:


``` bash
echo "p3Asujmn9CEeCB3A" | nc rev.tamuctf.com 7224

Please Enter a product key to continue:
gigem{x0r_64d5by}
```
