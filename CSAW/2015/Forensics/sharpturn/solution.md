sharpturn 400
I think my SATA controller is dying.
HINT ```git fsck -v```
NOTE: This writeup isn't complete, I'll erase this line when it has been completed.
---

Of course the first thing I did was untar the  file. That was a challenge in itself https://xkcd.com/1168/

Opening the folder and listing the contents we recognized that this was a git repository.

```sh
$ ls
branches  config  description  HEAD  hooks  info  objects  refs
```
The repository didn't show any code which was weird.

git logs output had some information, but git log -p also showed the diffs between the commits themselves. From that information we were able to recover the code that was being built during in this repository.

```
commit 4a2f335e042db12cc32a684827c5c8f7c97fe60b
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:11:05 2015 -0700

    All done now! Should calculate the flag..assuming everything went okay.

diff --git a/Makefile b/Makefile
new file mode 100644
index 0000000..e5e5f63
--- /dev/null
+++ b/Makefile
@@ -0,0 +1,6 @@
+
+CXXFLAGS:=-O2 -g -Wall -Wextra -Wshadow -std=c++11
+LDFLAGS:=-lcrypto
+
+ALL:
+	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o sharp sharp.cpp
diff --git a/sharp.cpp b/sharp.cpp
index d961f81..f8d0839 100644
--- a/sharp.cpp
+++ b/sharp.cpp
@@ -2,8 +2,57 @@
 #include <string>
 #include <algorithm>
 
+#include <stdint.h>
+#include <stdio.h>
+#include <openssl/sha.h>
+
 using namespace std;
 
+std::string calculate_flag(
+		std::string &part1, 
+		int64_t part2, 
+		std::string &part4,
+		uint64_t factor1,
+		uint64_t factor2)
+{
+
+	std::transform(part1.begin(), part1.end(), part1.begin(), ::tolower);
+	std::transform(part4.begin(), part4.end(), part4.begin(), ::tolower);
+
+	SHA_CTX ctx;
+	SHA1_Init(&ctx);
+
+	unsigned int mod = factor1 % factor2;
+	for (unsigned int i = 0; i < mod; i+=2)
+	{
+		SHA1_Update(&ctx,
+				reinterpret_cast<const unsigned char *>(part1.c_str()),
+				part1.size());
+	}
+
+
+	while (part2-- > 0)
+	{
+		SHA1_Update(&ctx,
+				reinterpret_cast<const unsigned char *>(part4.c_str()),
+				part1.size());
+	}
+
+	unsigned char *hash = new unsigned char[SHA_DIGEST_LENGTH];
+	SHA1_Final(hash, &ctx);
+
+	std::string rv;
+	for (unsigned int i = 0; i < SHA_DIGEST_LENGTH; i++)
+	{
+		char *buf;
+		asprintf(&buf, "%02x", hash[i]);
+		rv += buf;
+		free(buf);
+	}
+
+	return rv;
+}
+
 int main(int argc, char **argv)
 {
 	(void)argc; (void)argv; //unused
@@ -41,6 +90,11 @@ int main(int argc, char **argv)
 		factor2 = first;
 	}
 
+	std::string flag = calculate_flag(part1, part2, part4, factor1, factor2);
+	cout << "flag{";
+	cout << &lag;
+	cout << "}" << endl;
+
 	return 0;
 }
 

commit d57aaf773b1a8c8e79b6e515d3f92fc5cb332860
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:09:31 2015 -0700

    There's only two factors. Don't let your calculator lie.

diff --git a/sharp.cpp b/sharp.cpp
index 354ebf3..d961f81 100644
--- a/sharp.cpp
+++ b/sharp.cpp
@@ -24,6 +24,23 @@ int main(int argc, char **argv)
 	cout << "Part4: C.R.E.A.M. Get da _____: " << endl;
 	cin >> part4;
 
+	uint64_t first, second;
+	cout << "Part5: Input the two prime factors of the number 270031727027." << endl;
+	cin >> first;
+	cin >> second;
+
+	uint64_t factor1, factor2;
+	if (first < second)
+	{
+		factor1 = first;
+		factor2 = second;
+	}
+	else
+	{
+		factor1 = second;
+		factor2 = first;
+	}
+
 	return 0;
 }
 

commit 2e5d553f41522fc9036bacce1398c87c2483c2d5
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:08:51 2015 -0700

    It's getting better!

diff --git a/sharp.cpp b/sharp.cpp
index efda2f5..354ebf3 100644
--- a/sharp.cpp
+++ b/sharp.cpp
@@ -12,7 +12,17 @@ int main(int argc, char **argv)
 	cout << "Part1: Enter flag:" << endl;
 	cin >> part1;
 
+	int64_t part2;
+	cout << "Part2: Input 51337:" << endl;
+	cin >> part2;
 
+	std::string part3;
+	cout << "Part3: Watch this: https://www.youtube.com/watch?v=PBwAxmrE194" << endl;
+	cin >> part3;
+
+	std::string part4;
+	cout << "Part4: C.R.E.A.M. Get da _____: " << endl;
+	cin >> part4;
 
 	return 0;
 }

commit 7c9ba8a38ffe5ce6912c69e7171befc64da12d4c
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:08:05 2015 -0700

    Initial commit! This one should be fun.

diff --git a/sharp.cpp b/sharp.cpp
new file mode 100644
index 0000000..efda2f5
--- /dev/null
+++ b/sharp.cpp
@@ -0,0 +1,19 @@
+#include <iostream>
+#include <string>
+#include <algorithm>
+
+using namespace std;
+
+int main(int argc, char **argv)
+{
+	(void)argc; (void)argv; //unused
+
+	std::string part1;
+	cout << "Part1: Enter flag:" << endl;
+	cin >> part1;
+
+
+
+	return 0;
+}
+

```

