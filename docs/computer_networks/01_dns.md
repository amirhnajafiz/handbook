# DNS

## Quick Description (QD)

- DNS (Domain Name System) translates human-readable domain names (like `example.com`) into IP addresses. It acts as the phonebook of the internet.
- DNS responses are cached at multiple levels (browser, OS, resolver) to speed up lookups and reduce traffic.
- DNS can also be used for aliasing and load balancing.

### How DNS Works

1. The user enters a domain in the browser.
2. The browser checks the local cache for the IP.
3. If it is not found, the query goes to a recursive DNS resolver.
4. The resolver asks the root, TLD, and authoritative DNS servers in sequence.
5. The IP address is returned and used to connect to the website.

### Types of DNS Servers

- **Root Servers:** Direct queries to the TLD servers. There are 13 root server identities (`a.root-servers.net` to `m.root-servers.net`), but each one is really many anycast instances spread around the world.
- **TLD Servers:** Handle top-level domains (e.g., `.com`, `.org`). Each TLD is run by its own registry operator.
- **Authoritative Servers:** Hold the actual records (like domain-to-IP mappings) for a zone.
- **Recursive Resolvers:** Not part of the zone hierarchy; they do the lookups on behalf of clients and cache the answers.

### DNS Records

- **A Record:** Maps a domain to an IPv4 address.
- **AAAA Record:** Maps a domain to an IPv6 address.
- **CNAME:** Alias for another domain.
- **MX:** Mail server information.
- **NS:** Name server for the domain.
- **TXT:** Arbitrary text, commonly used for SPF, DKIM, and domain verification.
- **SOA:** Start of authority; zone metadata such as the serial number and timers.

### Common Issues

- **DNS Spoofing/Poisoning:** An attacker provides false DNS responses.
- **Propagation Delay:** DNS changes are not pushed anywhere. Resolvers keep serving the old answer until its TTL expires, so changes seem to take time to "propagate".

### DNS Security (DNSSEC)

- **DNSSEC (Domain Name System Security Extensions):** Adds digital signatures to DNS data using public-key cryptography.
- Allows resolvers to verify that DNS responses are authentic and have not been altered.
- Helps prevent attacks like DNS spoofing and cache poisoning.
- Not all domains and resolvers support DNSSEC, but adoption is increasing for better security.

### Anycast

Anycast in DNS is a routing technique used to direct users to a nearby DNS server from a group of geographically distributed servers, all sharing the same IP address.

How it works:

1. **Multiple Servers, One IP:** Many DNS servers are deployed in different physical locations (data centers around the world). All of these servers are configured with the same IP address (the anycast address).
2. **Routing Based on Network Topology:** When a user sends a DNS query to that IP address, the Internet routing system (BGP) routes the query to the topologically closest server (by BGP path, which is not always the lowest latency).
3. **Redundancy and Resilience:** If one server goes down or becomes unreachable, BGP reroutes traffic to another available anycast server without changing the IP. This provides high availability and failover capabilities.
4. **Use in Public DNS:** Major DNS providers like Cloudflare (1.1.1.1), Google DNS (8.8.8.8), and Quad9 (9.9.9.9) use anycast to make their DNS services fast and reliable worldwide.

## Installation

### Setup a DNS Server

Install BIND on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install bind9 bind9utils bind9-doc dnsutils
```

## Useful Tips/Commands (UToC)

### Configure the Zone Files

Edit BIND's main config file:

```bash
sudo nano /etc/bind/named.conf.local
```

Add a zone configuration like:

```text
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
};
```

Then create the zone file:

```bash
sudo mkdir -p /etc/bind/zones
sudo nano /etc/bind/zones/db.example.com
```

Example zone file:

```text
$TTL 604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                          2         ; Serial
                     604800         ; Refresh
                      86400         ; Retry
                    2419200         ; Expire
                     604800 )       ; Negative Cache TTL

@       IN      NS      ns1.example.com.
ns1     IN      A       192.0.2.1
www     IN      A       192.0.2.2
```

### Set the Hostname and IP

Make sure your server's hostname and IP match the names in your zone file:

```bash
sudo hostnamectl set-hostname ns1.example.com
```

### Check the BIND Configuration

```bash
sudo named-checkconf
sudo named-checkzone example.com /etc/bind/zones/db.example.com
```

### Start and Enable BIND

```bash
sudo systemctl restart bind9
sudo systemctl enable bind9
```

### Allow DNS Through the Firewall

```bash
sudo ufw allow Bind9
```

Or manually:

```bash
sudo ufw allow 53/tcp
sudo ufw allow 53/udp
```

## Examples (e.g.,)

Test your DNS server from another machine:

```bash
dig @<your_server_ip> example.com
```

## References

- [RFC 1034: Domain Names - Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
- [RFC 1035: Domain Names - Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
- [RFC 4033: DNS Security Introduction and Requirements](https://datatracker.ietf.org/doc/html/rfc4033)
- [RFC 4786: Operation of Anycast Services](https://datatracker.ietf.org/doc/html/rfc4786)
- [BIND 9 Administrator Reference Manual](https://bind9.readthedocs.io/en/latest/)
