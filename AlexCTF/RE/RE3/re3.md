# RE3: Catalyst system (150 points)

## Hint: 
CEO of catalyst systems decided to build his own log in system from scratch, he thought that it is so safe that no one can fool around with him!

### Solution
The first thing that we noticed was that this binary was taking too long to execute.
There was a loop where sleep was called with a random variable so I nop-ed out the calls to sleep and continued from there.
The sequence, with the nops, is shown below.

As a reminder, you can hot patch a binary in R2 by opening it in write mode `r2 -w program`, or reopening it with the command `oo+`.
Then you can either seek `s` to the location and insert with `wx`. Or if you are in visual mode, enable the cursor by typing `c`, hit `i`, and type in 9090909090.

```
│       ┌─< 0x00400e65      eb3e           jmp 0x400ea5
│      ┌──> 0x00400e67      e804f9ffff     call sym.imp.rand          ; int rand(void)
│      |│   0x00400e6c      89c6           mov esi, eax
│      |│   0x00400e6e      8b55fc         mov edx, dword [rbp - local_4h]
│      |│   0x00400e71      89d0           mov eax, edx
│      |│   0x00400e73      01c0           add eax, eax
│      |│   0x00400e75      01d0           add eax, edx
│      |│   0x00400e77      8d4801         lea ecx, dword [rax + 1]    ; 0x1
│      |│   0x00400e7a      89f0           mov eax, esi
│      |│   0x00400e7c      99             cdq
│      |│   0x00400e7d      f7f9           idiv ecx
│      |│   0x00400e7f      89d0           mov eax, edx
│      |│   0x00400e81      89c7           mov edi, eax
│      |│   0x00400e83      90             nop
│      |│   0x00400e84      90             nop
│      |│   0x00400e85      90             nop
│      |│   0x00400e86      90             nop
│      |│   0x00400e87      90             nop
│      |│   0x00400e88      bf2e000000     mov edi, 0x2e               ; '.' ; int c
│      |│   0x00400e8d      e82ef8ffff     call sym.imp.putchar       ; int putchar(int c)
│      |│   0x00400e92      488b052f1220.  mov rax, qword [obj.stdout] ; [0x6020c8:8]=0x4e4728203a434347 ; LEA obj.stdout ; "GCC: (GNU) 6.1.1 20160721 (Red Hat 6.1.1-4)" @ 0x6020c8
│      |│   0x00400e99      4889c7         mov rdi, rax                ; FILE *stream
│      |│   0x00400e9c      e88ff8ffff     call sym.imp.fflush        ; int fflush(FILE *stream)
│      |│   0x00400ea1      8345fc01       add dword [rbp - local_4h], 1
│      ↑│      ; JMP XREF from 0x00400e65 (main)
│      |└─> 0x00400ea5      837dfc1d       cmp dword [rbp - local_4h], 0x1d ; [0x1d:4]=0x40000000
│      └──< 0x00400ea9      7ebc           jle 0x400e67
```

I knew that the username was saved in main as [rbp-local_10h] and the password was at [rbp-local_18h].

```
│           0x00400eb5      bfb8184000     mov edi, str.Username:      ; "Username: " @ 0x4018b8 ; const char * format
│           0x00400eba      b800000000     mov eax, 0
│           0x00400ebf      e82cf8ffff     call sym.imp.printf        ; int printf(const char *format)
│           0x00400ec4      488b45f0       mov rax, qword [rbp - local_10h]
│           0x00400ec8      4889c6         mov rsi, rax
│           0x00400ecb      bfc3184000     mov edi, 0x4018c3           ; const char * format
│           0x00400ed0      b800000000     mov eax, 0
│           0x00400ed5      e866f8ffff     call sym.imp.__isoc99_scanf; int scanf(const char *format)
│           0x00400eda      bfc6184000     mov edi, str.Password:      ; "Password: " @ 0x4018c6 ; const char * format
│           0x00400edf      b800000000     mov eax, 0
│           0x00400ee4      e807f8ffff     call sym.imp.printf        ; int printf(const char *format)
│           0x00400ee9      488b45e8       mov rax, qword [rbp - local_18h]
│           0x00400eed      4889c6         mov rsi, rax
│           0x00400ef0      bfc3184000     mov edi, 0x4018c3           ; const char * format
│           0x00400ef5      b800000000     mov eax, 0
│           0x00400efa      e841f8ffff     call sym.imp.__isoc99_scanf; int scanf(const char *format)
```

You can change the variable names in R2 using the following commands to make reversing easier. 
```
afvn local_18h password
afvn local_10h username
```

