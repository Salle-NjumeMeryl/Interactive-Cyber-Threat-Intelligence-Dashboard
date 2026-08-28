# def classify_attack(pulse_tags):
#     tags = [t.lower() for t in pulse_tags]
#     if any(t in tags for t in ['phishing', 'spear-phishing', 'bec']):
#         return 'Phishing'
#     elif any(t in tags for t in ['ransomware', 'lockbit', 'blackcat']):
#         return 'Ransomware'
#     elif any(t in tags for t in ['ddos', 'dos', 'flood']):
#         return 'DDoS'
#     elif any(t in tags for t in ['malware', 'trojan', 'botnet', 'worm']):
#         return 'Malware'
#     elif any(t in tags for t in ['brute-force', 'bruteforce', 'credential']):
#         return 'Brute Force'
#     elif any(t in tags for t in ['sqli', 'sql-injection', 'injection']):
#         return 'SQL Injection'
#     else:
#         return 'Other'