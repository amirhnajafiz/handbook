# Blockchains

## Quick Description (QD)

A blockchain is a distributed ledger technology that records transactions in a secure, tamper-evident, and decentralized manner. Each block contains a list of transactions and is linked to the previous block, forming a chain. Blockchains are designed to be resilient to failures and attacks, making them suitable for trustless environments.

### Key Concepts

- **Block:** A container for a set of transactions, along with metadata such as a timestamp and a reference (hash) to the previous block.
- **Chain:** Blocks are linked together in chronological order, forming an immutable chain.
- **Decentralization:** No single entity controls the blockchain; it is maintained by a distributed network of nodes.
- **Consensus mechanism:** Protocols used by nodes to agree on the contents of the blockchain (for example, Proof of Work or Proof of Stake).
- **Immutability:** Once data is recorded in a block and added to the chain, it cannot be altered without redoing all subsequent blocks (and, in PoW, redoing their work).
- **Smart contracts:** Self-executing code stored on the blockchain that runs when predefined conditions are met.

### Consensus Mechanisms

- **Proof of Work (PoW):** Nodes (miners) solve computational puzzles to add new blocks. Used in Bitcoin.
- **Proof of Stake (PoS):** Validators are chosen to propose and attest to new blocks based on the amount of cryptocurrency they have locked up as a "stake," which can be slashed if they misbehave. Used in Ethereum since the Merge (2022).
- **Delegated Proof of Stake (DPoS):** Stakeholders elect delegates to validate transactions and create blocks.
- **Practical Byzantine Fault Tolerance (PBFT):** Used in permissioned blockchains for fast consensus with known participants (see [PBFT](03_pbft.md)).

### Blockchain Types

- **Public blockchain:** Open to anyone (for example, Bitcoin and Ethereum).
- **Private blockchain:** Access is restricted to specific participants.
- **Consortium blockchain:** Controlled by a group of organizations.

### Use Cases

- Cryptocurrencies (for example, Bitcoin and Ethereum)
- Supply chain tracking
- Digital identity management
- Decentralized finance (DeFi)
- Voting systems

### Challenges

- **Scalability:** Handling a large number of transactions per second.
- **Energy consumption:** Especially in PoW-based blockchains.
- **Privacy:** Balancing transparency with user confidentiality.
- **Regulation:** Legal and compliance issues in different jurisdictions.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Bitcoin Whitepaper (Satoshi Nakamoto)](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)
- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)
- [Ethereum Docs: Consensus Mechanisms](https://ethereum.org/en/developers/docs/consensus-mechanisms/)
- [Ethereum Docs: Proof-of-Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
- [Ethereum Docs: Proof-of-Work](https://ethereum.org/en/developers/docs/consensus-mechanisms/pow/)
