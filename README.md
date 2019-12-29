# Codeforces Hacking Script
Automates the process of hacking solutions in codeforces Educational rounds.
# Requirements 
Refer to [requirements.txt](../master/requirements.txt)
# How to use?
* Enter your test case in input.txt. <br/> <b> Note </b>
    * Avoid using extra spaces/newline in the end
    * The maximum size of the test file can be 256KB dur to upload limit on codeforces
* Enter expected output in output.txt
* If the problem requires custom checker(e.g.- Case insensitive) then update the Checker function in [checker.py](../master/checker.py). The current checker does character by character matching.
* Run the script using 
```
python3 main.py
```

* Enter your codeforces handle, password, contest id and problem id
```
Enter your handle/email = coder_h
Enter password = ************
Enter contest id = 1283
Enter problem id = C
```
# How it works?
* The script fetches all the accepted submissions for the problem.
* Runs each code on the given test case using Codeforces' custom invocation.
* Compares the expected output and output given by the code.
* If the outputs don't match, the script hacks the solution.
