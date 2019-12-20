# Codeforces Hacking Script
Automates the process of hacking solutions in codeforces Educational rounds.
# How to use?
* Enter your test case in input.txt
* Enter expected output in output.txt
* Run the script using 
```
python3 main.py
```

* Enter your codeforces handle, password, contest id and problem id
```
Enter your handle/email = coder_h
Enter password = ************
Enter contest id = 1278
Enter problem id = A
```
# How it works?
* The script fetches all the accepted submissions for the problem.
* Runs each code on the given test case using Codeforces' custom invocation.
* Compares the expected output and output given by the code.
* If the outputs don't match the script prints the url for hacking the solution.
