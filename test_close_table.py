import requests
import json
import sys

base = "http://comanda-pitim.187.77.41.37.sslip.io"

try:
    print("Testing 'Fechar Mesa' functionality...")
    prods = requests.get(f"{base}/api/products").json()["products"]
    p1 = prods[0]
    p2 = prods[1] if len(prods) > 1 else prods[0]

    table = "Mesa 18"
    print(f"\n1. Placing order 1 on {table} for 'João Silva'...")
    requests.post(f"{base}/api/orders", json={
        "table_number": table,
        "customer_name": "João Silva",
        "items": [{"product_id": p1["id"], "quantity": 1, "notes": ""}]
    }).raise_for_status()

    print(f"2. Placing order 2 on {table} for 'Mariana Costa'...")
    requests.post(f"{base}/api/orders", json={
        "table_number": table,
        "customer_name": "Mariana Costa",
        "items": [{"product_id": p2["id"], "quantity": 2, "notes": ""}]
    }).raise_for_status()

    print("\n3. Testing Admin Login...")
    login = requests.post(f"{base}/api/auth/login", json={"username": "admin", "password": "admin123"}).json()
    token = login["token"]
    headers = {"Authorization": f"Bearer {token}"}

    print(f"4. Checking active tables for {table}...")
    tables = requests.get(f"{base}/api/admin/active-tables", headers=headers).json()["tables"]
    t18 = next((t for t in tables if t["table_number"] == table), None)
    assert t18 is not None, f"{table} not found in active tables"
    print(f"   Found {table} with {len(t18['comandas'])} comandas, total R$ {t18['table_total']:.2f}")

    print(f"\n5. Requesting 'Fechar Mesa' for {table} via /api/comanda/fechar-mesa...")
    req_res = requests.post(f"{base}/api/comanda/fechar-mesa", json={
        "table_number": table,
        "requester_name": "João Silva"
    }).json()
    print("   Request response:", req_res["message"])

    tables_after = requests.get(f"{base}/api/admin/active-tables", headers=headers).json()["tables"]
    t18_after = next((t for t in tables_after if t["table_number"] == table), None)
    assert t18_after["has_closing_request"] == True, "has_closing_request should be True"
    print("   [OK] Table marked with has_closing_request = True")

    print(f"\n6. Executing Admin Close Table via /api/admin/table/{table}/close...")
    close_res = requests.post(f"{base}/api/admin/table/{table}/close", json={
        "payment_method": "Cartão de Crédito"
    }, headers=headers).json()
    print("   Admin close response:", close_res["message"])
    assert close_res["success"] == True

    print("\n7. Verifying table is settled and removed from active tables...")
    tables_final = requests.get(f"{base}/api/admin/active-tables", headers=headers).json()["tables"]
    t18_final = next((t for t in tables_final if t["table_number"] == table), None)
    assert t18_final is None, f"{table} should no longer be active"
    print(f"   [OK] {table} is no longer in active tables!")

    print("\n>>> ALL 'FECHAR MESA' TESTS PASSED WITH 100% SUCCESS! <<<")

except Exception as e:
    print(f"\n[FAIL] ERROR: {e}")
    sys.exit(1)
