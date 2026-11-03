# Authentication

## Quick Description (QD)

Authentication is to ensure that the principal is who it claims to be. It covers user authentication and authentication between systems.

### Passwords

Early systems stored plaintext passwords. After a while, they stored only one-way hashes of passwords. Then, they added a random salt per password to defeat precomputed tables (rainbow tables) and to make identical passwords hash differently.

#### Confidentiality of Stored Passwords

It is difficult to protect stored passwords. The solution is to not store plaintext passwords. Instead, use one-way hash functions and store hashed passwords. But weak passwords are still a problem, since they can be guessed.

### Attacks on Passwords

There are two types of attacks on passwords: __offline__ and __online__.

#### Offline Attacks

Attacker has access to hashed passwords, and can make an unbounded number of attempts at guessing the password. These attacks are greatly sped up by GPUs.

- __Brute-force attack__: guess password, hash, compare
- __Dictionary attack__: use an intelligent algorithm to enumerate passwords

#### Defending Against Offline Attacks

- slow down offline attacks
    - make hash algorithm slower (modern password hashes such as bcrypt, scrypt and Argon2 are designed for this)
    - make attacker repeat work for every user by using `salt`
      - Original Unix proposal: encrypt the zero block 25 times with DES, keyed by the password and perturbed by the salt, $DES_{password || salt}^{25} (0)$
- protect password file
    - `/etc/passwd` is world-readable, however the hashes are kept in `/etc/shadow`, which is readable only by root

#### Online Attacks

Attacker has no access to hashed passwords, so each attack attempt requires entering the password at the password dialog. Usually gets blocked by system limits. So, guessing is typically unsuccessful except for the most easily guessed passwords.

Password stealing is the most viable approach for succeeding in online attacks such as:

- Phishing
- Password dumps
- Network sniffers
- Keyloggers and other malware
- Password reset

#### Password Theft and Trusted Path

In order to make sure that a password is not stolen when it is used, users can use __trusted path__ which is a secure way for a user to communicate with the subsystem performing user authentication.

#### Phishing and Trusted Path

Phishing attacks typically involve tricking a user into revealing their passwords. There are three ways to defend against that:

1. __Two-stage login__ with personalized prompts
2. __TLS (SSL)__ with certificate checks provides a strong defense
3. __Two-factor authentication__

Other non-solutions:

- CAPTCHA
- Security questions
- Password rules
- Alternative password schemes

### Authentication over Networks

This authentication is needed when two systems are going to share data between themselves.

#### Server-side Authentication of Plaintext Passwords

The server doesn't trust the client computer, therefore it performs this task itself. It is a bad option unless you physically secure the network, and trust all clients on the network.

#### Host-based Authentication

Trust client host to perform user authentication. Used in network file system by using `/etc/hosts.equiv`. It is not a great option today, as users often have admin privileges on client machines.

#### Transmit Only Encrypted Passwords

Encrypt user password using a client host specific secret. Server uses client secret to decrypt and verify user password. However, attackers can use replay attacks. Therefore, __one-time passwords__ come handy.

#### One-time Passwords

Start with a password P to generate a sequence of one time passwords $Q_{1}, \ldots , Q_{N}$. No password should provide any info about the other passwords. Using a one-way hash function $H$ (the S/KEY scheme), $Q_{k} = H^{N-k}(P)$, i.e., $H$ applied $N-k$ times. So, the protocol goes as follows:

1. System sends user $(i)$
2. User sends system $H^{N-i}(P)$
3. Even if user doesn't respond, use $i+1$ as next challenge

The system need not store P, just the previous OTP: it checks that hashing the received value once gives the previously stored one, and then stores the received value. Since $H$ is one-way, a sniffed OTP does not reveal the next one.

#### Other OTPs: SecurID

- A hand-held token sold by RSA.
- Uses a device-specific secret to generate a new authentication token every minute, as a function of the secret and the current time (e.g., $AES_{K_{s}} (Time)$).
- Combined with a PIN or password.

#### Challenge-response Protocols

In these protocols, server sends a challenge to the client and waits for the response. If the client is successful in solving the challenge, the server continues the communication.

