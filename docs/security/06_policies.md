# Security Policies and Enforcement Mechanisms

## Quick Description (QD)

In this chapter, our focus is on policies and their enforcement. Basically, we want to limit the operations and force entities to follow these limits.

### Terminology and Concepts

In access control, three kinds of entities exist:

1. __Principals__ (users)
2. __Subjects__ (processes)
3. __Objects__ (files, network sockets, devices, ...)

### Access Control

The basic principle of least privilege says that, throughout execution, each subject should be given the minimal access necessary to accomplish its task. The goal is to control access to operations performed by subjects on objects.

### Discretionary Access Control (DAC)

Discretionary permissions settings at owner's discretion. Meaning that permission on an object is set by its owner.

It can be modeled as a matrix:

|        | $O_{1}$ | $O_{2}$ | $O_{3}$ | $\ldots$ |
|--------|:-------:|:-------:|:-------:|:--------:|
| User 1 | rw | w | - | $\ldots$ |
| $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ |
| User N | r | wx | - | $\ldots$ |

Implementations:

- __Access-control lists (ACLs)__
    - the AC-matrix column describing access rights on an object are stored with the object
- __Capabilities__
    - row-wise representation of AC-matrix, held by the user corresponding to the row
    - user should not change them, therefore comes with cryptography mechanisms

#### Managing Permissions

In systems, manageability is improved using indirection with __groups and roles (RBAC, role based access control)__. They give the features of inheritance and negative permissions.

#### Implementation of DAC on UNIX

__Objects__:

All resources are files. Each file has an __owner__ and __group owner__. Permissions are divided into three classes (file owner, owner group, everyone else), with 3 bits of permission for each class (read/write/execute). Besides these, there are the setuid, setgid and sticky bits.

For directories:

- read means ability to list the directory.
- write means ability to create files in the directory.
- execute means the ability to access specific files if you know the name.

Permissions on newly created files are determined by `umask`. To change permissions, use `chmod`. To change ownership use `chown`.

__Subjects__:

Subjects inherit the userid, group and supplementary groups of the parent. File permission checks are performed using this userid and groups. No permission checks on superuser (userid 0). Objects created by a subject inherit the subject's userid and group.

Each process also has an effective, real and saved UID/GID. See [Operating System Security](03_os.md) for the details.

### Capabilities

A capability is a ticket to gain access to a resource: it combines an object and the access rights on it into one package. Capabilities are transferable and must be unforgeable.

- Passwords
- Certificates
- File descriptors
- Some cookies in web applications

#### In Linux

Linux capabilities split root's privileges into distinct units (e.g., `CAP_DAC_OVERRIDE`, `CAP_NET_BIND_SERVICE`). They are attached to threads and, via file attributes, to executables. To handle them, you can use the `libcap` tools (package `libcap2-bin` on Debian/Ubuntu, `libcap` on RHEL/Fedora).

- set capabilities on a binary: `sudo setcap cap_net_bind_service+ep /path/to/bin` (`e` effective, `p` permitted)
- view capabilities of a binary: `getcap /path/to/bin`
- drop a capability for a command: `sudo capsh --drop=cap_dac_override -- -c "command"`
- check capabilities of a process: `grep Cap /proc/<pid>/status`
- decode the hex masks: `capsh --decode=<mask>`

#### Implementation Drawbacks

They are more difficult to implement than ACLs. They are also difficult to manage, therefore, capabilities in their purest form are not widely used in OSes.

However, they provide a better framework than ACLs when one or more of the following conditions hold:

- Policy enforcement isn't centralized.
- Parties have limited trust on each other.
- Rights need to move with principals.

### Mandatory Access Control (MAC)

There are limitations for DAC:

- _Trojan Horse_ problem: DAC assumes that users authorize all actions of their processes. But a process may not follow the user's intent (e.g., malware), or users may be unable to fully control their processes because of their complexity.
- DAC provides no protection if a resource owner did not bother to set the ACL properly.

To overcome these problems, MAC moves the responsibility to a central point, typically the __system administrator__.

#### Multi-Level Security (MLS)

Access control policies do not provide any way to control the manner in which information is used. Once an entity is given access to some data, it can use this information in any way. MLS policies control __information flow__, and hence control how information is used.

#### Confidentiality Policies

An object is labeled with a level L (unclassified, classified, secret, top secret). A subject is associated with a clearance level C. A subject may read an object if its clearance level is equal to or above the object's level.

#### MLS: Bell-LaPadula Model

To prevent leakage of sensitive information, we ensure:

1. No __read-up__: a subject S can read object O only if $C(S) \geq L(O)$
2. No __write-down__: a subject can write an object O only if $L(O) \geq C(S)$

This ensures that information can flow only upwards in terms of confidentiality level.

#### MLS: Biba Model (Integrity)

Designed to ensure integrity rather than confidentiality. We want to keep high-integrity subjects and objects safe from contamination by lower-integrity ones. So information can flow only downwards: a subject can write to objects at or below its own level, and it can read only from objects at or above its own level.

