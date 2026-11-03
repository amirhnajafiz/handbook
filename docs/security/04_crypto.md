# Cryptography

## Quick Description (QD)

Cryptography is the process of hiding or coding information so that only the person a message was intended for can read it.

### Security Basis

Separation is the basis of achieving security. However, functionality is in joining. Therefore, it should be a controlled sharing to achieve both.

There are two areas where security is needed.

1. __Communication security__: data channels, cryptographic separation is necessary
2. __System security__: security at the end points, logical separation is necessary

#### Communication Security Concerns

In a message transfer between A and B, we can have four types of concerns:

- __Interruption__ : A to B is blocked
- __Interception__ : C can see messages from A to B
- __Modification__ : C changes messages from A to B
- __Fabrication__ : C sends messages as A to B

### Cryptography

Encode the data in a manner that makes it accessible only to authorized parties. Two important factors are here, the __encryption algorithm__ and the __encryption key__. Secure algorithms are hard to develop, and keeping an algorithm secret does not scale beyond a few users. So the algorithm is assumed to be public, and only the secrecy of the key needs to be preserved (Kerckhoffs's principle).

__Security by Obscurity__ seeks to keep a system secure by keeping knowledge of it secret, and it is not a good method. Attackers always manage to find bugs one way or another. If the design is published, experts may be able to identify and report vulnerabilities before they are exploited, thus increasing security.

#### Terminology

- Plaintext = unencrypted
- Ciphertext = encrypted
- Encryption = $E_{k}(X)$
- Decryption = $D_{k}(X)$
- Cryptanalysis = discover k, X or both

#### Types of Attacks in Cryptography

In all these types, we assume that the attacker knows the encryption algorithm.

1. __Cipher text only__ : attacker only has a set of cipher texts.
2. __Known plain text__ : attacker has access to both the plain text and its encrypted version.
3. __Chosen plain text__ : attacker can select the plain text and see its encrypted version.
4. __Chosen cipher text__ : attacker can select a cipher text and see its decrypted version.
5. __Chosen text__ : attacker can choose both plain texts (seeing their encryptions) and cipher texts (seeing their decryptions).

In theory, the cryptographic algorithms have to be resistant to ciphertext only attacks. In reality, however, this is not sufficient. Some messages are much more frequently present in the traffic than others, and these messages are predictable. This is particularly true in the connection establishment phase, when the protocol mandates certain messages to be exchanged. Because the text of these messages can be predicted, that means that the attacker knows the corresponding plaintext. So, cryptographic algorithms have to be resistant to known plaintext attacks.

### Steganography

It is hiding presence of information. Use normal-looking messages/pictures that conceal secret data.

### Symmetric Cryptography

In the __symmetric cryptography__, encryption and decryption are performed with only one secret key.

#### Stream and Block Ciphers

- __Stream cipher__ is used to encrypt digital streams of data, one bit or bytes at a time.
It provides most flexibility for cryptographic applications.
- __Block cipher__ operates on data blocks that are typically 64 or 128 bits.

#### Structure of Block Ciphers

It needs to produce a reversible mapping that maps n-bit blocks to other n-bit blocks. Good ciphers are based on Shannon's concepts.

- __Diffusion__: spread the influence of each plaintext bit over many ciphertext bits, so that statistical patterns of the plaintext are dissipated (typically by permutation).
- __Confusion__: make the relationship between the key and the ciphertext as complex as possible (typically by substitution).

In principle, good ciphers can be implemented using a table of mappings in which encryption key selects which mapping to use.

#### Symmetric Cryptography Algorithms

- DES (56 bits, obsolete)
- Triple DES with two keys (112 bits of effective strength)
- AES (128, 192 or 256 bits)
- IDEA (128 bits)
- Blowfish (up to 448 bits)
- RC2 (8 to 1024 bits)
- RC5 (up to 2040 bits)
- CAST-128 (40 to 128 bits)

### Public Key (Asymmetric) Cryptography

It uses one key for encryption and another one for decryption. It requires that it be computationally infeasible to compute one of the keys based on the other. One of the two keys is private to a principal; the other key can be freely distributed to any one.

#### Encryption vs Signing

- __Encryption in public key crypto__: `A` locks a message using `B` public key, therefore only `B` can open it using its private key.
- __Authentication in public key crypto__: `A` locks a message using `A` private key, therefore `B` can open it using `A` public key.

When the encoding operation is performed using someone's public key, the results are accessible only to that person. When the encoding operation is done using someone's private key, the results are accessible to every one. By combining them, we can have both encryption and signing. So the flow is like this:

```txt
A sends a message to B:
1. A signs the message using its private key
2. A encrypts the result using B's public key
3. B decrypts it using its own private key
4. B verifies the signature using A's public key
```

#### RSA Algorithm

- Alphabet: $\{0, \ldots , n-1\}$
- Encryption: $C = M^e \mod n$
- Decryption: $M = C^d \mod n = M^{ed} \mod n$
- Both sender and receiver know n
- Sender knows e, while only the receiver knows d
- $KU = (e, n), KR = (d, n)$
- It is possible to find d, e, and n such that $M^{ed} \equiv M \mod n$
- It is infeasible to determine d from e

#### RSA Key Generation

- Select two large prime numbers p and q
- Calculate $n = p \times q$
- Calculate the number of integers less than n that are relatively prime to it, $\phi(n) = (p-1)(q-1)$.
- Select an e with $1 < e < \phi(n)$ that is relatively prime to $\phi(n)$
- Calculate $d = e^{-1} \mod \phi(n)$
- Set $KU = (e, n), KR = (d, n)$

In order to find big prime numbers, we can use __Miller-Rabin__ test for primality.

#### Miller-Rabin Test for Primality

- Pick an odd number n. Note that $n-1 = 2^k q$, where q is odd.
- Pick a number $1 < a < n-1$, compute $a^q, a^{2q}, \ldots, a^{2^k q} \bmod n$.
- If n is prime, by Fermat's theorem: $a^{2^k q} = a^{n-1} \equiv 1 \pmod n$. Moreover, the only square roots of 1 modulo a prime are $1$ and $-1$.
- So the test passes if $a^q \equiv 1$, or if $a^{2^j q} \equiv -1 \pmod n$ for some $0 \le j < k$. Otherwise n is composite.
- If it passes, n is not guaranteed to be prime. But the probability that a composite n passes for a random a is at most 0.25, so the test is repeated with several values of a.

#### Conventional vs Public Key Crypto

Conventional crypto (__symmetric or single-key cryptography__) is fast, on the other hand, public key crypto is much slower. But, key distribution is easier with public keys. Therefore, the solution is to use conventional crypto for encrypting bulk data, and use public key crypto to set up keys for such encryption.

Use __certificates__ and __certification authorities__ (CAs) to establish authenticity of public keys.

### Use of Random Numbers

When creating random numbers for cryptography, we need a strong random number generator. These random numbers are used to protect against replay attacks.

- __Pseudorandom__ number generators: Linear congruential method, which is not good for crypto
- __Natural Random Noise__: which is the best source for having randomness.
    - radiation counters
    - radio noise
    - keystroke intervals
    - network packet arrival characteristics

In Linux, the kernel gathers such noise into an entropy pool and provides cryptographically secure random numbers through `/dev/random` and `/dev/urandom` (and the `getrandom` syscall). On older kernels `/dev/random` could block when the entropy estimate was low, so `/dev/urandom` was the recommended choice; since Linux 5.6 both only block until the pool is initialized at boot.

### Digital Signatures

It provides the following required properties:

- receiver can verify who sends
- sender cannot repudiate (tell that I was not the sender)
- receiver cannot forge the signature

It uses public-key signature. Originator simply encrypts the message using its private key. When the receiver gets the message decrypted using the originator's public key, then we can be sure about who sent the message.

#### Message Digests

Encrypting the whole message for signature purposes is too inefficient. The solution is to use one-way hash functions on message and encrypt the hash using private key.

#### Common Hash Functions

- MD5 (128 bits, broken)
- SHA-1 (160 bits, broken)
- SHA-2 (e.g., SHA-256)
- SHA-3 (224 to 512 bits)
- RIPEMD-160

### Digital Certificates

Certificates are issued by a CA (certificate authority). As everyone knows the public key of the CA, a certificate for a principal A is simply A's identity and public key, signed with the CA's private key (the CA signs a hash of the certificate contents). Anyone can verify the signature with the CA's public key.

Certificates allow key exchange without real-time access to a public-key authority. A certificate binds an identity to a public key. The standard format is `X.509`.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Generate Digital Certificates

__Let’s Encrypt__ provides free SSL certificates. You can automate the process with __Certbot__, which is the recommended tool for obtaining and renewing __Let’s Encrypt__ certificates.

```sh
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com # certificates will be at /etc/letsencrypt/live/yourdomain.com/ directory
sudo certbot renew --dry-run # test the renewal process; certificates are valid for 90 days
```

Certbot usually installs a cron job or a systemd timer for automatic renewal. You can check `systemctl list-timers` or `/etc/cron.d/` for it.

You can also purchase a certificate from other CAs. Moreover, for a self-signed certificate, you can use `openssl`:

```sh
openssl req -x509 -newkey rsa:2048 -nodes -keyout private.key -out cert.crt -days 365
```

- `-x509` outputs a self-signed certificate instead of a certificate signing request.
- `-newkey rsa:2048` generates a new 2048-bit RSA key.
- `-nodes` does not encrypt the private key with a passphrase.
- `-days 365` sets the validity period.

### Notes and Comments

- Encryption with private key provides a way for digital signatures. In particular, it provides __nonrepudiability__ property. However, in practice, nonrepudiability isn't always guaranteed, since users can claim that their private key was stolen and that someone else that stole the key must have signed a certain document.
- Some of the advantages of __public key cryptography__ over symmetric key cryptography are:
  - Key distribution is easier: no secret has to be shared in advance, and each principal needs only one key pair rather than a key per pair of principals.
  - Public key crypto provides nonrepudiability without requiring a central, fully trusted server.
- In a typical TLS handshake of the old RSA key exchange, the client generates a random __session key__ and encrypts it with the server's public key; after that, the communication uses symmetric cryptography with that key. Modern TLS uses ephemeral Diffie-Hellman key exchange instead. See [Authentication](05_auth.md) for how websites use it.
- When choosing p and q for RSA, they should be of similar size but not too close to each other: if p and q are close, n can be factored quickly (Fermat's factorization method).
- Self-signed certificates can be created by the application's developer or company. Browsers do not trust them by default and show a warning, unless the certificate is added as trusted.

## Examples (e.g.,)

_Nothing here yet._

## References

- [RFC 8017: PKCS #1, RSA Cryptography Specifications v2.2](https://www.rfc-editor.org/rfc/rfc8017)
- [RFC 5280: Internet X.509 PKI Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [FIPS 197: Advanced Encryption Standard](https://csrc.nist.gov/pubs/fips/197/final)
- [random(7)](https://man7.org/linux/man-pages/man7/random.7.html)
- [openssl-req](https://docs.openssl.org/master/man1/openssl-req/)
- [Let's Encrypt: Getting Started](https://letsencrypt.org/getting-started/)
- [Certbot](https://certbot.eff.org/)
- [Miller-Rabin primality test (Wikipedia)](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
