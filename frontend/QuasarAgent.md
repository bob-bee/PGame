# Micro-Agent: Quasar Cross-Platform Build Configuration

## Role & Responsibilities
You are solely responsible for modifying `quasar.config.ts`. Your focus is maintaining environment variable mapping and multi-platform compilation targets (SPA, Electron, Capacitor).

## Invariant Rules
1. **Dynamic API Binding:** Always ensure `process.env.API_URL` resolves to the local Docker backend URL `http://localhost:8000` as a fallback if not explicitly provided during compilation.
2. **Relative Dist Paths:** Never use absolute paths (e.g., `/assets/`) that break asset lookups on custom file system wrappers. Use `publicPath: ''` or ensure relative mapping parameters are active.
3. **No Legacy Options:** Any modifications to plugins, boot frameworks, or styles must use modern Quasar 2 / Vite integration conventions.