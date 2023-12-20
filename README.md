# idBruteforcer
This is a Python program which bruteforces Estonian ID code certs based on Date of Birth and Gender.  
It uses the public ID API. Info: https://www.skidsolutions.eu/resources/ldap/
 
It works by generating all possible ID candidates for a given DoB and Gender combination and requesting public certs for that ID from the API. If a valid cert is received, it prints the name, ID and ID type (e.g. Diplomatic ID, European Residence Card, Estonian ID card).  

As per Estonian ID documentation, ID codes and the associated names are **not** considered private information. Thereby, this code does not break any privacy laws.  

More info on ID numbers and how they work: https://et.wikipedia.org/wiki/Isikukood  

External dependencies: **python-ldap**, **rich**.

**NB: I could not get the ldap Python library to work on Windows, but it works on Linux. If you want it to support Windows, you might have to find an alternative ldap library.**

# Example use:
![image](https://github.com/karl-k-m/idBruteforcer/assets/74490726/c481b43b-08e8-41d7-b570-7fba01e7e4e7)
