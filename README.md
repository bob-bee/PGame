🧵 Civic Threads

“Where public policy meets structural accountability.”

Civic Threads is a structured, role-based public debate platform designed to test whether constrained digital discussion can foster higher-quality public discourse than traditional, engagement-driven social media.

👁️ The Vision & Philosophy

In a world dominated by algorithms that optimize for outrage, polarization, and endless feeds, Civic Threads takes a deliberate step backward. We believe public policy discussions should be organized, role-based, transparent, and measurable.

This platform is not designed to replace governments, determine election outcomes, or act as an arbiter of absolute truth. It is an experimental, open-source digital town square governed by clear structural constraints, transparent metrics, and user accountability.

📐 Core Principles

Structure over Chaos: Threaded, highly classified statements and evidence instead of unorganized, infinite comment feeds.

Public Accountability: Real, verifiable reputations for those speaking from positions of public influence.

Open & Equal Participation: Anyone can join, read, submit structured evidence, and ask questions.

Optional Contender Role: Clear, opt-in lanes of high-accountability debate for leaders and experts.

Transparent Metrics: Complete transparency of system operation costs, funding sources, and moderation metrics.

Privacy by Design: Collecting only what is necessary, with no hidden trackers or invasive identity verification.

Development Philosophy: Build the smallest useful experiment first. Measure engagement, discourse quality, and system load, and iterate strictly based on empirical evidence.

🎭 Roles & Permissions

Civic Threads operates on a strict Role-Based Access Control (RBAC) model to preserve the integrity of debates:

Action / Capability

👥 Regular User

🛡️ Verified Contender

Explore & Read Threads

Yes

Yes

Propose & Vote on New Threads

Yes

Yes

React to Official Statements

Yes

Yes

Submit Classified Feedback (Evidence, Questions, Counterarguments)

Yes

Yes

Publish Official, Authoritative Statements

No

Yes

Systematically Reply to Community Inputs

No

Yes

🔄 The Thread Lifecycle

To maintain clean, productive discourse, policy discussions flow through a structured progression:

[ Propose ] ──> [ Vote ] ──> [ Active ] ──> [ Statements ] ──> [ Feedback ] ──> [ Follow-up ]
   User          Community    Popularity     Contenders       Community      Contender
  Creates         Decides      Triggers      Publish Form    Post Evidence    Response


Creation: Any registered user proposes a thread (e.g., "Evaluating Proposed Municipal Public Transit Expansions").

Prioritization: The community votes on the importance of the topic.

Activation: Once a thread gains enough traction, it goes Active.

Alerting: Relevant contenders are programmatically notified.

Declaration: Verified contenders publish formal, authoritative statements.

Engagement: Regular users react to statements and submit structured, classified inputs (Evidence, Clarification Questions, or Counterarguments).

Resolution: Contenders selectively publish official follow-up replies to the highest-voted structured feedback.

🛠️ Technology Stack & Architecture

Civic Threads is engineered for highly efficient async database communications on the backend and native multi-platform compilation on the frontend:

           [ Client App ] (Quasar + Vue 3 Setup + Pinia + TS)
                 │
                 ▼
          [ Reverse Proxy ] (Dockerized Gateway)
                 │
                 ▼
         [ Async Backend ] (FastAPI + Asyncpg AsyncIO Engine)
            /          \
           ▼            ▼
    [ PostgreSQL ]   [ Redis ] (Caching Layer)


Layer

Technology

Description

Frontend

Quasar CLI + Vite + TypeScript

High-performance, reactive SPA interface.

UI Design

Quasar Vue 3 + Tailwind CSS

Fluid, responsive, system-adaptive layouts.

Backend

FastAPI (Python 3.11+)

Asynchronous, high-throughput micro-framework.

Database ORM

SQLAlchemy 2.0 (SQLModel)

Async IO bindings utilizing clean relation loads.

Database

PostgreSQL 16

Relational store for structured data objects.

Caching / Store

Redis

Session caching, thread status trackers.

Authentication

JWT Auth

Safe credentials using direct bcrypt hashing.

Containers

Docker Compose

Local multi-container orchestration.

📊 Initial Data Model

The relational architecture is highly structured, ensuring clean indices on high-query reference vectors to prevent query bottlenecks:

User: id, username, email, password_hash, role (user/contender/admin), created_at

Thread: id, title, category, creator_id (FK User), status (proposed/active/archived), created_at

Statement: id, thread_id (FK Thread), contender_id (FK User), body, created_at

Community Response: id, statement_id (FK Statement), user_id (FK User), type (evidence/question/counterargument), body

Reaction: id, statement_id (FK Statement), user_id (FK User), reaction (agree/disagree)

🔌 API Blueprint (MVP Routes)

POST /auth/register - Create an account

POST /auth/login - Authenticate & obtain JWT

POST /threads - Propose a new policy topic

GET /threads - List, filter, and search threads

GET /threads/{id} - Return detailed thread views with all loaded relations

POST /statements - Post an authoritative contender position statement

POST /responses - Attach structured community feedback

POST /reactions - Toggle statement reaction counts

POST /contenders/apply - Upgrade a user's role to contender status

🤖 The Micro-Agent Workflow (Markdown-Driven Development)

This repository utilizes a localized, decentralized network of Micro-Agent Invariant Files to allow safe, fast local AI assistance using small models (such as qwen2.5-coder:7b on Ollama) without context bloating:

MasterAgent.md (Root): Instructs the local runner on strict raw-code output constraints.

backend/ModelsAgent.md: Guards database schemas, index invariants, and asynchronous loading configurations.

frontend/src/boot/AxiosAgent.md: Directs environment setup, relative build assets, and JWT token interceptors.

frontend/src/stores/AuthAgent.md: Governs reactive composition Pinia states and secure browser storage lifetimes.

To run safe, local file generation pipelines through Ollama, execute:

python3 runAgent.py pipeline


⚡ Quick Start Commands

🐳 1. Bring up the Ecosystem (Docker)

Build and spin up the backend, database, and hot-reloaded frontend instantly:

docker compose up --build


Frontend Client: http://localhost:9000

Backend Docs (Swagger): http://localhost:8000/docs

🧪 2. Run the Verification Tests

Execute the asynchronous e2e database integration test pipeline:

source backend/.venv/bin/activate
pip install pytest requests
pytest backend/test_lifecycle.py -v


📦 3. Build for Platforms

Compile the Quasar client for native platforms:

cd frontend

# Web SPA Distribution
pnpm quasar build

# Desktop App (Electron)
pnpm quasar build -m electron

# Mobile Native App (Capacitor)
pnpm quasar build -m capacitor -T [android|ios]


🛡️ Non-Goals & Boundaries

To preserve absolute clarity of scope, this platform explicitly does NOT:

Claim or mimic governmental authority.

Determine, run, or host binding election campaigns.

Implement automated fact-checking systems to determine absolute "truth" (the community surfaces contrasting perspectives through structured counter-evidence).

Replace traditional political institutions.

💰 Funding & Privacy Model

Transparent Funding: A public-facing ledger displaying infrastructure costs, donations, and runtime runway. Funded primarily by community donations, with potential optional paid ad-free tiers.

Minimalist Privacy: No tracking pixels, no biometric profiles, and full support for complete account erasure upon request.

📜 License

This project is open-source and licensed under the terms of the MIT License. Build, experiment, share.