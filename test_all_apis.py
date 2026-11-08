"""Quick API validation test for all endpoints."""
import sys, os
sys.path.insert(0, 'd:/Airtel_prj')
os.chdir('d:/Airtel_prj')

from app import app
client = app.test_client()

PASS = "[PASS]"
FAIL = "[FAIL]"

def test(name, response, check_key=None, check_val=None):
    ok = response.status_code == 200
    data = None
    if ok:
        try:
            data = response.get_json()
            if check_key and data:
                if isinstance(data, list):
                    # Check first item
                    ok = check_key in (data[0] if data else {})
                else:
                    ok = check_key in data
        except Exception as e:
            ok = False
    icon = PASS if ok else FAIL
    status = f"HTTP {response.status_code}"
    extra = ""
    if data and isinstance(data, dict):
        extra = str(list(data.keys())[:6])
    elif data and isinstance(data, list):
        extra = f"[{len(data)} items, keys: {list(data[0].keys())[:5] if data else []}]"
    print(f"  {icon} {name:40s} {status}  {extra}")
    return ok

print("\n=== Airtel Project Udyam Digital — API Tests ===\n")

# Pages
test("GET /", client.get('/'), None)
test("GET /advisor", client.get('/advisor'), None)
test("GET /quote", client.get('/quote'), None)
test("GET /kyc", client.get('/kyc'), None)
test("GET /tracker", client.get('/tracker'), None)
test("GET /crm", client.get('/crm'), None)
test("GET /deliverables", client.get('/deliverables'), None)

print()
# API endpoints
import json

r = client.get('/api/products')
test("GET /api/products", r, "product_code")

r = client.post('/api/advisor/recommend', json={"business_type":"kirana","segment":"micro","language":"en","has_gstin":"Y"})
test("POST /api/advisor/recommend", r, "bundle_title")

r = client.post('/api/advisor/chat', json={"message":"I have a kirana shop","context":{"language":"en"}})
test("POST /api/advisor/chat", r, "response")

r = client.post('/api/advisor/chat', json={"message":"मेरी दुकान है","context":{"language":"hi"}})
test("POST /api/advisor/chat (Hindi)", r, "response")

r = client.get('/api/kyc/specimens')
test("GET /api/kyc/specimens", r, "code")

r = client.post('/api/kyc/verify-specimen', json={"applicant_code":"K03"})
test("POST /api/kyc/verify-specimen K03", r, "overall_result")
if r.status_code == 200:
    d = r.get_json()
    verdict = d.get("overall_result", "?")
    print(f"      K03 verdict: {verdict} (expected APPROVED)")

r = client.post('/api/kyc/verify-specimen', json={"applicant_code":"K12"})
test("POST /api/kyc/verify-specimen K12", r, "overall_result")
if r.status_code == 200:
    d = r.get_json()
    verdict = d.get("overall_result", "?")
    print(f"      K12 verdict: {verdict} (expected APPROVED)")

r = client.post('/api/kyc/verify-specimen', json={"applicant_code":"K01"})
if r.status_code == 200:
    d = r.get_json()
    verdict = d.get("overall_result", "?")
    print(f"  {'[PASS]' if verdict=='REJECTED' else '[FAIL]'} K01 verdict: {verdict} (expected REJECTED)")

r = client.post('/api/kyc/verify-specimen', json={"applicant_code":"K10"})
if r.status_code == 200:
    d = r.get_json()
    verdict = d.get("overall_result", "?")
    print(f"  {'[PASS]' if verdict=='REJECTED' else '[FAIL]'} K10 verdict: {verdict} (expected REJECTED)")

r = client.post('/api/kyc/lookup-gstin', json={"gstin":"27AAJCG3029F1ZK"})
test("POST /api/kyc/lookup-gstin", r, "found")

r = client.get('/api/crm/funnel')
test("GET /api/crm/funnel", r, "total_leads")
if r.status_code == 200:
    d = r.get_json()
    print(f"      Funnel keys: {list(d.keys())}")

r = client.get('/api/crm/leads?limit=10')
test("GET /api/crm/leads", r, "stage")

r = client.post('/api/orders/create', json={"business_name":"Test Biz","city":"Mumbai","contact_phone":"9876543210","bundle_title":"Test Bundle","total_monthly_with_gst":2500})
test("POST /api/orders/create", r, "order_id")

print("\n=== Done ===\n")
