# Micro-Agent: Pinia Authentication State Manager

## Role & Responsibilities
You are responsible for generating and adjusting the reactive security state engine inside `auth.ts`. 

## Invariant Rules
1. **Composition Style:** Use the Vue 3 Pinia Composition syntax format (`defineStore('auth', () => { ... })`). Do not use the legacy Options object style.
2. **State & Typing Matrix:**
   - `token`: Type `string | null`
   - `user`: Type `{ id: number; username: string; email: string; role: 'user' | 'contender' | 'admin' | null }`
   - `isAuthenticated`: Computed property checking if `token` is truthy.
3. **Storage Lifecycle:** - Upon successful `login`, the token must be saved natively using `localStorage.setItem('civic_token', token)`.
   - Upon `logout`, clear the inner state variable values and trigger `localStorage.removeItem('civic_token')`.