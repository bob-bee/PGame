#!/usr/bin/env python3
import os
import sys
import subprocess

OLLAMA_MODEL = "qwen2.5-coder:7b"

def call_ollama(system_prompt: str, user_prompt: str) -> str:
    """Safely issues an invocation to the local Ollama instance."""
    full_payload = f"System Context:\n{system_prompt}\n\nTask:\n{user_prompt}"
    try:
        result = subprocess.run(
            ['ollama', 'run', OLLAMA_MODEL, full_payload],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Ollama execution crashed: {e.stderr}")
        sys.exit(1)

def clean_llm_code(raw_output: str) -> str:
    """Strips Markdown backticks and language identifiers from model outputs."""
    if "```" in raw_output:
        parts = raw_output.split("```")
        code = parts[1]
        lines = code.splitlines()
        if lines and (lines[0].strip().isalpha() or any(lang in lines[0] for lang in ['ts', 'py', 'ini', 'vue'])):
            code = "\n".join(lines[1:])
        return code.strip()
    return raw_output.strip()

def run_modification(target_path: str, agent_spec_path: str, task: str):
    """Executes a targeted file modification guarded by a local micro-agent."""
    if not os.path.exists(target_path):
        # Create empty file directory path if missing
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w') as f: 
            f.write("")
        print(f"🆕 Target file did not exist. Initializing empty slot: {target_path}")
        
    if not os.path.exists(agent_spec_path):
        print(f"❌ Target Micro-Agent rules file missing: {agent_spec_path}")
        return

    with open(target_path, 'r') as f: current_code = f.read()
    with open(agent_spec_path, 'r') as f: agent_rules = f.read()
    
    master_rules = ""
    if os.path.exists('MasterAgent.md'):
        with open('MasterAgent.md', 'r') as f: 
            master_rules = f.read()

    system_context = f"{master_rules}\n\nSPECIFIC MICRO-AGENT INVARIANTS:\n{agent_rules}"
    
    # Using single-line definition for safe parsing of user query f-string
    user_query = f"CURRENT FILE CONTENT:\n```\n{current_code}\n```\n\nINSTRUCTION: {task}"

    print(f"🤖 Processing change with micro-agent via {OLLAMA_MODEL} on: {target_path}...")
    raw_response = call_ollama(system_context, user_query)
    clean_code = clean_llm_code(raw_response)

    if not clean_code or len(clean_code.strip()) == 0:
        print(f"⚠️ Model returned empty output for {target_path}. Aborting mutation to prevent destruction.")
        return

    with open(target_path, 'w') as f:
        f.write(clean_code)
    print(f"✅ Successfully written updates to: {target_path}\n")

def run_pipeline():
    """Runs a sequential development execution pipeline using our micro-agents."""
    print("🚀 Starting Civic Threads Local Development Build Pipeline...")
    
    # Task 1: Fix backend testing path configuration
    run_modification(
        target_path="backend/pytest.ini",
        agent_spec_path="backend/ModelsAgent.md",
        task="Create a standard pytest.ini file that sets pythonpath to include '.' so running tests from root works flawlessly."
    )

    # Task 2: Build the global Axios Client
    run_modification(
        target_path="frontend/src/boot/axios.ts",
        agent_spec_path="frontend/src/boot/AxiosAgent.md",
        task="Implement the full axios initialization boot file with a localStorage check for 'civic_token' inside the authorization request header headers interceptor block."
    )

    # Task 3: Build the Pinia Authentication Engine
    run_modification(
        target_path="frontend/src/stores/auth.ts",
        agent_spec_path="frontend/src/stores/AuthAgent.md",
        task="Generate a complete Pinia composition-style auth store containing token, user, isAuthenticated, and registration/login actions matching our specifications."
    )

    print("🏁 Pipeline run completed. Run your local tests or view frontend assets to verify stability!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pipeline":
        run_pipeline()
    else:
        print("💡 Usage:")
        print("  Run entire stack build pipeline:  python3 runAgent.py pipeline")
        print("  Modify a single specific file:    Modify the __main__ script or pass interactive args.")