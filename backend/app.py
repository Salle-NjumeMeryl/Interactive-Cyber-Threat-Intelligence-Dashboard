from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from OTXv2 import OTXv2
import requests
from data_cleaner import clean_threats, load_csv_fallback

app = Flask(__name__)
CORS(app)

# ── Your OTX API Key ──────────────────────────────────
OTX_API_KEY = "19065656d4104dd6a35726ccec94bfcbb0c8effbd54e2eb2dec0116df8946fb1"
otx = OTXv2(OTX_API_KEY)

# ── Your 6 defined attack types ───────────────────────
ATTACK_TYPES = [
    "Phishing",
    "Ransomware",
    "DDoS",
    "Malware",
    "Brute Force",
    "SQL Injection"
]

# ── Attack classifier ─────────────────────────────────
def classify_attack(tags):
    tags_lower = [t.lower() for t in tags]
    if any(t in tags_lower for t in ['phishing', 'spear-phishing', 'bec', 'spearphishing']):
        return 'Phishing'
    elif any(t in tags_lower for t in ['ransomware', 'lockbit', 'blackcat', 'ryuk', 'conti']):
        return 'Ransomware'
    elif any(t in tags_lower for t in ['ddos', 'dos', 'flood', 'amplification']):
        return 'DDoS'
    elif any(t in tags_lower for t in ['malware', 'trojan', 'botnet', 'worm', 'spyware', 'emotet', 'rat']):
        return 'Malware'
    elif any(t in tags_lower for t in ['brute-force', 'bruteforce', 'credential', 'password-spray']):
        return 'Brute Force'
    elif any(t in tags_lower for t in ['sqli', 'sql-injection', 'injection', 'sqlinjection']):
        return 'SQL Injection'
    else:
        return 'Other'

# ── Fetch and parse OTX pulses ────────────────────────

def fetch_otx_threats(max_items=5):
    try:
        pulses = otx.getall(max_items=max_items)
        threats = []
        for pulse in pulses:
            tags = pulse.get('tags', [])
            threat = {
                "title":       pulse.get('name', 'Unknown Threat'),
                "author":      pulse.get('author_name', 'Unknown'),
                "attack_type": classify_attack(tags),
                "tags":        tags,
                "ioc_count":   len(pulse.get('indicators', [])),
                "country":     (pulse.get('targeted_countries') or ['Unknown'])[0],
                "timestamp":   pulse.get('created', ''),
                "description": pulse.get('description', '')[:200],
                "severity":    "High" if len(pulse.get('indicators', [])) > 20 else "Medium" if len(pulse.get('indicators', [])) > 5 else "Low"
            }
            threats.append(threat)

        # ── Clean the live data ───────────────────────
        threats = clean_threats(threats)

        # ── Fallback to CSV if OTX returns nothing ────
        if not threats:
            print("⚠️ OTX returned no data — loading CSV fallback")
            threats = load_csv_fallback()

        return threats, None

    except Exception as e:
        # ── On any error load CSV fallback ────────────
        print(f"⚠️ OTX API error: {e} — loading CSV fallback")
        return load_csv_fallback(), None

#def fetch_otx_threats(max_items=5):
    #try:
        #pulses = otx.getall(max_items=max_items)
        #threats = []

        #for pulse in pulses:
            #tags = pulse.get('tags', [])
            #attack_type = classify_attack(tags)

            # Extract country tags
            #country_tags = pulse.get('targeted_countries', [])
            #country = country_tags[0] if country_tags else 'Unknown'

            # Extract IOC count
            #ioc_count = len(pulse.get('indicators', []))

            # Build structured threat object
            #threat = {
                #"title":        pulse.get('name', 'Unknown Threat'),
                #"author":       pulse.get('author_name', 'Unknown'),
                #"attack_type":  attack_type,
                #"tags":         tags,
                #"ioc_count":    ioc_count,
                #"country":      country,
                #"timestamp":    pulse.get('created', ''),
                #"description":  pulse.get('description', '')[:200],
                #"severity":     "High" if ioc_count > 20 else "Medium" if ioc_count > 5 else "Low"
            #}
            #threats.append(threat)

        #return threats, None

    #except Exception as e:
        #return [], str(e)

# ── Health check ──────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "message": "CTI Dashboard backend is running",
        "timestamp": datetime.now().isoformat(),
        "attack_types_tracked": ATTACK_TYPES
    })

# ── All threats ───────────────────────────────────────
@app.route('/api/threats', methods=['GET'])
def get_threats():
    threats, error = fetch_otx_threats(max_items=50)

    if error:
        return jsonify({"status": "error", "message": error}), 500

    return jsonify({
        "status": "ok",
        "count": len(threats),
        "data": threats
    })

# ── Threats grouped by your 6 attack types ────────────
@app.route('/api/threats/by-type', methods=['GET'])
def get_by_type():
    threats, error = fetch_otx_threats(max_items=50)

    if error:
        return jsonify({"status": "error", "message": error}), 500

    # Count threats per attack type
    by_type = {attack: 0 for attack in ATTACK_TYPES}
    by_type['Other'] = 0
    for threat in threats:
        attack = threat['attack_type']
        if attack in by_type:
            by_type[attack] += 1
        else:
            by_type['Other'] += 1

    return jsonify({"status": "ok", "data": by_type})

# ── Threats grouped by country ────────────────────────
@app.route('/api/threats/by-country', methods=['GET'])
def get_by_country():
    threats, error = fetch_otx_threats(max_items=5)

    if error:
        return jsonify({"status": "error", "message": error}), 500

    by_country = {}
    for threat in threats:
        country = threat['country']
        if country and country != 'Unknown':
            by_country[country] = by_country.get(country, 0) + 1

    # Sort by count descending
    sorted_countries = dict(sorted(by_country.items(), key=lambda x: x[1], reverse=True))

    return jsonify({"status": "ok", "data": sorted_countries})

# ── Threat timeline (last 30 days) ────────────────────
@app.route('/api/threats/timeline', methods=['GET'])
def get_timeline():
    threats, error = fetch_otx_threats(max_items=100)

    if error:
        return jsonify({"status": "error", "message": error}), 500

    timeline = {}
    for threat in threats:
        timestamp = threat['timestamp']
        if timestamp:
            date = timestamp[:10]  # Extract YYYY-MM-DD
            timeline[date] = timeline.get(date, 0) + 1

    # Sort by date
    sorted_timeline = dict(sorted(timeline.items()))

    return jsonify({"status": "ok", "data": sorted_timeline})

# ── Run server ────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)