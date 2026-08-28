from OTXv2 import OTXv2
import os

API_KEY = os.getenv("OTX_API_KEY")
if not API_KEY:
    raise RuntimeError("Set OTX_API_KEY before running this test.")

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