There was another loop with sleep, I nopped that out as well. In the end of main, we have the following sequence of calls.

```
│           0x00400f6e      488b45f0       mov rax, qword [rbp - username]
│           0x00400f72      4889c7         mov rdi, rax
│           0x00400f75      e820fdffff     call fcn.00400c9a
│           0x00400f7a      488b45f0       mov rax, qword [rbp - username]
│           0x00400f7e      4889c7         mov rdi, rax                ; const char * s
│           0x00400f81      e857fdffff     call sub.puts_cdd          ; int puts(const char *s)
│           0x00400f86      488b45f0       mov rax, qword [rbp - username]
│           0x00400f8a      4889c7         mov rdi, rax                ; const char * s
│           0x00400f8d      e865f9ffff     call sub.puts_8f7          ; int puts(const char *s)
│           0x00400f92      488b55e8       mov rdx, qword [rbp - password]
│           0x00400f96      488b45f0       mov rax, qword [rbp - username]
│           0x00400f9a      4889d6         mov rsi, rdx
│           0x00400f9d      4889c7         mov rdi, rax                ; const char * s
│           0x00400fa0      e8d2f9ffff     call sub.puts_977          ; int puts(const char *s)
│           0x00400fa5      488b55e8       mov rdx, qword [rbp - password]
│           0x00400fa9      488b45f0       mov rax, qword [rbp - username]
│           0x00400fad      4889d6         mov rsi, rdx
│           0x00400fb0      4889c7         mov rdi, rax                ; const char * format
│           0x00400fb3      e8bef8ffff     call sub.printf_876        ; int printf(const char *format)
│           0x00400fb8      b800000000     mov eax, 0
│           0x00400fbd      c9             leave
└           0x00400fbe      c3             ret
```

Lets look at these these functions one by one. The first one takes the username as an argument.

```
[0x00400d93]> pdf @ fcn.00400c9a 
┌ (fcn) fcn.00400c9a 67
│   fcn.00400c9a (int arg_31h);
│           ; var int local_18h @ rbp-0x18
│           ; var int local_4h @ rbp-0x4
│           ; arg int arg_31h @ rbp+0x31
│              ; CALL XREF from 0x00400f75 (main)
│           0x00400c9a      55             push rbp
│           0x00400c9b      4889e5         mov rbp, rsp
│           0x00400c9e      4883ec20       sub rsp, 0x20
│           0x00400ca2      48897de8       mov qword [rbp - local_18h], rdi
│           0x00400ca6      c745fc000000.  mov dword [rbp - local_4h], 0
│       ┌─< 0x00400cad      eb18           jmp 0x400cc7
│      ┌──> 0x00400caf      8b45fc         mov eax, dword [rbp - local_4h]
│      |│   0x00400cb2      4863d0         movsxd rdx, eax
│      |│   0x00400cb5      488b45e8       mov rax, qword [rbp - local_18h]
│      |│   0x00400cb9      4801d0         add rax, rdx                ; '('
│      |│   0x00400cbc      0fb600         movzx eax, byte [rax]
│      |│   0x00400cbf      84c0           test al, al
│     ┌───< 0x00400cc1      740c           je 0x400ccf
│     │|│   0x00400cc3      8345fc01       add dword [rbp - local_4h], 1
│     │↑│      ; JMP XREF from 0x00400cad (fcn.00400c9a)
│     │|└─> 0x00400cc7      837dfc31       cmp dword [rbp - local_4h], 0x31 ; [0x31:4]=0x40000000 ; '1'
│     │└──< 0x00400ccb      7ee2           jle 0x400caf
│     │ ┌─< 0x00400ccd      eb01           jmp 0x400cd0
│     └───> 0x00400ccf      90             nop
│       │      ; JMP XREF from 0x00400ccd (fcn.00400c9a)
│       └─> 0x00400cd0      8b45fc         mov eax, dword [rbp - local_4h]
│           0x00400cd3      89c7           mov edi, eax                ; const char * s
│           0x00400cd5      e867ffffff     call sub.puts_c41          ; int puts(const char *s)
│           0x00400cda      90             nop
│           0x00400cdb      c9             leave
└           0x00400cdc      c3             ret
```
The first function was basically strlen() as it kept a counter of chars in the username that aren't equal to 0.
Once that loop was done, it called 'sub.puts_c41' shown below.

