import os

def load_vulnerabilities():
    file_path = os.path.join(os.path.dirname(__file__), "data", "vuln_list.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        vulnerabilities = [line.strip() for line in f if line.strip()]
    return [(v, v) for v in vulnerabilities]