Yeah, thats a lot of information....
However, the code was easily recovered from this log by cutting and pasting the data

``` cpp
#include <iostream>
#include <string>
#include <algorithm>

#include <stdint.h>
#include <stdio.h>
#include <openssl/sha.h>

using namespace std;

std::string calculate_flag(
		std::string &part1, 
		int64_t part2, 
		std::string &part4,
		uint64_t factor1,
		uint64_t factor2)
{

	std::transform(part1.begin(), part1.end(), part1.begin(), ::tolower);
	std::transform(part4.begin(), part4.end(), part4.begin(), ::tolower);

	SHA_CTX ctx;
	SHA1_Init(&ctx);

	unsigned int mod = factor1 % factor2;
	for (unsigned int i = 0; i < mod; i+=2)
	{
		SHA1_Update(&ctx,
				reinterpret_cast<const unsigned char *>(part1.c_str()),
				part1.size());
	}


	while (part2-- > 0)
	{
		SHA1_Update(&ctx,
				reinterpret_cast<const unsigned char *>(part4.c_str()),
				part1.size());
	}

	unsigned char *hash = new unsigned char[SHA_DIGEST_LENGTH];
	SHA1_Final(hash, &ctx);

	std::string rv;
	for (unsigned int i = 0; i < SHA_DIGEST_LENGTH; i++)
	{
		char *buf;
		asprintf(&buf, "%02x", hash[i]);
		rv += buf;
		free(buf);
	}

	return rv;
}

int main(int argc, char **argv)
{
	(void)argc; (void)argv; //unused

	std::string part1;
	cout << "Part1: Enter flag:" << endl;
	cin >> part1;

	int64_t part2;
	cout << "Part2: Input 51337:" << endl;
	cin >> part2;

	std::string part3;
	cout << "Part3: Watch this: https://www.youtube.com/watch?v=PBwAxmrE194" << endl;
	cin >> part3;

	std::string part4;
	cout << "Part4: C.R.E.A.M. Get da _____: " << endl;
	cin >> part4;

	uint64_t first, second;
	cout << "Part5: Input the two prime factors of the number 270031727027." << endl;
	cin >> first;
	cin >> second;

	uint64_t factor1, factor2;
	if (first < second)
	{
		factor1 = first;
		factor2 = second;
	}
	else
	{
		factor1 = second;
		factor2 = first;
	}

	std::string flag = calculate_flag(part1, part2, part4, factor1, factor2);
	cout << "flag{";
	cout << &lag;
	cout << "}" << endl;

	return 0;
}

```

There also was a makefile which made compilation simpler

``` make

CXXFLAGS:=-O2 -g -Wall -Wextra -Wshadow -std=c++11
LDFLAGS:=-lcrypto

ALL:
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o sharp sharp.cpp

```

Running make did produce an interesting output:

``` sh
$ make
g++ -O2 -g -Wall -Wextra -Wshadow -std=c++11 -lcrypto -o sharp sharp.cpp
sharp.cpp: In function ‘int main(int, char**)’:
sharp.cpp:95:11: error: ‘lag’ was not declared in this scope
  cout << &lag;
           ^
Makefile:6: recipe for target 'ALL' failed
make: *** [ALL] Error 1
```

UH-OH! Did we mess up here? double checking the logs did verify that the line was indeed the same. We decided to fix that line of code which caused a successfull compilation.

Running the code gave us a few prompts 

```
Part1: Enter flag:
Part2: Input 51337:
Part3: Watch this: https://www.youtube.com/watch?v=PBwAxmrE194
Part4: C.R.E.A.M. Get da _____: 
Part5: Input the two prime factors of the number 270031727027.
flag{da39a3ee5e6b4b0d3255bfef95601890afd80709}
```

