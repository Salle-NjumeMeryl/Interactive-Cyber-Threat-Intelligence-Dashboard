from OTXv2 import OTXv2

API_KEY = "24950467d6064440832ba21636eed55fd2627fd8f0fb73667c40b64f0c9e0ee0"

otx = OTXv2(API_KEY)

# Fetch the latest threat pulses
pulses = otx.getall(max_items=5)

print(f"✅ Connection successful! Found {len(pulses)} threat pulses.\n")

for pulse in pulses:
    print("-----------------------------------")
    print(f"Title     : {pulse['name']}")
    print(f"Author    : {pulse['author_name']}")
    print(f"Created   : {pulse['created']}")
    print(f"Tags      : {pulse.get('tags', [])}")
