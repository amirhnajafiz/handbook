# DNS

- DNS (Domain Name System) translates human-readable domain names (like `example.com`) into IP addresses. Acts as the phonebook of the internet.
- DNS responses are cached at multiple levels (browser, OS, resolver) to speed up lookups and reduce traffic.
- DNS can be used for aliasing and load balancing too.

## How DNS works?

1. User enters a domain in the browser.
2. Browser checks local cache for the IP.
3. If not found, query goes to a recursive DNS resolver.
4. Resolver asks root, TLD, and authoritative DNS servers in sequence.
5. IP address is returned and used to connect to the website.

### Types of DNS Servers

- **Root Servers:** Direct queries to TLD servers. 13 root servers.
- **TLD Servers:** Handle top-level domains (e.g., `.com`, `.org`), for each organisation.
- **Authoritative Servers:** Store actual domain-to-IP mappings.
- **Nameserver**: Can be a part of DNS hierarchy.

## DNS Records

- **A Record:** Maps domain to IPv4 address.
- **AAAA Record:** Maps domain to IPv6 address.
- **CNAME:** Alias for another domain.
- **MX:** Mail server information.
- **NS:** Name server for the domain.

## Common Issues

- **DNS Spoofing/Poisoning:** Attacker provides false DNS responses.
- **Propagation Delay:** DNS changes take time to update globally.

## DNS Security (DNSSEC)

- **DNSSEC (Domain Name System Security Extensions):** Adds digital signatures to DNS data using public-key cryptography.
- Allows resolvers to verify that DNS responses are authentic and have not been altered.
- Helps prevent attacks like DNS spoofing and cache poisoning.
- Not all domains and resolvers support DNSSEC, but adoption is increasing for better security.

## Anycast

Anycast in DNS is a routing technique used to direct users to the nearest or best-performing DNS server from a group of geographically distributed servers, all sharing the same IP address.

### How it works?

1. **Multiple Servers, One IP**: Many DNS servers are deployed in different physical locations (data centers around the world). All of these servers are configured with the same IP address (the anycast address).
2. **Routing Based on Network Topology**: When a user sends a DNS query to that IP address, the Internet routing system (BGP) routes the query to the closest or lowest-latency server, based on the user's network location.
3. **Redundancy and Resilience**: If one server goes down or becomes unreachable, BGP reroutes traffic to another available anycast server without changing the IP. This provides high availability and failover capabilities.
4. **Use in Public DNS**: Major DNS providers like Cloudflare (1.1.1.1), Google DNS (8.8.8.8), and Quad9 (9.9.9.9) use anycast to make their DNS services fast and reliable worldwide.

## Setup DNS Server

Install BIND on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install bind9 bind9utils bind9-doc dnsutils
```

Configure the Zone files, edit BIND’s main config file:

```bash
sudo nano /etc/bind/named.conf.local
```

Add a zone configuration like:

```
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

```
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

Set the Hostname and IP, make sure your server’s hostname and IP match the names in your zone file:

```bash
hostnamectl set-hostname ns1.example.com
```

Check BIND configuration:

```bash
sudo named-checkconf
sudo named-checkzone example.com /etc/bind/zones/db.example.com
```

Start and enable BIND:

```bash
sudo systemctl restart bind9
sudo systemctl enable bind9
```

Allow DNS through the firewall:

```bash
sudo ufw allow Bind9
```

Or manually:

```bash
sudo ufw allow 53/tcp
sudo ufw allow 53/udp
```

Test your DNS server from another machine:

```bash
dig @<your_server_ip> example.com
```