Of course, we entered flag, then 51337, got the missing lyric from that video (money), but wait? there are more than two prime factors of 270031727027!

Thats when we re-read the challenge description

```
I think my SATA controller is dying.
```

THERE ARE CORRUPTIONS IN THE DATA!

To figure out what happened, we used *git fsck -v* which verified the data. Output is shown below

```
Checking HEAD link
Checking object directory
Checking directory ./objects/2b
Checking directory ./objects/2e
Checking directory ./objects/35
Checking directory ./objects/4a
Checking directory ./objects/4c
Checking directory ./objects/7c
Checking directory ./objects/a1
Checking directory ./objects/cb
Checking directory ./objects/d5
Checking directory ./objects/d9
Checking directory ./objects/e5
Checking directory ./objects/ef
Checking directory ./objects/f8
Checking commit 2e5d553f41522fc9036bacce1398c87c2483c2d5
Checking tree 2bd4c81f7261a60ecded9bae3027a46b9746fa4f
error: sha1 mismatch 354ebf392533dce06174f9c8c093036c138935f3
error: 354ebf392533dce06174f9c8c093036c138935f3: object corrupt or missing
Checking commit 4a2f335e042db12cc32a684827c5c8f7c97fe60b
Checking tree 4c0555b27c05dbdf044598a0601e5c8e28319f67
Checking commit 7c9ba8a38ffe5ce6912c69e7171befc64da12d4c
Checking tree a1607d81984206648265fbd23a4af5e13b289f83
Checking tree cb6c9498d7f33305f32522f862bce592ca4becd5
Checking commit d57aaf773b1a8c8e79b6e515d3f92fc5cb332860
error: sha1 mismatch d961f81a588fcfd5e57bbea7e17ddae8a5e61333
error: d961f81a588fcfd5e57bbea7e17ddae8a5e61333: object corrupt or missing
Checking blob e5e5f63b462ec6012bc69dfa076fa7d92510f22f
Checking blob efda2f556de36b9e9e1d62417c5f282d8961e2f8
error: sha1 mismatch f8d0839dd728cb9a723e32058dcc386070d5e3b5
error: f8d0839dd728cb9a723e32058dcc386070d5e3b5: object corrupt or missing
Checking connectivity (32 objects)
Checking a1607d81984206648265fbd23a4af5e13b289f83
Checking e5e5f63b462ec6012bc69dfa076fa7d92510f22f
Checking 4a2f335e042db12cc32a684827c5c8f7c97fe60b
Checking cb6c9498d7f33305f32522f862bce592ca4becd5
Checking 4c0555b27c05dbdf044598a0601e5c8e28319f67
Checking 2bd4c81f7261a60ecded9bae3027a46b9746fa4f
Checking 2e5d553f41522fc9036bacce1398c87c2483c2d5
Checking efda2f556de36b9e9e1d62417c5f282d8961e2f8
Checking 354ebf392533dce06174f9c8c093036c138935f3
missing blob 354ebf392533dce06174f9c8c093036c138935f3
Checking d57aaf773b1a8c8e79b6e515d3f92fc5cb332860
Checking f8d0839dd728cb9a723e32058dcc386070d5e3b5
missing blob f8d0839dd728cb9a723e32058dcc386070d5e3b5
Checking d961f81a588fcfd5e57bbea7e17ddae8a5e61333
missing blob d961f81a588fcfd5e57bbea7e17ddae8a5e61333
Checking 7c9ba8a38ffe5ce6912c69e7171befc64da12d4c
```

There were a few mismatched sha1sums! Thankfully, the format of a git blob is well documented.

http://www.gitguys.com/topics/what-is-the-format-of-a-git-blob/

We needed to modify the blobs to find out which bits were changed. This wasn't that hard of a process since the first couple of changes were obvious. The hardest one was the number that we needed to calculate the prime factors of.


The modifications needed to get the final solution were

modification | description
---- | ------
&lag to flag | We though this was a typo at first, so this was changed even before we did the fsck
Changing 51337 to 31337  | That was obvious since we are 31337 ;)
270031727027 to 272031727027 | iteratively modifying chars that are 1 bit off untill we got a number which only had 2 prime factors.

After each of these modifications we needed to be calculate the hash of the blob to make sure it was properly fixed, and carried over our changed to the next file.

The final prime factors were 31357 and 8675311 which, when input to the program, gave us a correct flag.

hi117 wrote code to calculate the hashes during the CTF which I don't have. I'll be writing my own code as practice when I get time.

TODO: write my own code to calculate the hashes and post here.
