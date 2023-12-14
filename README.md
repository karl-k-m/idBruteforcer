# idBruteforcer
This is a Python program which bruteforces Estonian ID code certs based on Date of Birth and Gender.  
It uses the public ID API. Info: https://www.skidsolutions.eu/resources/ldap/
 
It works by generating all possible ID candidates for a given DoB and Gender combination and requesting public certs for that ID from the API. If a valid cert is received, it prints the name, ID and ID type (e.g. Diplomatic ID, European Residence Card, Estonian ID card).
More info on ID numbers and how they work: https://et.wikipedia.org/wiki/Isikukood

**NB: I could not get the ldap Python library to work on Windows, but it works on Linux. If you want it to support Windows, you might have to find an alternative ldap library.**
