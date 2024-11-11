# Raft Consensus Algorithm

The Raft consensus algorithm is a protocol designed to manage a replicated log in a distributed system. It ensures that multiple servers (or nodes) agree on a consistent state, even in the presence of failures. Raft is often used to implement fault-tolerant services. This is an __incomplete__ attempt at implementing Raft from scratch in Python to develop a deeper understanding about Networking in and fault tolerance in Python.

## Key Concepts

### 1. Leader Election
Raft divides time into terms, and in each term, a leader is elected. The leader handles all client interactions and log replication. If a leader fails, a new leader is elected.

### 2. Log Replication
The leader receives log entries from clients and replicates them to follower nodes. Once a majority of followers acknowledge the entries, they are considered committed.

### 3. Safety
Raft ensures that committed entries are durable and consistent across all nodes. Even if some nodes fail and recover, they will eventually reach the same state as the leader.

## Raft Components

### 1. Nodes
- **Leader**: Handles client requests and log replication.
- **Followers**: Replicate the leader's log entries.
- **Candidates**: Nodes that are trying to become the leader.

### 2. Terms
A term is a logical time unit in Raft. Each term starts with an election. Terms are identified by monotonically increasing numbers.

### 3. Log Entries
Log entries are the commands that need to be replicated across the nodes. Each entry has an index and a term number.

## Raft Operations

### 1. Leader Election
- A follower becomes a candidate if it doesn't hear from the leader.
- The candidate requests votes from other nodes.
- If a candidate receives a majority of votes, it becomes the leader.

### 2. Log Replication
- The leader appends the client's command to its log.
- The leader sends AppendEntries RPCs to followers.
- Followers append the entries to their logs and send acknowledgments.
- Once a majority of followers acknowledge, the entry is committed.

### 3. Safety Mechanisms
- **Election Safety**: At most one leader can be elected in a given term.
- **Leader Append-Only**: A leader never overwrites or deletes its log entries.
- **Log Matching**: If two logs contain an entry with the same index and term, they are identical up to that point.
- **Leader Completeness**: If a log entry is committed in a term, that entry will be present in the logs of the leaders for all higher-numbered terms.

## Advantages of Raft
- **Simplicity**: Raft is designed to be easy to understand.
- **Strong Leader**: The leader handles all client interactions, simplifying the system.
- **Consistency**: Raft ensures that all nodes have a consistent view of the log.

## Conclusion
The Raft consensus algorithm provides a robust and easy-to-understand method for achieving consensus in distributed systems. Its clear leader-based approach and strong safety guarantees make it a popular choice for building reliable, fault-tolerant services.

For more detailed information, refer to the [Raft paper](https://raft.github.io/raft.pdf).
