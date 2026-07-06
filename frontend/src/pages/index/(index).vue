<template>
  <q-page class="q-pa-md bg-neutral-950 text-white">
    <div v-if="isDemoMode" class="max-w-7xl mx-auto mb-6 p-4 border border-white bg-neutral-950 text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-[4px_4px_0px_0px_rgba(255,255,255,1)]">
      <div class="flex items-center gap-4 text-center sm:text-left">
        <div class="hidden sm:block font-mono font-bold text-xl select-none">// // //</div>
        <div>
          <span class="font-mono font-extrabold block text-sm uppercase tracking-widest">Local Demo Simulation Active</span>
          <span class="text-xs text-neutral-400 font-mono">Backend server is offline. Simulating database transactions securely locally.</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <q-btn unelevated color="white" text-color="black" size="sm" label="Reconnect" @click="checkBackendConnection" :loading="checkingConnection" class="rounded-none font-mono font-bold hover:bg-neutral-200" />
      </div>
    </div>

    <header class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 mb-10 pb-6 border-b border-neutral-800">
      <div class="flex items-center gap-4 text-center md:text-left">
        <div class="p-2 border-2 border-white bg-white text-black font-mono font-extrabold text-2xl select-none">
          CT
        </div>
        <div>
          <h1 class="text-3xl font-mono font-black tracking-tighter uppercase text-white">Civic Threads</h1>
          <p class="text-xs font-mono tracking-widest text-neutral-400 uppercase mt-1">Structured Policy Debate Platform</p>
        </div>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-4 bg-neutral-950 p-3 border border-neutral-800">
        <div v-if="authStore.isAuthenticated && authStore.user" class="flex items-center gap-4">
          <div class="text-right">
            <span class="block text-xs font-mono font-bold uppercase tracking-wider text-neutral-200">{{ authStore.user.username }}</span>
            <span :class="roleBadgeClass" class="inline-block text-[9px] uppercase tracking-widest font-mono font-bold mt-0.5 px-2 py-0.5">
              [{{ authStore.user.role }}]
            </span>
          </div>
          <button v-if="isDemoMode" @click="toggleDemoRole" class="font-mono text-[9px] border border-neutral-700 hover:border-white px-2 py-1 text-neutral-400 hover:text-white uppercase tracking-widest transition-colors">
            Toggle Role
          </button>
          <button @click="handleSignOut" class="font-mono text-xs border border-white bg-white text-black hover:bg-neutral-200 px-3 py-1.5 font-bold uppercase tracking-wider transition-colors">
            Sign Out
          </button>
        </div>
        <div v-else class="flex gap-2">
          <button @click="showAuthModal('login')" class="font-mono text-xs bg-white text-black border border-white hover:bg-neutral-200 px-4 py-2 font-bold uppercase tracking-wider transition-all">
            Sign In
          </button>
          <button @click="showAuthModal('register')" class="font-mono text-xs text-white border border-neutral-700 hover:border-white px-4 py-2 uppercase tracking-wider transition-all">
            Register
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <section class="lg:col-span-4 flex flex-col gap-6">
        
        <div class="border border-neutral-800 bg-neutral-950 p-6 flex flex-col gap-4 relative overflow-hidden group">
          <div class="absolute right-0 top-0 text-neutral-900 text-6xl font-mono font-black select-none pointer-events-none opacity-20">
            NEW
          </div>
          <h2 class="text-md font-mono font-bold uppercase tracking-widest text-neutral-100 flex items-center gap-2">
            [+] Propose Policy Topic
          </h2>
          <p class="text-xs text-neutral-400 font-sans leading-relaxed">
            Suggest a framework, transit expansion plan, or civic budget layout requiring structured responder analysis.
          </p>
          <button @click="triggerNewThreadModal" class="w-full font-mono text-xs py-3 border-2 border-white bg-white text-black hover:bg-neutral-200 transition-colors uppercase font-bold tracking-widest">
            Propose Thread
          </button>
        </div>

        <div class="border border-neutral-800 bg-neutral-950 p-6">
          <div class="flex items-center justify-between mb-4 pb-2 border-b border-neutral-900">
            <h3 class="text-xs font-mono font-bold tracking-widest uppercase text-neutral-400">Categories</h3>
            <span class="text-[10px] font-mono border border-neutral-800 px-2 py-0.5 text-neutral-500">{{ filteredThreads.length }} Threads</span>
          </div>

          <div class="flex flex-wrap gap-2 mb-6">
            <button v-for="cat in categories" 
                    :key="cat" 
                    @click="selectedCategory = cat" 
                    :class="selectedCategory === cat ? 'bg-white text-black font-bold' : 'bg-neutral-900 text-neutral-400 hover:text-white hover:bg-neutral-800 border border-neutral-800'" 
                    class="px-3 py-1 font-mono text-[10px] uppercase tracking-wider transition-all">
              {{ cat }}
            </button>
          </div>

          <h3 class="text-xs font-mono font-bold tracking-widest uppercase text-neutral-400 mb-4">Thread Stream</h3>
          
          <div v-if="loadingThreads" class="flex flex-col items-center justify-center py-12 gap-3 text-neutral-600">
            <q-spinner-tail color="white" size="28px" />
            <span class="text-[10px] font-mono uppercase tracking-widest">Polling live stream...</span>
          </div>

          <div v-else-if="filteredThreads.length === 0" class="text-center py-12 border border-dashed border-neutral-800">
            <p class="text-xs font-mono uppercase text-neutral-500">Empty category stack.</p>
          </div>

          <div v-else class="flex flex-col gap-3 max-h-[480px] overflow-y-auto pr-1">
            <div v-for="thread in filteredThreads" 
                 :key="thread.id" 
                 @click="selectThread(thread)" 
                 :class="activeThread && activeThread.id === thread.id ? 'border-white bg-neutral-900 shadow-md' : 'border-neutral-800 bg-neutral-950/40 hover:border-neutral-700'" 
                 class="p-4 border transition-all duration-150 cursor-pointer flex flex-col gap-2">
              
              <div class="flex items-center justify-between">
                <span class="text-[9px] font-mono border border-neutral-700 px-2 py-0.5 uppercase tracking-widest text-neutral-400">
                  {{ thread.category }}
                </span>
                <span class="text-[9px] font-mono font-bold uppercase tracking-wider text-neutral-500">
                  &lt;{{ thread.status }}&gt;
                </span>
              </div>
              
              <h4 :class="activeThread && activeThread.id === thread.id ? 'text-white underline decoration-1' : 'text-neutral-300'" class="font-mono font-bold text-xs leading-snug transition-colors">
                {{ thread.title }}
              </h4>
              
              <div class="flex items-center justify-between text-[10px] font-mono text-neutral-500 mt-1 pt-1 border-t border-neutral-900">
                <span>By user #{{ thread.creator_id }}</span>
                <span>{{ formatDate(thread.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="lg:col-span-8">
        
        <div v-if="!activeThread" class="h-full min-h-[500px] flex flex-col items-center justify-center border border-neutral-800 bg-neutral-950/20 p-8 text-center">
          <div class="w-12 h-12 border-2 border-neutral-800 text-neutral-600 flex items-center justify-center font-mono font-black text-xl mb-4 select-none">
            ?
          </div>
          <h3 class="text-md font-mono font-bold text-neutral-300 uppercase tracking-widest">No Thread Active</h3>
          <p class="text-xs text-neutral-500 max-w-sm mt-2 leading-relaxed font-sans">
            Please pick a public policy proposal from the list stream on the left to analyze the active debate, contender responses, and verification documents.
          </p>
        </div>

        <div v-else class="border border-neutral-800 bg-neutral-950 p-6 md:p-8 flex flex-col gap-6">
          
          <div class="border-b border-neutral-800 pb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-3">
                <span class="text-[10px] font-mono border-2 border-white bg-white text-black px-3 py-0.5 uppercase tracking-wider font-bold">
                  {{ activeThread.category }}
                </span>
                <span class="text-[10px] font-mono text-neutral-400 font-bold uppercase tracking-widest">
                  &lt;{{ activeThread.status }}&gt;
                </span>
              </div>
              <h2 class="text-xl font-mono font-black text-white leading-tight uppercase">
                {{ activeThread.title }}
              </h2>
            </div>
            <div class="text-[10px] font-mono text-neutral-500 text-left sm:text-right">
              <span class="block">CREATOR_ID: #{{ activeThread.creator_id }}</span>
              <span class="block mt-1">INIT_DATE: {{ formatDate(activeThread.created_at) }}</span>
            </div>
          </div>

          <div>
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <h3 class="text-xs font-mono font-bold text-neutral-200 uppercase tracking-widest flex items-center gap-2">
                [//] Contender Statements
              </h3>
              
              <div v-if="authStore.user?.role === 'contender' || authStore.user?.role === 'admin'">
                <button @click="showStatementForm = !showStatementForm" class="font-mono text-[10px] uppercase tracking-wider font-bold border border-white bg-white text-black hover:bg-neutral-200 px-4 py-2">
                  {{ showStatementForm ? 'Close Workspace' : 'Publish Stance' }}
                </button>
              </div>
            </div>

            <div v-if="showStatementForm" class="border border-neutral-700 bg-neutral-900 p-5 mb-6 shadow-sm">
              <h4 class="text-xs font-mono font-bold text-white uppercase tracking-widest flex items-center gap-2 mb-3">
                &gt; Formulate Authoritative Declaration
              </h4>
              <p class="text-xs text-neutral-400 mb-4 font-sans leading-relaxed">
                Provide structured, cited commentary. Statements submitted here will represent your public, auditable policy vectors on this topic.
              </p>
              <q-input v-model="newStatementBody" 
                       type="textarea" 
                       dark 
                       filled 
                       square 
                       borderless 
                       bg-color="neutral-950" 
                       color="white" 
                       placeholder="Enter statement payload..." 
                       class="font-mono text-xs border border-neutral-800" 
                       rows="4" />
              <div class="flex justify-end gap-3 mt-4">
                <button @click="showStatementForm = false" class="font-mono text-[10px] uppercase tracking-widest text-neutral-400 hover:text-white px-3 py-2">
                  Cancel
                </button>
                <button @click="handlePublishStatement" :disabled="publishingStatement" class="font-mono text-[10px] uppercase tracking-widest border border-white bg-white text-black hover:bg-neutral-200 px-4 py-2 font-bold">
                  {{ publishingStatement ? 'Publishing...' : 'Execute Publish' }}
                </button>
              </div>
            </div>

            <div v-if="!activeThread.statements || activeThread.statements.length === 0" class="text-center py-12 border border-dashed border-neutral-800">
              <p class="text-xs font-mono uppercase text-neutral-500">No authoritative stances filed on this thread.</p>
            </div>

            <div v-else class="flex flex-col gap-6">
              <div v-for="statement in activeThread.statements" :key="statement.id" class="border border-neutral-800 bg-neutral-950/60 p-5 md:p-6 flex flex-col gap-4">
                
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-neutral-900 pb-3">
                  <div class="flex items-center gap-3">
                    <div class="w-6 h-6 border border-white text-white flex items-center justify-center font-mono font-bold text-[10px] select-none">
                      V
                    </div>
                    <div>
                      <span class="block text-[10px] font-mono font-bold uppercase tracking-wider text-white">CONTENDER_ID: #{{ statement.contender_id }}</span>
                      <span class="text-[9px] font-mono text-neutral-500">{{ formatDate(statement.created_at) }}</span>
                    </div>
                  </div>
                  
                  <div class="flex items-center gap-2 bg-neutral-950 border border-neutral-800 px-2 py-1 font-mono text-[10px]">
                    <button @click="handleReaction(statement.id, 'agree')" 
                            :class="hasUserReacted(statement.id, 'agree') ? 'bg-white text-black font-extrabold' : 'text-neutral-400 hover:text-white'" 
                            class="px-2 py-0.5 tracking-wider transition-all uppercase">
                      AGREE [{{ getReactionCount(statement.id, 'agree') }}]
                    </button>
                    <span class="text-neutral-800">/</span>
                    <button @click="handleReaction(statement.id, 'disagree')" 
                            :class="hasUserReacted(statement.id, 'disagree') ? 'bg-white text-black font-extrabold' : 'text-neutral-400 hover:text-white'" 
                            class="px-2 py-0.5 tracking-wider transition-all uppercase">
                      DISAGREE [{{ getReactionCount(statement.id, 'disagree') }}]
                    </button>
                  </div>
                </div>

                <p class="text-neutral-300 font-sans text-sm md:text-base leading-relaxed whitespace-pre-wrap selection:bg-white selection:text-black">
                  {{ statement.body }}
                </p>

                <div class="border-t border-neutral-900 pt-4 mt-2">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                    <h5 class="text-[10px] font-mono font-bold uppercase tracking-widest text-neutral-400">
                      [+] Community Feedback Modules
                    </h5>
                    
                    <button @click="triggerFeedbackForm(statement.id)" class="font-mono text-[9px] uppercase tracking-widest text-white border border-neutral-800 hover:border-white px-2.5 py-1">
                      Attach Response
                    </button>
                  </div>

                  <div v-if="feedbackFormActiveId === statement.id" class="border border-neutral-700 bg-neutral-900 p-4 mb-4 flex flex-col gap-3">
                    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                      <span class="text-[10px] font-mono font-bold text-neutral-400 uppercase tracking-widest">Classification Mode:</span>
                      <div class="flex gap-1">
                        <button v-for="mode in responseTypes" 
                                :key="mode.value" 
                                @click="selectedFeedbackType = mode.value as 'evidence' | 'question' | 'counterargument'" 
                                :class="selectedFeedbackType === mode.value ? 'bg-white text-black font-bold' : 'bg-neutral-950 text-neutral-400 border border-neutral-800'" 
                                class="px-2 py-1 font-mono text-[9px] uppercase tracking-wider transition-all">
                          {{ mode.label }}
                        </button>
                      </div>
                    </div>
                    
                    <q-input v-model="newFeedbackBody" 
                             type="textarea" 
                             dark 
                             filled 
                             square 
                             borderless 
                             bg-color="neutral-950" 
                             color="white" 
                             placeholder="Provide evidence mapping link, structured clarification or counterargument payload..." 
                             class="font-mono text-xs border border-neutral-800" 
                             rows="2" />
                             
                    <div class="flex justify-end gap-2">
                      <button @click="feedbackFormActiveId = null" class="font-mono text-[9px] uppercase tracking-widest text-neutral-400 px-3 py-1">
                        Cancel
                      </button>
                      <button @click="handleFeedbackSubmit(statement.id)" :disabled="submittingFeedback" class="font-mono text-[9px] uppercase tracking-widest border border-white bg-white text-black hover:bg-neutral-200 px-3 py-1.5 font-bold">
                        Submit Response
                      </button>
                    </div>
                  </div>

                  <div v-if="!statement.responses || statement.responses.length === 0" class="text-[10px] font-mono text-neutral-600 text-center py-4 border border-dashed border-neutral-900 uppercase tracking-wider">
                    No community inputs attached.
                  </div>
                  <div v-else class="flex flex-col gap-2.5 max-h-[300px] overflow-y-auto pr-1">
                    <div v-for="response in statement.responses" :key="response.id" class="p-3 bg-neutral-950 border border-neutral-900 flex flex-col gap-2">
                      <div class="flex items-center justify-between font-mono text-[9px]">
                        <div class="flex items-center gap-2">
                          <span :class="getFeedbackTypeClass(response.type)" class="font-bold border px-1.5 py-0.5 uppercase tracking-widest">
                            {{ response.type }}
                          </span>
                          <span class="text-neutral-500">USER_ID: #{{ response.user_id }}</span>
                        </div>
                        <span class="text-neutral-500">{{ formatDate(response.created_at) }}</span>
                      </div>
                      <p class="text-neutral-300 font-sans text-xs leading-relaxed selection:bg-white selection:text-black">
                        {{ response.body }}
                      </p>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>

        </div>
      </section>
    </main>

    <q-dialog v-model="threadModalActive" persistent>
      <q-card class="bg-neutral-950 border border-neutral-800 rounded-none p-6 min-w-[320px] md:min-w-[500px]">
        <q-card-section class="flex justify-between items-center pb-4 border-b border-neutral-900">
          <h3 class="text-sm font-mono font-black text-white uppercase tracking-widest">[+] Propose Policy Thread</h3>
          <q-btn flat round dense icon="close" size="sm" class="text-neutral-500 hover:text-white" v-close-popup />
        </q-card-section>

        <q-card-section class="flex flex-col gap-4 py-6">
          <q-input v-model="newThreadTitle" 
                   dark 
                   filled 
                   square 
                   borderless 
                   label="Thread Title (e.g., Evaluation of Municipal Transit Line Expansion)" 
                   bg-color="neutral-900" 
                   color="white" 
                   class="font-mono text-xs border border-neutral-800" 
                   :rules="[(val: string) => !!val || 'Field required']" />
          
          <div class="flex flex-col gap-2">
            <span class="text-[10px] font-mono font-bold text-neutral-400 uppercase tracking-widest">Select Category:</span>
            <div class="flex flex-wrap gap-2">
              <button v-for="cat in availableCategories" 
                      :key="cat" 
                      @click="newThreadCategory = cat" 
                      :class="newThreadCategory === cat ? 'bg-white text-black font-bold' : 'bg-neutral-900 text-neutral-400 border border-neutral-800'" 
                      class="px-3 py-1 font-mono text-[9px] uppercase tracking-wider transition-all">
                {{ cat }}
              </button>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="border-t border-neutral-900 pt-4">
          <q-btn flat label="Cancel" size="sm" class="font-mono text-neutral-400 uppercase tracking-wider" v-close-popup />
          <q-btn unelevated label="Propose Thread" size="sm" class="font-mono font-bold bg-white text-black hover:bg-neutral-200 uppercase tracking-wider" :loading="proposingThread" @click="handleProposeThread" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="authModalActive" persistent>
      <q-card class="bg-neutral-950 border border-neutral-800 rounded-none p-6 min-w-[320px] md:min-w-[420px]">
        <q-card-section class="flex justify-between items-center pb-4 border-b border-neutral-900">
          <h3 class="text-sm font-mono font-black text-white uppercase tracking-widest">
            {{ authModalMode === 'login' ? '[*] Sign In' : '[+] Register Account' }}
          </h3>
          <q-btn flat round dense icon="close" size="sm" class="text-neutral-500 hover:text-white" v-close-popup />
        </q-card-section>

        <q-card-section class="flex flex-col gap-4 py-6">
          <q-input v-model="authForm.username" dark filled square borderless label="Username" bg-color="neutral-900" color="white" class="font-mono text-xs border border-neutral-800" />
          <q-input v-if="authModalMode === 'register'" v-model="authForm.email" dark filled square borderless label="Email Address" bg-color="neutral-900" color="white" class="font-mono text-xs border border-neutral-800" />
          <q-input v-model="authForm.password" type="password" dark filled square borderless label="Password" bg-color="neutral-900" color="white" class="font-mono text-xs border border-neutral-800" />
          
          <div v-if="authModalMode === 'register'" class="flex flex-col gap-2 mt-2">
            <span class="text-[10px] font-mono font-bold text-neutral-400 uppercase tracking-widest">Initial Role Context:</span>
            <div class="flex gap-2">
              <button @click="authForm.role = 'user'" :class="authForm.role === 'user' ? 'bg-white text-black font-bold' : 'bg-neutral-900 text-neutral-400 border border-neutral-800'" class="flex-1 py-2 font-mono text-[10px] uppercase tracking-wider transition-all">
                Citizen
              </button>
              <button @click="authForm.role = 'contender'" :class="authForm.role === 'contender' ? 'bg-white text-black font-bold' : 'bg-neutral-900 text-neutral-400 border border-neutral-800'" class="flex-1 py-2 font-mono text-[10px] uppercase tracking-wider transition-all">
                Contender
              </button>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="border-t border-neutral-900 pt-4 flex justify-between items-center">
          <button @click="toggleAuthMode" class="text-[10px] font-mono text-neutral-400 hover:text-white uppercase tracking-widest underline">
            {{ authModalMode === 'login' ? "Register Instead" : "Sign In Instead" }}
          </button>
          <div class="flex gap-2">
            <q-btn flat label="Cancel" size="sm" class="font-mono text-neutral-400 uppercase tracking-wider" v-close-popup />
            <button @click="handleAuthSubmit" class="font-mono text-xs bg-white text-black hover:bg-neutral-200 px-4 py-2 uppercase font-bold tracking-widest">
              {{ authModalMode === 'login' ? 'Login' : 'Sign Up' }}
            </button>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
// State definitions, stores, methods, and types go here
</script>