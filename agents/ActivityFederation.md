Role: Backend Protocol Engineer.
Mandate: Implement ActivityPub endpoints.
Requirements:

Create backend/app/api/federation.py.

Implement route /.well-known/webfinger using JRD+JSON format.

Implement /inbox for POST requests. Validate incoming JSON-LD structure.

Add a stubbed verify_signature function for future RSA security.

DEPLOYMENT NOTE: The backend Dockerfile must install requests and cryptography (required for signature verification). Ensure these are added to backend/requirements.txt by the agent before the build.