```
[0x00400d93]> pdf @ sub.puts_c41 
┌ (fcn) sub.puts_c41 89
│   sub.puts_c41 ();
│           ; var int local_14h @ rbp-0x14
│           ; var int local_8h @ rbp-0x8
│           ; var int local_4h @ rbp-0x4
│           ; var int local_0h @ rbp-0x0
│              ; CALL XREF from 0x00400cd5 (fcn.00400c9a)
│           0x00400c41      55             push rbp
│           0x00400c42      4889e5         mov rbp, rsp
│           0x00400c45      4883ec20       sub rsp, 0x20
│           0x00400c49      897dec         mov dword [rbp - local_14h], edi
│           0x00400c4c      8b45ec         mov eax, dword [rbp - local_14h]
│           0x00400c4f      c1f802         sar eax, 2
│           0x00400c52      8945fc         mov dword [rbp - local_4h], eax
│           0x00400c55      8b45fc         mov eax, dword [rbp - local_4h]
│           0x00400c58      c1e002         shl eax, 2
│           0x00400c5b      3b45ec         cmp eax, dword [rbp - local_14h]
│       ┌─< 0x00400c5e      7523           jne 0x400c83
│       │   0x00400c60      8b45fc         mov eax, dword [rbp - local_4h]
│       │   0x00400c63      c1f802         sar eax, 2
│       │   0x00400c66      8945f8         mov dword [rbp - local_8h], eax
│       │   0x00400c69      8b45f8         mov eax, dword [rbp - local_8h]
│       │   0x00400c6c      c1e002         shl eax, 2
│       │   0x00400c6f      3b45fc         cmp eax, dword [rbp - local_4h]
│      ┌──< 0x00400c72      740f           je 0x400c83
│      ││   0x00400c74      8b45fc         mov eax, dword [rbp - local_4h]
│      ││   0x00400c77      d1f8           sar eax, 1
│      ││   0x00400c79      85c0           test eax, eax
│     ┌───< 0x00400c7b      7406           je 0x400c83
│     │││   0x00400c7d      837df800       cmp dword [rbp - local_8h], 0
│    ┌────< 0x00400c81      7414           je 0x400c97
│    │└└└─> 0x00400c83      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│    │      0x00400c88      e843faffff     call sym.imp.puts          ; int puts(const char *s)
│    │      0x00400c8d      bf00000000     mov edi, 0                  ; int status
│    │      0x00400c92      e8b9faffff     call sym.imp.exit          ; void exit(int status)
│    └────> 0x00400c97      90             nop
│           0x00400c98      c9             leave
└           0x00400c99      c3             ret
```
Huh, there is a sequence of bit shifts and checks to figure out if the length of the username was valid.
I decided to not bother dealing with the math for now as there was another function later being called that had the username as an argument. I nopped out the call to this functin to skip it for now.

And function sub.puts_cdd, which actually did check out the username, is listed below:

