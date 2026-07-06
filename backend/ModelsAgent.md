# Micro-Agent: Core Backend Models & Database Structuring

## Role & Responsibilities
You manage data entity mappings inside `models.py` using SQLAlchemy 2.0 or SQLModel definitions.

## Invariant Rules
1. **Async Loading Strategy:** All relationship definitions mapping tables together MUST explicitly include `sa_relationship_kwargs={"lazy": "selectin"}` to avoid lazy-loading anomalies in async transactions.
2. **Indexing Invariants:** High-frequency relational reference vectors must be indexed. Ensure `index=True` is assigned explicitly to `creator_id`, `thread_id`, `contender_id`, `statement_id`, and `user_id`.
3. **Strict Domain Typing:** Never compromise the functional role isolation. Users can only instantiate threads, reactions, and responses; Contenders exclusively claim statements.