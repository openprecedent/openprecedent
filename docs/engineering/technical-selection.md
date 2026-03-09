# Technical Selection

## Decision

OpenPrecedent will follow a `Python first, Rust later` technical path.

## Why Python First

The MVP problem is primarily:

- schema definition
- event ingestion
- decision extraction
- replay APIs
- retrieval experiments
- LLM and embedding integration

Python is the best fit for this stage because it maximizes iteration speed and ecosystem leverage.

## Why Not Rust First

Rust is a strong fit for future engine work, but it would slow down MVP validation if introduced as the primary implementation language now.

The current unknowns are product and model questions, not systems performance questions.

## Where Rust May Arrive Later

- high-throughput event normalization
- deterministic decision extraction engines
- policy evaluation cores
- local replay/query engines
- embeddable runtime-side components

## Initial Stack

- Python 3.12+
- `uv` for project and dependency management
- FastAPI for HTTP APIs
- Pydantic for schemas
- pytest for tests

Storage for the MVP is expected to remain simple:

- PostgreSQL for relational data
- pgvector later if retrieval needs vector support

## Constraints

- keep the MVP single-language for now
- do not introduce Rust until a clear bottleneck appears
- optimize for explainability and schema clarity before performance