- No __read-down__: a subject S can read object O only if $C(S) \leq L(O)$
- No __write-up__: a subject S can write an object O only if $C(S) \geq L(O)$

#### Low Water-Mark Policy (LOMAC)

Allows read-downs, but lowers the subject's level to the level of the object it has read.

#### Problems with Information Flow

- __Label creep__: as more and more objects become sensitive, it is difficult for the system to be used by lower-clearance subjects.
- No controlled mechanism for making __exceptions__.

#### Alternative Approaches

The key goal is to mitigate damage that may result from all powerful root privileges. So, we should break down root privilege into a number of sub-privileges, and decouple user privileges from program privileges. Like:

- Domain and type enforcement: SELinux (Red Hat, Fedora), AppArmor (Debian, Ubuntu, SUSE)
- Linux capabilities (see above)

### Domain and Type Enforcement (DTE)

All subjects belong to __domains__. Users have default domains, but not all their processes belong to the same domain. Objects belong to __types__. DTE policies specify which domains have what access rights on which types.

Processes can transition to another domain, typically when executing another program. These domain transitions are an important feature.

#### DTE and SELinux

__Security-enhanced Linux (aka SELinux)__ combines standard UNIX DAC with DTE. Intuitively, the idea is to make access rights a function of the user, the program, and the object.

Generally speaking, MLS requires us to trust a program fully, or not trust it at all. In contrast, DTE allows us to express limited trust that is a function of the program. It grants a program only those rights that it needs to carry out its function.

#### SELinux vs Information Flow

In practice, DTE has turned out to be _one policy per application_. Therefore, scalability is an issue. In addition, SELinux policies are quite complex. On the other hand, information flow policies are simpler and closely related to high-level objectives. But, neither approach is easy enough for widespread use.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Managing Access in Linux

There are three important entities:

- __Owner__: the user who created a file or directory is its owner.
- __User__: any person or system component with a user account on the system.
- __Group__: a collection of users. Each user belongs to at least one group, and each file has a group associated with it.

To see the system users, run `cat /etc/passwd` (it is world-readable; password hashes live in `/etc/shadow`). Each line is `name:password:uid:gid:comment:home:shell`:

```txt
root:x:0:0:root:/root:/bin/bash
user1:x:1001:1001::/home/user1:/bin/bash
alice:x:1002:1002::/home/alice:/bin/bash
```

#### File Permissions

Every file or directory in Linux has an owner and belongs to a group:

```sh
-rw-r--r-- 1 user1 group1 1024 Oct  7 10:00 file.txt
```

The permissions are for owner, group, and others. In the octal notation of `chmod`, each digit is the sum of permissions:

- 4 = Read
- 2 = Write
- 1 = Execute

For example, `755` means:

- Owner: read/write/execute
- Group: read/execute
- Others: read/execute

To change file and directory permissions, these commands are used:

- change ownership: `chown <user>:<group> <file>`
- change permissions: `chmod <permissions> <file>`

#### User and Group Management

The following commands are used to manage users and groups:

- add a user: `useradd <username>`
- set a user's password: `passwd <username>`
- create a group: `groupadd <groupname>`
- add a user to a group: `usermod -aG <group> <user>`
- view group memberships: `groups <username>`

#### Add User for SSH

1. Create the user: `sudo useradd -m -s /bin/bash <username>`
2. Set password for user: `sudo passwd <username>`
3. Enable SSH access for the user:
   1. switch to user: `su - <username>`
   2. create `.ssh` directory: `mkdir ~/.ssh && chmod 700 ~/.ssh`
   3. add the user's public key: `echo "<user-public-key>" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`
   4. as root, check that `/etc/ssh/sshd_config` has `PubkeyAuthentication yes`
   5. restart the ssh service: `sudo systemctl restart sshd` (the unit is named `ssh` on Debian/Ubuntu)
4. To allow password authentication
   1. edit `/etc/ssh/sshd_config` and set `PasswordAuthentication yes` (and, to forbid root logins over SSH, `PermitRootLogin no`)
   2. restart the ssh service as above

Now users can log in using SSH:

```sh
ssh <username>@<server-ip>
ssh -i <private-key-file> <username>@<server-ip>
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html)
- [setcap(8)](https://man7.org/linux/man-pages/man8/setcap.8.html)
- [capsh(1)](https://man7.org/linux/man-pages/man1/capsh.1.html)
- [chmod(1)](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [useradd(8)](https://man7.org/linux/man-pages/man8/useradd.8.html)
- [sshd_config(5)](https://man7.org/linux/man-pages/man5/sshd_config.5.html)
- [Bell-LaPadula model (Wikipedia)](https://en.wikipedia.org/wiki/Bell%E2%80%93LaPadula_model)
- [Biba model (Wikipedia)](https://en.wikipedia.org/wiki/Biba_Model)
- [Linux Security Modules](https://www.kernel.org/doc/html/latest/admin-guide/LSM/index.html)
