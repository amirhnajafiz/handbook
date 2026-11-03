# CDN

## Quick Description (QD)

A CDN (Content Delivery Network) is a network of distributed servers that deliver web content to users based on their geographic location. CDNs improve website performance and reliability by delivering content from servers closer to users.

### How CDNs Work

1. Content is cached on multiple servers (edge servers) worldwide.
2. User requests are routed to a nearby edge server, usually through DNS (a `CNAME` to the CDN's domain, see [DNS](01_dns.md)) or anycast routing.
3. On a cache hit, the edge server answers directly. On a cache miss, it fetches the content from the origin server, stores it, and then serves it.
4. How long an object stays cached is controlled by the origin through HTTP caching headers such as `Cache-Control` and `Expires`.

This reduces latency and the load on the origin.

### Benefits of CDNs

- Faster load times for users.
- Reduced bandwidth costs for website owners.
- Improved availability and reliability.
- Protection against traffic spikes and some attacks.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

See whether a response came from a cache by looking at the headers (the exact header names, like `X-Cache` or `CF-Cache-Status`, depend on the CDN):

```bash
curl -sI https://example.com/logo.png | grep -iE 'cache|age|via'
```

## Examples (e.g.,)

Common uses:

- Serving static assets (images, CSS, JS).
- Streaming media content.
- Distributing software updates.

## References

- [RFC 9111: HTTP Caching](https://datatracker.ietf.org/doc/html/rfc9111)
- [CDN (MDN Web Docs glossary)](https://developer.mozilla.org/en-US/docs/Glossary/CDN)
- [HTTP caching (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
