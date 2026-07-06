System: You are an expert TypeScript/Quasar engineer. Respond ONLY with the clean code block. No explanations.

Task: Implement the Quasar Axios boot file at `frontend/src/boot/axios.ts`.

Context:
- It needs to read an environment variable `process.env.API_URL` (defaulting to http://localhost:8000).
- It must export an `api` instance.
- It must include a request interceptor that looks for a item named `civic_token` in localStorage. If found, automatically append the `Authorization: Bearer <token>` header to all outbound requests.