#!/usr/bin/env python3
import os, json, logging, ollama, asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
# Adjust concurrency based on available VRAM/GPU cores
CONCURRENT_AGENTS = 3 
semaphore = asyncio.Semaphore(CONCURRENT_AGENTS)

logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'agent_activity.log'),
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

async def run_async_inference(prompt):
    """Executes inference concurrently using the async ollama client."""
    async with semaphore:
        print(f"🚀 Launching parallel agent...")
        # Direct async call to Ollama
        client = ollama.AsyncClient()
        response = await client.chat(model='qwen2.5-coder:7b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']

async def ProcessTask(Task):
    Target = os.path.join(BASE_DIR, Task['target_path'])
    SpecPath = os.path.join(BASE_DIR, 'agents', Task['id'] + ".md") # Auto-map ID to file
    
    with open(SpecPath, 'r') as f: spec = f.read()
    current_code = ""
    if os.path.exists(Target):
        with open(Target, 'r') as f: current_code = f.read()

    prompt = f"SPEC:\n{spec}\nCURRENT CODE:\n{current_code}\nTASK: {Task['description']}"
    
    code = await run_async_inference(prompt)
    
    os.makedirs(os.path.dirname(Target), exist_ok=True)
    with open(Target, 'w') as f: f.write(code.strip())
    print(f"✅ Completed: {Task['id']}")

async def main():
    roadmap_path = os.path.join(BASE_DIR, 'roadmap.json')
    with open(roadmap_path, 'r') as f: Roadmap = json.load(f)
    
    # Gather all pending tasks and run them concurrently
    tasks = [ProcessTask(t) for t in Roadmap['tasks'] if t['status'] == 'pending']
    await asyncio.gather(*tasks)
    
    # Mark as done
    for t in Roadmap['tasks']: t['status'] = 'done'
    with open(roadmap_path, 'w') as f: json.dump(Roadmap, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())