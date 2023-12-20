# idBruteforcer
This is a Python program which bruteforces Estonian ID code certs based on Date of Birth and Gender.  
It uses the public ID API. Info: https://www.skidsolutions.eu/resources/ldap/
 
It works by generating all possible ID candidates for a given DoB and Gender combination and requesting public certs for that ID from the API. If a valid cert is received, it prints the name, ID and ID type (e.g. Diplomatic ID, European Residence Card, Estonian ID card).  

As per Estonian ID documentation, ID codes and the associated names are **not** considered private information. Thereby, this code does not break any privacy laws.  

More info on ID numbers and how they work: https://et.wikipedia.org/wiki/Isikukood  

External dependencies: **python-ldap**, **rich**.

### Usage:
python3 idBruteforcer.py [OPTIONS]

Options:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**--verbose / -v**: After search, print all ID's which didn't return a cert.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**--help / -h**: Show help message.

### Key Points:
* The program (theoretically) does 10 requests per second. If you want to change this, change the sleep time in the spam_api function. I have no clue what the API's rate limit is, or if there even is a rate limit, so I just went with 10 requests per second. Increase it at your own risk.
* The search (searching for names) is not case-sensitive.
* If you search for a name (or part of a name), it will return all results which match that name. However, this filtering is done **after** the search, so it will still make requests for all possible ID's.

**NB: I could not get the ldap Python library to work on Windows, but it works on Linux. If you want it to support Windows, you might have to find an alternative ldap library.**

# Example use:
![image](https://github.com/karl-k-m/idBruteforcer/assets/74490726/c481b43b-08e8-41d7-b570-7fba01e7e4e7)