```
[0x00400d93]> pdf @ sub.puts_cdd 
┌ (fcn) sub.puts_cdd 182
│   sub.puts_cdd ();
│           ; var int local_28h @ rbp-0x28
│           ; var int local_20h @ rbp-0x20
│           ; var int local_18h @ rbp-0x18
│           ; var int local_10h @ rbp-0x10
│           ; var int local_8h @ rbp-0x8
│              ; CALL XREF from 0x00400f81 (main)
│           0x00400cdd      55             push rbp
│           0x00400cde      4889e5         mov rbp, rsp
│           0x00400ce1      4883ec30       sub rsp, 0x30               ; '0'
│           0x00400ce5      48897dd8       mov qword [rbp - local_28h], rdi
│           0x00400ce9      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400ced      488945f8       mov qword [rbp - local_8h], rax
│           0x00400cf1      488b45f8       mov rax, qword [rbp - local_8h]
│           0x00400cf5      8b00           mov eax, dword [rax]
│           0x00400cf7      89c0           mov eax, eax
│           0x00400cf9      488945f0       mov qword [rbp - local_10h], rax
│           0x00400cfd      488b45f8       mov rax, qword [rbp - local_8h]
│           0x00400d01      4883c004       add rax, 4
│           0x00400d05      8b00           mov eax, dword [rax]
│           0x00400d07      89c0           mov eax, eax
│           0x00400d09      488945e8       mov qword [rbp - local_18h], rax
│           0x00400d0d      488b45f8       mov rax, qword [rbp - local_8h]
│           0x00400d11      4883c008       add rax, 8
│           0x00400d15      8b00           mov eax, dword [rax]
│           0x00400d17      89c0           mov eax, eax
│           0x00400d19      488945e0       mov qword [rbp - local_20h], rax
│           0x00400d1d      488b45f0       mov rax, qword [rbp - local_10h]
│           0x00400d21      482b45e8       sub rax, qword [rbp - local_18h]
│           0x00400d25      4889c2         mov rdx, rax
│           0x00400d28      488b45e0       mov rax, qword [rbp - local_20h]
│           0x00400d2c      4801d0         add rax, rdx                ; '('
│           0x00400d2f      483d564b665c   cmp rax, 0x5c664b56
│       ┌─< 0x00400d35      7545           jne 0x400d7c
│       │   0x00400d37      488b55f0       mov rdx, qword [rbp - local_10h]
│       │   0x00400d3b      488b45e0       mov rax, qword [rbp - local_20h]
│       │   0x00400d3f      4801c2         add rdx, rax                ; '#'
│       │   0x00400d42      4889d0         mov rax, rdx
│       │   0x00400d45      4801c0         add rax, rax                ; '#'
│       │   0x00400d48      4801c2         add rdx, rax                ; '#'
│       │   0x00400d4b      488b45e8       mov rax, qword [rbp - local_18h]
│       │   0x00400d4f      4801c2         add rdx, rax                ; '#'
│       │   0x00400d52      48b8b2c700e7.  movabs rax, 0x2e700c7b2
│       │   0x00400d5c      4839c2         cmp rdx, rax
│      ┌──< 0x00400d5f      751b           jne 0x400d7c
│      ││   0x00400d61      488b45e8       mov rax, qword [rbp - local_18h]
│      ││   0x00400d65      480faf45e0     imul rax, qword [rbp - local_20h]
│      ││   0x00400d6a      4889c2         mov rdx, rax
│      ││   0x00400d6d      48b814d36a9a.  movabs rax, 0x32ac30689a6ad314
│      ││   0x00400d77      4839c2         cmp rdx, rax
│     ┌───< 0x00400d7a      7414           je 0x400d90
│     │└└─> 0x00400d7c      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│     │     0x00400d81      e84af9ffff     call sym.imp.puts          ; int puts(const char *s)
│     │     0x00400d86      bf00000000     mov edi, 0                  ; int status
│     │     0x00400d8b      e8c0f9ffff     call sym.imp.exit          ; void exit(int status)
│     └───> 0x00400d90      90             nop
│           0x00400d91      c9             leave
└           0x00400d92      c3             ret
```
Following the logic this function appears to be checking the username by running some math operations against small chunks of the username, then comparing against certain constants. We can reverse the operations by using the following algebra.

We know that the constants are: 
0x5c664b56, 0x2e700c7b2, and 0x32ac30689a6ad314.

To solve for them, we followed the logic and found the following equations.
* x - y + z = 0x5c664b56
* 3(x+z) + y = 0x2e700c7b2
* y * z = 0x32ac30689a6ad314

Where x = user[0:3], y = [4:7], and z = user[8:11] for the 12 character password we got.
Solving for the equations we got:

x = "atac", y = "tsyl", z = "oec_".
Accounting for endianness, the username was found to be: "catalyst_ceo".

I verified this by running gdb and setting a breakpoint after those functions to make sure I can pass these checks.


Function at 0x4008f7 only checked for formatting of the username, so we can skip that. But if you are curious, I was able to tell that it was simply checking for formatting because it was comparing each character against a range of ASCII values, exiting if the character is out of range. We pass this check already since we know the username.  It is listed below for completeness.

