# HTTP

## Quick Description (QD)

- HTTP (HyperText Transfer Protocol) is the protocol for transferring data on the web.
- It defines how clients (like browsers) and servers communicate.
- HTTP has evolved from simple, text-based communication (HTTP/1.1) to faster, more efficient, and secure protocols (HTTP/2 and HTTP/3) to meet modern web demands.

### HTTP/1.1

- Introduced persistent connections (keep-alive) to reuse TCP connections.
- Requests and responses are sent as plain text.
- Responses must be returned in the order of the requests, so in practice a connection handles one request at a time (head-of-line blocking). Pipelining exists but is rarely used, so browsers open several parallel connections instead.
- Widely used but can be inefficient for modern web needs.

### HTTP/2

- Uses binary framing instead of plain text, making it faster and more efficient.
- Supports multiplexing: multiple requests/responses over a single connection.
- Header compression (HPACK) reduces overhead.
- Still runs over TCP, so a single lost packet stalls all streams (TCP-level head-of-line blocking).
- Improves performance, especially for sites with many resources.

### HTTP/3

- Uses the QUIC protocol (built on [UDP](05_udp.md)) instead of [TCP](04_tcp.md).
- Reduces connection setup time (QUIC combines the transport and TLS 1.3 handshakes), so encryption is always on.
- Each stream is independent, so a lost packet only stalls the stream it belongs to. QUIC connections also survive IP address changes.
- Keeps multiplexing from HTTP/2 and uses QPACK for header compression.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Inspect the request and response headers, and the negotiated protocol version:

```bash
curl -v https://example.com -o /dev/null
curl -sI --http2 https://example.com
curl -sI --http3 https://example.com   # needs a curl built with HTTP/3 support
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
- [RFC 9112: HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112)
- [RFC 9113: HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
- [RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport](https://datatracker.ietf.org/doc/html/rfc9000)
- [Evolution of HTTP (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Evolution_of_HTTP)
