# import csv
# from datetime import datetime
# from pathlib import Path

# # ── Country name normalization map ────────────────────
# COUNTRY_NAMES = {
#     "US": "United States",
#     "USA": "United States",
#     "United States of America": "United States",
#     "UK": "United Kingdom",
#     "GB": "United Kingdom",
#     "Great Britain": "United Kingdom",
#     "RU": "Russia",
#     "Russian Federation": "Russia",
#     "CN": "China",
#     "People's Republic of China": "China",
#     "NG": "Nigeria",
#     "CM": "Cameroon",
#     "DE": "Germany",
#     "FR": "France",
#     "BR": "Brazil",
#     "IN": "India",
#     "KP": "North Korea",
#     "IR": "Iran",
#     "UA": "Ukraine",
#     "ZA": "South Africa",
# }

# # ── Your 6 attack types ───────────────────────────────
# ATTACK_TYPES = [
#     "Phishing",
#     "Ransomware",
#     "DDoS",
#     "Malware",
#     "Brute Force",
#     "SQL Injection"
# ]

# # ── Normalize country name ────────────────────────────
# def normalize_country(country):
#     if not country or country.strip() == "":
#         return "Unknown"
#     return COUNTRY_NAMES.get(country.strip(), country.strip())

# # ── Normalize attack type ─────────────────────────────
# def normalize_attack_type(attack_type):
#     if not attack_type or attack_type.strip() == "":
#         return "Unknown"
#     for valid_type in ATTACK_TYPES:
#         if valid_type.lower() == attack_type.strip().lower():
#             return valid_type
#     return "Other"

# # ── Normalize timestamp ───────────────────────────────
# def normalize_timestamp(timestamp):
#     if not timestamp or timestamp.strip() == "":
#         return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#     # Try common formats
#     formats = [
#         "%Y-%m-%dT%H:%M:%S.%f",
#         "%Y-%m-%dT%H:%M:%S",
#         "%Y-%m-%d %H:%M:%S",
#         "%Y-%m-%d",
#         "%d/%m/%Y",
#         "%m/%d/%Y"
#     ]
#     for fmt in formats:
#         try:
#             return datetime.strptime(timestamp.strip(), fmt).strftime("%Y-%m-%dT%H:%M:%S")
#         except ValueError:
#             continue
#     return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# # ── Clean a single threat record ──────────────────────
# def clean_threat(threat):
#     return {
#         "title":        threat.get("title", "Unknown Threat").strip() or "Unknown Threat",
#         "author":       threat.get("author", "Unknown").strip() or "Unknown",
#         "attack_type":  normalize_attack_type(threat.get("attack_type", "")),
#         "country":      normalize_country(threat.get("country", "")),
#         "ioc_count":    int(threat.get("ioc_count", 0)),
#         "timestamp":    normalize_timestamp(threat.get("timestamp", "")),
#         "description":  threat.get("description", "")[:200].strip(),
#         "severity":     threat.get("severity", "Low").strip() or "Low",
#         "tags":         threat.get("tags", [])
#     }

# # ── Clean a list of threats ───────────────────────────
# def clean_threats(threats):
#     cleaned = []
#     for threat in threats:
#         try:
#             cleaned.append(clean_threat(threat))
#         except Exception as e:
#             print(f"Skipping malformed record: {e}")
#             continue
#     return cleaned

# # ── Load CSV fallback data ────────────────────────────
# def load_csv_fallback(filepath=None):
#     threats = []
#     if filepath is None:
#         filepath = Path(__file__).resolve().parent.parent / 'data' / 'mitre_techniques.csv'
#     try:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 # Map MITRE CSV columns to your threat structure
#                 tactic = row.get('Tactic', '')
#                 attack_type = map_tactic_to_attack_type(tactic)
#                 threat = {
#                     "title":       row.get('Name', 'Unknown'),
#                     "author":      "MITRE ATT&CK",
#                     "attack_type": attack_type,
#                     "country":     "Unknown",
#                     "ioc_count":   0,
#                     "timestamp":   datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                     "description": row.get('Description', '')[:200],
#                     "severity":    "Medium",
#                     "tags":        [tactic]
#                 }
#                 threats.append(clean_threat(threat))
#         print(f"CSV fallback loaded: {len(threats)} records")
#     except FileNotFoundError:
#         print(f"CSV file not found at {filepath}")
#     except Exception as e:
#         print(f"Error loading CSV: {e}")
#     return threats

# # ── Map MITRE tactic to your 6 attack types ───────────
# def map_tactic_to_attack_type(tactic):
#     tactic_lower = tactic.lower()
#     if 'initial-access' in tactic_lower or 'phish' in tactic_lower:
#         return 'Phishing'
#     elif 'impact' in tactic_lower:
#         return 'Ransomware'
#     elif 'credential' in tactic_lower:
#         return 'Brute Force'
#     elif 'execution' in tactic_lower or 'persistence' in tactic_lower:
#         return 'Malware'
#     elif 'exfiltration' in tactic_lower or 'collection' in tactic_lower:
#         return 'SQL Injection'
#     else:
#         return 'Other'

# # ── Test the cleaner ──────────────────────────────────
# if __name__ == '__main__':
#     # Test with sample dirty data
#     sample_dirty_data = [
#         {
#             "title": "  Phishing Campaign  ",
#             "author": "",
#             "attack_type": "phishing",
#             "country": "US",
#             "ioc_count": "25",
#             "timestamp": "2026-08-01T10:00:00",
#             "description": "A phishing campaign targeting banks",
#             "severity": "",
#             "tags": ["phishing", "banking"]
#         },
#         {
#             "title": "",
#             "author": "AlienVault",
#             "attack_type": "",
#             "country": "Russian Federation",
#             "ioc_count": "3",
#             "timestamp": "01/08/2026",
#             "description": "",
#             "severity": "high",
#             "tags": []
#         },
#         {
#             "title": "LockBit Ransomware",
#             "author": "Researcher",
#             "attack_type": "ransomware",
#             "country": "CN",
#             "ioc_count": "50",
#             "timestamp": "",
#             "description": "LockBit 3.0 spreading via phishing emails",
#             "severity": "High",
#             "tags": ["ransomware", "lockbit"]
#         }
#     ]

#     print("=== BEFORE CLEANING ===")
#     for d in sample_dirty_data:
#         print(d)

#     print("\n=== AFTER CLEANING ===")
#     cleaned = clean_threats(sample_dirty_data)
#     for c in cleaned:
#         print(c)

#     print(f"\n✅ Cleaned {len(cleaned)} records successfully")

#     # Test CSV fallback loader
#     print("\n=== TESTING CSV FALLBACK ===")
#     csv_data = load_csv_fallback()
#     if csv_data:
#         print(f"✅ First CSV record: {csv_data[0]}")
#     else:
#         print("⚠️ No CSV data loaded — check that mitre_techniques.csv exists in data/")