```
[0x00400d93]> pdf @ sub.puts_8f7
┌ (fcn) sub.puts_8f7 128
│   sub.puts_8f7 ();
│           ; var int local_18h @ rbp-0x18
│           ; var int local_4h @ rbp-0x4
│              ; CALL XREF from 0x00400f8d (main)
│           0x004008f7      55             push rbp
│           0x004008f8      4889e5         mov rbp, rsp
│           0x004008fb      4883ec20       sub rsp, 0x20
│           0x004008ff      48897de8       mov qword [rbp - local_18h], rdi
│           0x00400903      c745fc000000.  mov dword [rbp - local_4h], 0
│       ┌─< 0x0040090a      eb54           jmp 0x400960
│      ┌──> 0x0040090c      8b45fc         mov eax, dword [rbp - local_4h]
│      |│   0x0040090f      4863d0         movsxd rdx, eax
│      |│   0x00400912      488b45e8       mov rax, qword [rbp - local_18h]
│      |│   0x00400916      4801d0         add rax, rdx                ; '('
│      |│   0x00400919      0fb600         movzx eax, byte [rax]
│      |│   0x0040091c      3c60           cmp al, 0x60                ; '`' ; '`'
│     ┌───< 0x0040091e      7e14           jle 0x400934
│     │|│   0x00400920      8b45fc         mov eax, dword [rbp - local_4h]
│     │|│   0x00400923      4863d0         movsxd rdx, eax
│     │|│   0x00400926      488b45e8       mov rax, qword [rbp - local_18h]
│     │|│   0x0040092a      4801d0         add rax, rdx                ; '('
│     │|│   0x0040092d      0fb600         movzx eax, byte [rax]
│     │|│   0x00400930      3c7a           cmp al, 0x7a                ; 'z' ; 'z'
│    ┌────< 0x00400932      7e28           jle 0x40095c
│    │└───> 0x00400934      8b45fc         mov eax, dword [rbp - local_4h]
│    │ |│   0x00400937      4863d0         movsxd rdx, eax
│    │ |│   0x0040093a      488b45e8       mov rax, qword [rbp - local_18h]
│    │ |│   0x0040093e      4801d0         add rax, rdx                ; '('
│    │ |│   0x00400941      0fb600         movzx eax, byte [rax]
│    │ |│   0x00400944      3c5f           cmp al, 0x5f                ; '_' ; '_'
│    │┌───< 0x00400946      7414           je 0x40095c
│    ││|│   0x00400948      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│    ││|│   0x0040094d      e87efdffff     call sym.imp.puts          ; int puts(const char *s)
│    ││|│   0x00400952      bf00000000     mov edi, 0                  ; int status
│    ││|│   0x00400957      e8f4fdffff     call sym.imp.exit          ; void exit(int status)
│    └└───> 0x0040095c      8345fc01       add dword [rbp - local_4h], 1
│      ↑│      ; JMP XREF from 0x0040090a (sub.puts_8f7)
│      |└─> 0x00400960      8b45fc         mov eax, dword [rbp - local_4h]
│      |    0x00400963      4863d0         movsxd rdx, eax
│      |    0x00400966      488b45e8       mov rax, qword [rbp - local_18h]
│      |    0x0040096a      4801d0         add rax, rdx                ; '('
│      |    0x0040096d      0fb600         movzx eax, byte [rax]
│      |    0x00400970      84c0           test al, al
│      └──< 0x00400972      7598           jne 0x40090c
│           0x00400974      90             nop
│           0x00400975      c9             leave
└           0x00400976      c3             ret
```

On to the next function. This one actually takes the password variable.

