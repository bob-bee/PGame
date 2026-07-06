import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('civic_token') || n[1D[K
null);
  const user = ref<{ id: number; username: string; email: string; role: 'us[3D[K
'user' | 'contender' | 'admin' | null }>({
    id: null,
    username: '',
    email: '',
    role: null
  });

  // Getters
  const isAuthenticated = computed(() => !!token.value);

  // Actions
  function login(tokenValue: string, userData: { id: number; username: stri[4D[K
string; email: string; role: 'user' | 'contender' | 'admin' }) {
    token.value = tokenValue;
    user.value = userData;
    localStorage.setItem('civic_token', tokenValue);
  }

  function logout() {
    token.value = null;
    user.value = { id: null, username: '', email: '', role: null };
    localStorage.removeItem('civic_token');
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout
  };
});