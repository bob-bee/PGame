# backend/test_lifecycle.py
import sys
import time
import requests

BASE_URL = "http://localhost:8000"

def run_integration_test():
    print("🚀 Starting Political Threads API Integration Test...\n")
    
    # Unique suffixes to avoid DB collision failures on rerun
    timestamp = int(time.time())
    citizen_username = f"citizen_{timestamp}"
    contender_username = f"contender_{timestamp}"
    
    # ----------------------------------------------------
    # 1. REGISTER USER ACCOUNTS
    # ----------------------------------------------------
    print("🔹 Step 1: Registering Citizen and Contender accounts...")
    
    citizen_payload = {
        "username": citizen_username,
        "email": f"{citizen_username}@example.com",
        "password": "securepassword123"
    }
    res = requests.post(f"{BASE_URL}/auth/register", json=citizen_payload)
    assert res.status_code == 201, f"Citizen registration failed: {res.text}"
    print(" ✅ Citizen registered.")

    contender_payload = {
        "username": contender_username,
        "email": f"{contender_username}@example.com",
        "password": "contenderpassword123"
    }
    res = requests.post(f"{BASE_URL}/auth/register", json=contender_payload)
    assert res.status_code == 201, f"Contender registration failed: {res.text}"
    print(" ✅ Contender base user registered.")

    # ----------------------------------------------------
    # 2. AUTHENTICATE AND OBTAIN TOKENS
    # ----------------------------------------------------
    print("\n🔹 Step 2: Authenticating and acquiring OAuth2 tokens...")
    
    # Standard OAuth2 form submission structure
    citizen_login = {"username": citizen_username, "password": "securepassword123"}
    res = requests.post(f"{BASE_URL}/auth/login", data=citizen_login)
    assert res.status_code == 200, "Citizen login failed"
    citizen_token = res.json()["access_token"]
    citizen_headers = {"Authorization": f"Bearer {citizen_token}"}
    print(" ✅ Citizen token acquired.")

    contender_login = {"username": contender_username, "password": "contenderpassword123"}
    res = requests.post(f"{BASE_URL}/auth/login", data=contender_login)
    assert res.status_code == 200, "Contender login failed"
    contender_token = res.json()["access_token"]
    contender_headers = {"Authorization": f"Bearer {contender_token}"}
    print(" ✅ Contender token acquired.")

    # ----------------------------------------------------
    # 3. MANUALLY SIMULATE ELEVATION TO CONTENDER
    # ----------------------------------------------------
    # Note: Since the core engine relies on a database state change for the demo 
    # role guard, we will demonstrate the role restriction failing, then passing.
    print("\n🔹 Step 3: Verifying Role Security Controls...")
    
    thread_data = {"title": "Decentralized Public Transit Budgets", "category": "Infrastructure"}
    res = requests.post(f"{BASE_URL}/threads", json=thread_data, headers=citizen_headers)
    assert res.status_code == 201, "Thread creation failed"
    thread_id = res.json()["id"]
    print(f" ✅ Citizen created public Thread ID: {thread_id}")

    # Try to post an official statement using standard user account -> Should Fail (403)
    bad_statement_payload = {"thread_id": thread_id, "body": "Unauthorized statement attempt."}
    res = requests.post(f"{BASE_URL}/threads/{thread_id}/statements", json=bad_statement_payload, headers=citizen_headers)
    assert res.status_code == 403, f"Security Guard Failure: Allowed standard user to act as contender: {res.status_code}"
    print(" ✅ Guard Blocked Standard Citizen from posting official Contender statements.")

    print("\n⚠️  [Manual Step Notice] In live operations, a /contenders/apply workflow handles elevation.")
    print("    To continue testing the backend router pipeline directly, update your database manually:")
    print(f"    UPDATE \"user\" SET role = 'contender' WHERE username = '{contender_username}';")
    print("\n    Let's run a soft check. Did you update the test database role flag? (y/n): ")
    
    # If automating inside a headless setup, you can query database engines directly.
    # For now, we wrap the subsequent validation pipeline so it can be verified gracefully.
    user_input = input().strip().lower()
    if user_input != 'y':
        print("Skipping Contender validation pipelines. Test complete up to authorization boundaries.")
        return

    # ----------------------------------------------------
    # 4. CONTENDER DISCOURSE LIFECYCLE
    # ----------------------------------------------------
    print("\n🔹 Step 4: Validating Contender Statement Submission...")
    statement_payload = {"thread_id": thread_id, "body": "Official Policy: Transit lines require localized sub-budgets."}
    res = requests.post(f"{BASE_URL}/threads/{thread_id}/statements", json=statement_payload, headers=contender_headers)
    if res.status_code == 403:
        print(" ❌ Failed: Update the DB role record first before testing contender execution lines.")
        sys.exit(1)
    assert res.status_code == 201, f"Statement placement error: {res.text}"
    statement_id = res.json()["id"]
    print(f" ✅ Verified Contender published Statement ID: {statement_id}")

    # ----------------------------------------------------
    # 5. CITIZEN STRUCTURED FEEDBACK & REACTION TOGGLES
    # ----------------------------------------------------
    print("\n🔹 Step 5: Testing Citizen Structured Responses & Reactions...")
    
    # Submit explicit counterargument
    response_payload = {
        "statement_id": statement_id,
        "type": "counterargument",
        "body": "Feeder line networks running without centralized synchronization lose efficiency."
    }
    res = requests.post(f"{BASE_URL}/responses", json=response_payload, headers=citizen_headers)
    assert res.status_code == 201, "Response structure failed"
    print(" ✅ Citizen attached structured Counterargument to statement.")

    # Record reaction (Vote: Agree)
    reaction_payload = {"statement_id": statement_id, "reaction": "agree"}
    res = requests.post(f"{BASE_URL}/reactions", json=reaction_payload, headers=citizen_headers)
    assert res.status_code == 200 and res.json()["message"] == "Reaction recorded", "Reaction logging issue"
    print(" ✅ Citizen registered 'agree' vote.")

    # Toggle reaction off
    res = requests.post(f"{BASE_URL}/reactions", json=reaction_payload, headers=citizen_headers)
    assert res.status_code == 200 and res.json()["message"] == "Reaction removed", "Reaction retraction issue"
    print(" ✅ Citizen retracted vote natively (Toggle logic verified).")

    # ----------------------------------------------------
    # 6. VERIFY DYNAMIC JOIN PAYLOAD
    # ----------------------------------------------------
    print("\n🔹 Step 6: Verifying consolidated Thread Detail view contract...")
    res = requests.get(f"{BASE_URL}/threads/{thread_id}")
    assert res.status_code == 200, "Failed to retrieve public aggregate tracking views"
    data = res.json()
    assert len(data["statements"]) >= 1, "Statements payload failed to resolve joins cleanly"
    print(" ✅ Aggregate payload verified. All relational structures loaded smoothly.")
    
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Core CRUD and authorization lines are operational.")

if __name__ == "__main__":
    run_integration_test()