```
[0x00400d93]> pdf @ sub.puts_977
┌ (fcn) sub.puts_977 714
│   sub.puts_977 ();
│           ; var int local_40h @ rbp-0x40
│           ; var int local_38h @ rbp-0x38
│           ; var int local_28h @ rbp-0x28
│           ; var int local_20h @ rbp-0x20
│           ; var int local_14h @ rbp-0x14
│              ; CALL XREF from 0x00400fa0 (main)
│           0x00400977      55             push rbp
│           0x00400978      4889e5         mov rbp, rsp
│           0x0040097b      53             push rbx
│           0x0040097c      4883ec38       sub rsp, 0x38               ; '8'
│           0x00400980      48897dc8       mov qword [rbp - local_38h], rdi
│           0x00400984      488975c0       mov qword [rbp - local_40h], rsi
│           0x00400988      488b45c8       mov rax, qword [rbp - local_38h]
│           0x0040098c      488945e0       mov qword [rbp - local_20h], rax
│           0x00400990      488b45c0       mov rax, qword [rbp - local_40h]
│           0x00400994      488945d8       mov qword [rbp - local_28h], rax
│           0x00400998      c745ec000000.  mov dword [rbp - local_14h], 0
│       ┌─< 0x0040099f      e990000000     jmp 0x400a34
│      ┌──> 0x004009a4      8b45ec         mov eax, dword [rbp - local_14h]
│      |│   0x004009a7      4863d0         movsxd rdx, eax
│      |│   0x004009aa      488b45c0       mov rax, qword [rbp - local_40h]
│      |│   0x004009ae      4801d0         add rax, rdx                ; '('
│      |│   0x004009b1      0fb600         movzx eax, byte [rax]
│      |│   0x004009b4      3c60           cmp al, 0x60                ; '`' ; '`'
│     ┌───< 0x004009b6      7e14           jle 0x4009cc
│     │|│   0x004009b8      8b45ec         mov eax, dword [rbp - local_14h]
│     │|│   0x004009bb      4863d0         movsxd rdx, eax
│     │|│   0x004009be      488b45c0       mov rax, qword [rbp - local_40h]
│     │|│   0x004009c2      4801d0         add rax, rdx                ; '('
│     │|│   0x004009c5      0fb600         movzx eax, byte [rax]
│     │|│   0x004009c8      3c7a           cmp al, 0x7a                ; 'z' ; 'z'
│    ┌────< 0x004009ca      7e64           jle 0x400a30
│    │└───> 0x004009cc      8b45ec         mov eax, dword [rbp - local_14h]
│    │ |│   0x004009cf      4863d0         movsxd rdx, eax
│    │ |│   0x004009d2      488b45c0       mov rax, qword [rbp - local_40h]
│    │ |│   0x004009d6      4801d0         add rax, rdx                ; '('
│    │ |│   0x004009d9      0fb600         movzx eax, byte [rax]
│    │ |│   0x004009dc      3c40           cmp al, 0x40                ; '@' ; '@'
│    │┌───< 0x004009de      7e14           jle 0x4009f4
│    ││|│   0x004009e0      8b45ec         mov eax, dword [rbp - local_14h]
│    ││|│   0x004009e3      4863d0         movsxd rdx, eax
│    ││|│   0x004009e6      488b45c0       mov rax, qword [rbp - local_40h]
│    ││|│   0x004009ea      4801d0         add rax, rdx                ; '('
│    ││|│   0x004009ed      0fb600         movzx eax, byte [rax]
│    ││|│   0x004009f0      3c5a           cmp al, 0x5a                ; 'Z' ; 'Z'
│   ┌─────< 0x004009f2      7e3c           jle 0x400a30
│   ││└───> 0x004009f4      8b45ec         mov eax, dword [rbp - local_14h]
│   ││ |│   0x004009f7      4863d0         movsxd rdx, eax
│   ││ |│   0x004009fa      488b45c0       mov rax, qword [rbp - local_40h]
│   ││ |│   0x004009fe      4801d0         add rax, rdx                ; '('
│   ││ |│   0x00400a01      0fb600         movzx eax, byte [rax]
│   ││ |│   0x00400a04      3c2f           cmp al, 0x2f                ; '/' ; '/'
│   ││┌───< 0x00400a06      7e14           jle 0x400a1c
│   │││|│   0x00400a08      8b45ec         mov eax, dword [rbp - local_14h]
│   │││|│   0x00400a0b      4863d0         movsxd rdx, eax
│   │││|│   0x00400a0e      488b45c0       mov rax, qword [rbp - local_40h]
│   │││|│   0x00400a12      4801d0         add rax, rdx                ; '('
│   │││|│   0x00400a15      0fb600         movzx eax, byte [rax]
│   │││|│   0x00400a18      3c39           cmp al, 0x39                ; '9' ; '9'
│  ┌──────< 0x00400a1a      7e14           jle 0x400a30
│  │││└───> 0x00400a1c      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│  │││ |│   0x00400a21      e8aafcffff     call sym.imp.puts          ; int puts(const char *s)
│  │││ |│   0x00400a26      bf00000000     mov edi, 0                  ; int status
│  │││ |│   0x00400a2b      e820fdffff     call sym.imp.exit          ; void exit(int status)
│  └└└────> 0x00400a30      8345ec01       add dword [rbp - local_14h], 1
│      ↑│      ; JMP XREF from 0x0040099f (sub.puts_977)
│      |└─> 0x00400a34      8b45ec         mov eax, dword [rbp - local_14h]
│      |    0x00400a37      4863d0         movsxd rdx, eax
│      |    0x00400a3a      488b45c0       mov rax, qword [rbp - local_40h]
│      |    0x00400a3e      4801d0         add rax, rdx                ; '('
│      |    0x00400a41      0fb600         movzx eax, byte [rax]
│      |    0x00400a44      84c0           test al, al
│      └──< 0x00400a46      0f8558ffffff   jne 0x4009a4
│           0x00400a4c      488b45e0       mov rax, qword [rbp - local_20h]
│           0x00400a50      8b10           mov edx, dword [rax]
│           0x00400a52      488b45e0       mov rax, qword [rbp - local_20h]
│           0x00400a56      4883c004       add rax, 4
│           0x00400a5a      8b00           mov eax, dword [rax]
│           0x00400a5c      01c2           add edx, eax
│           0x00400a5e      488b45e0       mov rax, qword [rbp - local_20h]
│           0x00400a62      4883c008       add rax, 8
│           0x00400a66      8b00           mov eax, dword [rax]
│           0x00400a68      01d0           add eax, edx
│           0x00400a6a      89c7           mov edi, eax                ; int seed
│           0x00400a6c      e88ffcffff     call sym.imp.srand         ; void srand(int seed)
│           0x00400a71      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400a75      8b18           mov ebx, dword [rax]
│           0x00400a77      e8f4fcffff     call sym.imp.rand          ; int rand(void)
│           0x00400a7c      29c3           sub ebx, eax
│           0x00400a7e      89d8           mov eax, ebx
│           0x00400a80      3d2a05eb55     cmp eax, 0x55eb052a
│       ┌─< 0x00400a85      7414           je 0x400a9b
│       │   0x00400a87      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400a8c      e83ffcffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400a91      bf00000000     mov edi, 0                  ; int status
│       │   0x00400a96      e8b5fcffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400a9b      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400a9f      4883c004       add rax, 4
│           0x00400aa3      8b18           mov ebx, dword [rax]
│           0x00400aa5      e8c6fcffff     call sym.imp.rand          ; int rand(void)
│           0x00400aaa      29c3           sub ebx, eax
│           0x00400aac      89d8           mov eax, ebx
│           0x00400aae      3d396cf70e     cmp eax, 0xef76c39
│       ┌─< 0x00400ab3      7414           je 0x400ac9
│       │   0x00400ab5      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400aba      e811fcffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400abf      bf00000000     mov edi, 0                  ; int status
│       │   0x00400ac4      e887fcffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400ac9      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400acd      4883c008       add rax, 8
│           0x00400ad1      8b18           mov ebx, dword [rax]
│           0x00400ad3      e898fcffff     call sym.imp.rand          ; int rand(void)
│           0x00400ad8      29c3           sub ebx, eax
│           0x00400ada      89d8           mov eax, ebx
│           0x00400adc      3d642d1ecc     cmp eax, 0xcc1e2d64
│       ┌─< 0x00400ae1      7414           je 0x400af7
│       │   0x00400ae3      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400ae8      e8e3fbffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400aed      bf00000000     mov edi, 0                  ; int status
│       │   0x00400af2      e859fcffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400af7      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400afb      4883c00c       add rax, 0xc
│           0x00400aff      8b18           mov ebx, dword [rax]
│           0x00400b01      e86afcffff     call sym.imp.rand          ; int rand(void)
│           0x00400b06      29c3           sub ebx, eax
│           0x00400b08      89d8           mov eax, ebx
│           0x00400b0a      3df5c6b6c7     cmp eax, 0xc7b6c6f5
│       ┌─< 0x00400b0f      7414           je 0x400b25
│       │   0x00400b11      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400b16      e8b5fbffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400b1b      bf00000000     mov edi, 0                  ; int status
│       │   0x00400b20      e82bfcffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400b25      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400b29      4883c010       add rax, 0x10
│           0x00400b2d      8b18           mov ebx, dword [rax]
│           0x00400b2f      e83cfcffff     call sym.imp.rand          ; int rand(void)
│           0x00400b34      29c3           sub ebx, eax
│           0x00400b36      89d8           mov eax, ebx
│           0x00400b38      3dfa1b9426     cmp eax, 0x26941bfa
│       ┌─< 0x00400b3d      7414           je 0x400b53
│       │   0x00400b3f      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400b44      e887fbffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400b49      bf00000000     mov edi, 0                  ; int status
│       │   0x00400b4e      e8fdfbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400b53      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400b57      4883c014       add rax, 0x14
│           0x00400b5b      8b18           mov ebx, dword [rax]
│           0x00400b5d      e80efcffff     call sym.imp.rand          ; int rand(void)
│           0x00400b62      29c3           sub ebx, eax
│           0x00400b64      89d8           mov eax, ebx
│           0x00400b66      3df3f00c26     cmp eax, 0x260cf0f3
│       ┌─< 0x00400b6b      7414           je 0x400b81
│       │   0x00400b6d      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400b72      e859fbffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400b77      bf00000000     mov edi, 0                  ; int status
│       │   0x00400b7c      e8cffbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400b81      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400b85      4883c018       add rax, 0x18
│           0x00400b89      8b18           mov ebx, dword [rax]
│           0x00400b8b      e8e0fbffff     call sym.imp.rand          ; int rand(void)
│           0x00400b90      29c3           sub ebx, eax
│           0x00400b92      89d8           mov eax, ebx
│           0x00400b94      3defcad410     cmp eax, 0x10d4caef
│       ┌─< 0x00400b99      7414           je 0x400baf
│       │   0x00400b9b      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400ba0      e82bfbffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400ba5      bf00000000     mov edi, 0                  ; int status
│       │   0x00400baa      e8a1fbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400baf      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400bb3      4883c01c       add rax, 0x1c
│           0x00400bb7      8b18           mov ebx, dword [rax]
│           0x00400bb9      e8b2fbffff     call sym.imp.rand          ; int rand(void)
│           0x00400bbe      29c3           sub ebx, eax
│           0x00400bc0      89d8           mov eax, ebx
│           0x00400bc2      3d24e866c6     cmp eax, 0xc666e824
│       ┌─< 0x00400bc7      7414           je 0x400bdd
│       │   0x00400bc9      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400bce      e8fdfaffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400bd3      bf00000000     mov edi, 0                  ; int status
│       │   0x00400bd8      e873fbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400bdd      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400be1      4883c020       add rax, 0x20
│           0x00400be5      8b18           mov ebx, dword [rax]
│           0x00400be7      e884fbffff     call sym.imp.rand          ; int rand(void)
│           0x00400bec      29c3           sub ebx, eax
│           0x00400bee      89d8           mov eax, ebx
│           0x00400bf0      3d9c4589fc     cmp eax, 0xfc89459c
│       ┌─< 0x00400bf5      7414           je 0x400c0b
│       │   0x00400bf7      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400bfc      e8cffaffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400c01      bf00000000     mov edi, 0                  ; int status
│       │   0x00400c06      e845fbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400c0b      488b45d8       mov rax, qword [rbp - local_28h]
│           0x00400c0f      4883c024       add rax, 0x24               ; '$'
│           0x00400c13      8b18           mov ebx, dword [rax]
│           0x00400c15      e856fbffff     call sym.imp.rand          ; int rand(void)
│           0x00400c1a      29c3           sub ebx, eax
│           0x00400c1c      89d8           mov eax, ebx
│           0x00400c1e      3d3a071324     cmp eax, 0x2413073a
│       ┌─< 0x00400c23      7414           je 0x400c39
│       │   0x00400c25      bf69104000     mov edi, str.invalid_username_or_password ; "invalid username or password" @ 0x401069 ; const char * s
│       │   0x00400c2a      e8a1faffff     call sym.imp.puts          ; int puts(const char *s)
│       │   0x00400c2f      bf00000000     mov edi, 0                  ; int status
│       │   0x00400c34      e817fbffff     call sym.imp.exit          ; void exit(int status)
│       └─> 0x00400c39      90             nop
│           0x00400c3a      4883c438       add rsp, 0x38               ; '8'
│           0x00400c3e      5b             pop rbx
│           0x00400c3f      5d             pop rbp
└           0x00400c40      c3             ret
```


