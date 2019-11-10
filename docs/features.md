# Features

## All

### Account Management

- Removes unauthorized users
- Adds users that should exist
- Ensures all standard users don't have admin rights
- Ensures all admin users have admin rights
- Gives all users a secure password
- Enforces change password at next logon (*Windows only*)

### Remove Software

- Polls user on what detected software to remove

## Linux

### PAM

- Enables password creation requirements
- Enables lockout for failed password attempts
- Ensures password reuse is limited
- Ensures secure password hashing algorithm is used

### Shadow Suite

- Ensures password expiration
- Ensures minimum password change days
- Ensures expiration warning
- Ensures inactive password lock
- Checks user password changed in past
- Ensures system accounts are correctly locked
- Ensures default group for the root account is GID 0
- Ensures default user umask
- Ensures default user shell timeout
- ~~Ensures root login is restricted to system console~~
- ~~Ensures access to the su command is restricted~~

### LightDM

- Disables guest account
- Hides account names

### Firewall

- Enables the uncomplicated firewall

### SSH

- Ensures permissions on important SSH files
- Ensures the following are secured: _Protocol, LogLevel, X11Forwarding, MaxAuthTries, IgnoreRhosts, HostbasedAuthentication, PermitRootLogin, PermitEmptyPasswords, PermitUserEnvironment, Ciphers, MACs, KexAlgorithms, ClientAliveInterval, ClientAliveCountMax, LoginGraceTime, Banner, UsePAM, AllowTcpForwarding, maxstartups, MaxSessions_
- ~~Ensures SSH access is limited~~

## Windows

### Apply Policies

- Applies a hardened local security policy
- Applies basic firewall rules
- Applies an advanced audit policy