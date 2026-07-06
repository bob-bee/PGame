# Civic Threads (Working Title)

## Vision

Civic Threads is a structured debate platform designed around the idea
that public policy discussions should be organized, role-based, and
measurable.

The project is **not** intended to replace governments or elections. It
is an experimental platform for testing whether constrained discussion
produces higher-quality public discourse than traditional social media.

## Principles

-   Structured discussion over chaotic feeds
-   Public accountability
-   Open participation
-   Optional contender role
-   Transparent funding
-   Open-source development
-   Privacy by design

## Core Concepts

### Users

Regular users can: - Read threads - Open new threads - React to
statements - Submit supporting evidence, questions, or counterarguments

### Contenders

Contenders are users who opt into a higher level of public
accountability.

They can: - Publish official statements - Respond to community input -
Participate in structured debates - Leave the program at any time

## Thread Lifecycle

1.  User creates a thread.
2.  Community votes on its importance.
3.  Popular threads become active.
4.  Contenders receive notifications.
5.  Contenders publish official statements.
6.  Users react and submit structured feedback.
7.  Contenders optionally publish follow-up responses.

## Architecture

    React (Vite + TypeScript)
            │
            ▼
     FastAPI Backend
            │
     ┌──────┴────────┐
     │               │
    PostgreSQL     Redis

### Technology

  Layer        Stack
  ------------ ---------------------------
  Frontend     Quasar CLI + Vite + TypeScript
  UI           Quasar Vue3
  Backend      FastAPI
  ORM          SQLAlchemy / SQLModel
  Database     PostgreSQL
  Cache        Redis
  Auth         JWT + 2FA
  Containers   Docker Compose

## Initial Data Model

### User

-   id
-   username
-   email
-   password_hash
-   role
-   created_at

### Thread

-   id
-   title
-   category
-   creator_id
-   status
-   created_at

### Statement

-   id
-   thread_id
-   contender_id
-   body
-   created_at

### Community Response

-   id
-   statement_id
-   user_id
-   type
-   body

### Reaction

-   id
-   statement_id
-   user_id
-   reaction

## Permissions

### User

-   Read
-   Create threads
-   React
-   Submit structured responses

### Contender

Everything a user can do, plus:

-   Publish official statements
-   Reply to structured feedback

## API (MVP)

-   POST /auth/login
-   POST /threads
-   GET /threads
-   GET /threads/{id}
-   POST /statements
-   POST /responses
-   POST /reactions
-   POST /contenders/apply

## Funding

The project aims to be transparent.

Possible funding sources:

-   Donations
-   Optional ad-supported tier
-   Optional paid ad-free tier

A public dashboard should display: - Infrastructure costs - Donations
received - Current project runway

## Privacy

Goals:

-   Minimize collected personal data.
-   Support account deletion.
-   Avoid storing biometric data.
-   Use strong authentication (password + optional 2FA).

## Future Ideas (Experimental)

-   Reputation scoring
-   Transparent moderation metrics
-   Open governance proposals
-   Plugin architecture
-   AI-assisted thread summarization
-   Public API
-   Federation support

## Non-Goals

This project does **not**: - claim governmental authority - determine
election outcomes - verify political truth - replace democratic
institutions

It is an open-source experiment in structured civic discussion.

## Repository Structure

    frontend/
    backend/
    docker/
    docs/
    scripts/
    .github/

## License

TBD (MIT or Apache-2.0 recommended for broad collaboration).

## Development Philosophy

Build the smallest useful experiment first.

Measure: - discussion quality - engagement - moderation workload -
system performance

Iterate only after collecting evidence.
