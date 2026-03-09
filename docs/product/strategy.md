# OpenPrecedent Strategy

## Positioning

OpenPrecedent is an open decision replay and precedent layer for agents.

It is not positioned as:

- a generic graph database
- a generic knowledge graph platform
- a generic RAG platform
- a generic observability platform
- a developer-only trace viewer

It is positioned as:

- a decision-centric infrastructure layer on the agent execution path
- a way to capture why a decision happened
- a way to replay and reuse historical precedent

## Why This Exists

Agent observability is becoming table stakes. Memory and graph-based context systems are also maturing. But most products still answer one of these two questions:

- what the system did
- what the system remembered

OpenPrecedent is aimed at the missing question:

- why the system made a decision, and how that decision can be reused later

## Product Thesis

The core object is not a log line and not a single trace span. The core object is a decision with:

- triggering context
- evidence
- constraints
- action taken
- outcome
- links to similar precedent

## Long-Term Direction

The long-term product direction is:

1. capture decision-relevant events
2. structure them into decision objects
3. replay and explain decisions
4. build a reusable precedent layer
5. extend toward policy-aware and governed execution
