### User Account Creation (T1136)
The concept is that once attacker creates a new user account, he can use that account to masquard his activities. Creating multiple accounts help the attacker to use alternative accounts to perform differnt activities. Also upon deletion of some accounts, he can use the other newly created accounts to maintain his control over the target.

#### Local Account Creation (T1136.001)
```
net user username password /ADD 

New-LocalUser -Name USERNAME -Password (ConvertTo-SecureString -AsPlainText PASSWORD -Force)
```
#### Domain Account Creation  (T1136.002)
Using cmd
``` 
net user /add /domain USERNAME PASSWORD 
```
*Keep the  `/domain` argument as it is, not need to provide the actual domain name, since we are executing this on AD or from AD joined device, this flag will try to create this user as domain user.  

Using Powershell module `Import-Module ActiveDirectory `
```
New-ADUser -Name USERNAME -GivenName FIRSTNAME -Surname LASTNAME -SamAccountName SAMACCOUNTNAME -
UserPrincipalName USERPRINCIPALNAME -AccountPassword (ConvertTo-SecureString -AsPlainText PASSWORD -Force) 
PasswordNotRequired $true
```
#### Cloud Account Creation  (T1136.003)
We should watch for new account creations on the cloud platforms also..

Note: The above concept can be applied to all the devices, including Network, Linux and other IT/OT systems or All the devices/service which supports RBAC, authentications flows should be covered under this tactic `[T1136]`. 

TODO: Issue Observed, In normal windows log reader we are just getting the full event verbros in the descripton field, it seems not parsed correcly. 