There was a loop which we can ignore since it just checked for the passwords formatting that was everything from the functions entry point until 0x00400a46.

The following checks looked like red herrings at first with all the calls to rand(). But, we later discovered that the seed to rand was actually from the username!
In here, the function seeded srand with chars from the username, and then subtracted the output of rand() calls to 4 byte chunks of the password at a time.
The result of this operation was then compared against a set of constants.

What did we do? we simply dropped into gdb and used that to calculate the expected values for us.
We examined $eax after returns from rand().
We knew that the 4 byte chars = constant + $eax.
We then converted to the integer value to a string using python by first converting the integer result to a hex value, and running chr() on each par of digits.
We got that part of the password. Stepped until the comparison instruction where we set $eax to the constant to force the checks for example `set $eax = 0x55eb052a`.

That wasn't the cleanest way to do this, but was the most obvious for us. In retrospect, we could have ran a C function to generate the password from us since we knew the seed.

While we did this (took a long time), I had another binary which was patched to skip over the checks.
The last function that was called was the flag generation function, it used the password to manipulated a hard coded string and printed a formatted password.
Used that to verify that our password was correct (saved me after a few typos). The final result is as follows.

```
./nochecks
 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌   ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌       ▐░▌▐░▌          ▐░▌            ▐░▌ ▐░▌  ▐░▌               ▐░▌     ▐░▌          
▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄▄▄    ▐░▐░▌   ▐░▌               ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌    ▐░▌    ▐░▌               ▐░▌     ▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌   ▐░▌               ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌       ▐░▌▐░▌          ▐░▌            ▐░▌ ▐░▌  ▐░▌               ▐░▌     ▐░▌          
▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▐░▌   ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░▌          
▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░▌          
 ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀           
Welcome to Catalyst systems
Loading..............................
Username: catalyst_ceo
Password: sLSVpQ4vK3cGWyW86AiZhggwLHBjmx9CRspVGggj
Logging in..............................
your flag is: ALEXCTF{1_t41d_y0u_y0u_ar3__gr34t__reverser__s33}
```