#### SSH

The following is a simplified view of the SSH authentication methods. Real SSH negotiates the session key with Diffie-Hellman, and public key authentication uses a signature over the session identifier (RFC 4252, see references).

- Password based authentication
    1. Server sends a $KU_{S}$ to client
    2. Client uses that key to send the password and a random number, $E_{KU_{s}} (K_{SES} = random()), E_{K_{SES}} (password)$
    3. Communication is encrypted using the client random number, $K_{SES}$
    4. It has a weakness, integrity of $KU_{S}$ is not assured. SSH asks the user to confirm the key the first time a server is accessed, and saves the key for use in future accesses to same server.
- Public key based authentication
    1. Client sends the server its public key, $KU_{USER}$
    2. Server checks in `.ssh/authorized_keys` to find the user key
    3. Server sends a random number encrypted using client public key, $challenge = E_{KU_{USER}} (random)$
    4. Client decrypts the message using its private key and sends the result back, which proves possession of the private key

#### Websites

Websites use password authentication over HTTPS.

1. Server sends the client its public key certificate with a key inside it
2. Client reads it and uses the server's public key to send a random number
3. All subsequent communication encrypted using that random number

### Improving Password Schemes

- Master password: a master password is used to encrypt all other passwords
- Public keys like SSH or PGP
- Two-factor authentication
- One-time passwords or PINs

#### Password Management Challenges

- easy-to-remember passwords may be easy to guess, using dictionary attacks
- password management dealing with multiple passwords, or password selection rules
- shared devices problem
- stolen devices

#### Using Master Passwords

A master password is used to encrypt all other passwords. The focus on creating one strong password. When using it, user password choices will no longer be constrained by memorability concerns. As a result, a user can create random passwords for any domain, encrypt it using the master password and store it anywhere.

#### Benefits of Password Managers

- Allows strong passwords unique to each website.
- Reduces theft due to practices such as writing them down.
- Password managers are harder to phish, since they fill in passwords only for the domain they were saved for.

#### Biometrics

Authenticate by recognizing some aspect of human physiology, anatomy, skill or trait. It can be __physiological__ or __behavioral__. It is convenient, it protects against poor choice of passwords, and it is more difficult to steal. However, it needs special equipment and is not 100% reliable. Also, biometric traits cannot be changed once compromised.

#### Issues

- False match or acceptance rate (FMR/FAR), __"fraud rate"__
- False non-match/rejection rate (FNMR/FRR), __"insult rate"__
  - there is a trade-off between these two rates
- __Verification__ (pair-wise comparison) vs __Identification__ (one-to-many comparison)

#### Handwritten Signatures

Routinely used in transactions and contracts. Recognition may be manual, machine-assisted or completely mechanical.

#### Fingerprints

Most commonly used biometric. However, even low error rates can compound when doing
a one-to-many match.

Other methods are:

- Iris recognition
- Voice recognition
- Keystroke dynamics
- DNA

#### Problems with Biometrics

- Aging of the reference data (traits change over time)
- Recordings (replay of captured data, e.g., a copied fingerprint or recorded voice)
- Collusion (a legitimate user voluntarily providing bad data)
- Reducing false accepts comes at the cost of increased false rejects

#### Visual Passwords

There are several schemes to use pictures that seem so much easier to remember than the details in an arbitrary text password.

- Using passpoints: select points on an image
- Select images from an array

#### Issues with Graphical Passwords

- Many of the basic attack techniques continue to work
  - Dictionary
  - Social engineering
- New attacks
  - Shoulder-surfing

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [NIST SP 800-63B: Digital Identity Guidelines, Authentication and Lifecycle Management](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [RFC 2289: A One-Time Password System](https://www.rfc-editor.org/rfc/rfc2289)
- [RFC 6238: TOTP, Time-Based One-Time Password Algorithm](https://www.rfc-editor.org/rfc/rfc6238)
- [RFC 4252: SSH Authentication Protocol](https://www.rfc-editor.org/rfc/rfc4252)
- [RFC 4251: SSH Protocol Architecture](https://www.rfc-editor.org/rfc/rfc4251)
