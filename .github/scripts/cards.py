#!/usr/bin/env python3
"""Build the profile cards (dark + light) into cards/.

Edit the DATA section below, then run:  python3 .github/scripts/cards.py
Every fact here mirrors the resume - keep them in sync.
"""
import math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES, SANS, MONO, WIDTH, esc, check_fits, frame, header  # noqa: E402

OUT = os.environ.get("CARDS_DIR", "cards")

# ============================== DATA ==============================
NAME = "Abdul Rehman"
TITLE = "Senior DevOps / DevSecOps / Cloud Engineer"
TAGLINE = "I build, secure and run production Kubernetes platforms on AWS, Azure and GCP."
PILLS = ["Kubernetes", "Terraform", "GitOps", "DevSecOps", "Multi-Cloud", "AI/GPU + Web3 infra"]
STATUS = "Open to full-time & freelance"
LOCATION = "Islamabad, Pakistan · UTC+5"

IMPACT = [  # (big number, label line 1, label line 2)
    ("4+", "years in production", "DevOps & DevSecOps"),
    ("3", "clouds in production", "AWS · Azure · GCP"),
    ("30+", "microservices run", "on Kubernetes"),
    ("~50%", "compute cost cut", "Karpenter + Spot"),
    ("<4 min", "deploy time", "down from 15 min"),
]

ROLES = [  # company, title, dates, location, bullets
    ("Funavry Technologies", "Senior DevOps / DevSecOps Engineer", "01/2026 — Present", "Islamabad", [
        "3–5 production clusters on EKS, AKS & GKE · Terraform + GitOps (ArgoCD / FluxCD) across all three clouds",
        "KEDA + Karpenter on Spot cut compute cost ~50% · DevSecOps gates · multi-node blockchain RPC · incident RCA",
    ]),
    ("IKONIC", "DevOps Engineer", "03/2025 — 01/2026", "Islamabad", [
        "AWS EKS + Google GKE + DigitalOcean workloads · GPU-enabled Python/React AI apps in production",
        "GitHub Actions dev → staging → prod · Docker multi-stage builds to ECR / Artifact Registry with scanning",
    ]),
    ("Forbmax", "DevOps / DevSecOps Engineer", "08/2023 — 03/2025", "Islamabad", [
        "3–4 clusters across cloud + an on-prem data center running a 30+ microservice media-streaming platform",
        "ArgoCD GitOps · Jenkins gated by SonarQube, Dependency-Check & Trivy · Helm · Prometheus / Grafana",
    ]),
    ("Onyx Tech", "Linux System Administrator", "10/2022 — 08/2023", "Lahore", [
        "Enterprise RHEL 7/8: patching, LVM / RAID, Apache / DNS / NFS, monitoring, backup and recovery",
        "SELinux + iptables hardening",
    ]),
]

TOOLBOX = [
    ("cloud", ["AWS", "Azure", "GCP", "DigitalOcean", "Hetzner", "On-Prem"]),
    ("kubernetes", ["EKS", "AKS", "GKE", "Helm", "Karpenter", "KEDA", "Istio", "Kiali", "Ingress-NGINX", "Traefik"]),
    ("gitops-ci", ["ArgoCD", "FluxCD", "GitHub Actions", "GitLab CI", "Jenkins", "Azure DevOps"]),
    ("iac", ["Terraform", "Ansible", "CloudFormation"]),
    ("devsecops", ["Semgrep", "SonarQube", "OWASP ZAP", "Trivy", "Gitleaks", "Checkov", "Dependency-Check", "Burp Suite"]),
    ("security", ["IAM / RBAC", "mTLS", "Network Policies", "KMS", "Cloudflare WAF", "SELinux"]),
    ("observability", ["Prometheus", "Grafana", "ELK", "CloudWatch", "Uptime Kuma", "k6"]),
    ("data", ["PostgreSQL", "Redis", "Elasticsearch", "Kafka"]),
    ("languages", ["Go", "Python", "Bash", "HCL", "SQL"]),
]
# ==================================================================


def chip(t, x, y, label, color, size=13, h=30):
    w = len(label) * size * 0.62 + 24
    return w, (f'    <rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["panel"]}" stroke="{color}" stroke-opacity="0.55"/>\n'
               f'    <text x="{x + w / 2:.0f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["text"]}">{esc(label)}</text>\n')


def hero(t):
    H = 330
    b = [header(t, 48, 38, "whoami")]
    check_fits(NAME, 56, 780, bold=True, where="hero name")
    check_fits(TITLE, 24, 780, bold=True, where="hero title")
    check_fits(TAGLINE, 17, 780, where="hero tagline")
    b.append(f'    <text x="48" y="122" font-family="{SANS}" font-size="56" font-weight="700" fill="{t["text"]}">{esc(NAME)}</text>')
    b.append(f'    <text x="48" y="164" font-family="{SANS}" font-size="24" font-weight="600" fill="url(#accent)">{esc(TITLE)}</text>')
    b.append(f'    <text x="48" y="202" font-family="{SANS}" font-size="17" fill="{t["muted"]}">{esc(TAGLINE)}</text>')
    x = 48
    colors = [t["a1"], t["a2"], t["a3"], t["a4"]]
    for i, p in enumerate(PILLS):
        w, s = chip(t, x, 226, p, colors[i % 4])
        b.append(s.rstrip("\n"))
        x += w + 10
    if x > 840:
        raise SystemExit(f"hero pills too wide: {x}")
    # status line with a gently pulsing dot
    b.append(f'''    <circle cx="56" cy="294" r="6" fill="{t["a3"]}"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
    <text x="72" y="299" font-family="{MONO}" font-size="14" fill="{t["text"]}">{esc(STATUS)}<tspan fill="{t["muted"]}">   ·   {esc(LOCATION)}</tspan></text>''')

    # right side: a cluster diagram (control plane + clouds), traffic flowing on the links
    cx, cy, r = 1010, 178, 112
    nodes = ["AWS", "Azure", "GCP", "on-prem", "GPU", "edge"]
    g = [f'    <circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="none" stroke="{t["border"]}" stroke-dasharray="2 6"/>']
    for i, n in enumerate(nodes):
        a = -math.pi / 2 + i * 2 * math.pi / len(nodes)
        nx, ny = cx + r * math.cos(a), cy + r * math.sin(a)
        col = t["a1"] if i % 2 == 0 else t["a2"]
        g.append(f'    <line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{col}" stroke-opacity="0.6" stroke-width="1.5" stroke-dasharray="4 6">'
                 f'<animate attributeName="stroke-dashoffset" values="20;0" dur="{1.2 + i * 0.15:.2f}s" repeatCount="indefinite"/></line>')
        g.append(f'    <circle cx="{nx:.1f}" cy="{ny:.1f}" r="27" fill="{t["panel"]}" stroke="{col}" stroke-width="1.5"/>')
        g.append(f'    <text x="{nx:.1f}" y="{ny + 4:.1f}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["text"]}">{esc(n)}</text>')
    g.append(f'    <circle cx="{cx}" cy="{cy}" r="40" fill="{t["bg"]}" stroke="url(#accent)" stroke-width="2.5"/>')
    g.append(f'    <text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{t["text"]}">k8s</text>')
    g.append(f'    <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["muted"]}">gitops</text>')
    b += g
    return frame(t, H, "\n".join(b), f"{NAME} — {TITLE}. {TAGLINE}")


def impact(t):
    H = 196
    b = [header(t, 48, 38, "cat impact.txt")]
    n = len(IMPACT); gap = 14; x0 = 32
    w = (WIDTH - 2 * x0 - gap * (n - 1)) / n
    cols = [t["a1"], t["a2"], t["a3"], t["a4"], t["a1"]]
    for i, (num, l1, l2) in enumerate(IMPACT):
        x = x0 + i * (w + gap); y = 60
        for s, size, bold in ((num, 36, True), (l1, 14, False), (l2, 13, False)):
            check_fits(s, size, w - 24, bold=bold, where="impact")
        b.append(f'    <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="112" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        b.append(f'    <rect x="{x:.0f}" y="{y}" width="4" height="112" rx="2" fill="{cols[i]}"/>')
        b.append(f'    <text x="{x + 22:.0f}" y="{y + 48}" font-family="{SANS}" font-size="36" font-weight="700" fill="{cols[i]}">{esc(num)}</text>')
        b.append(f'    <text x="{x + 22:.0f}" y="{y + 76}" font-family="{SANS}" font-size="14" fill="{t["text"]}">{esc(l1)}</text>')
        b.append(f'    <text x="{x + 22:.0f}" y="{y + 96}" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{esc(l2)}</text>')
    return frame(t, H, "\n".join(b), "Impact: " + "; ".join(f"{a} {b_} {c}" for a, b_, c in IMPACT))


def experience(t):
    top, block = 70, 116
    H = top + block * len(ROLES) + 6
    b = [header(t, 48, 38, "git log --career", f"{len(ROLES)} roles · 4+ years")]
    x_line, x_text, x_right = 60, 92, WIDTH - 40
    b.append(f'    <line x1="{x_line}" y1="{top + 10}" x2="{x_line}" y2="{top + block * (len(ROLES) - 1) + 10}" stroke="{t["border"]}" stroke-width="2"/>')
    for i, (co, title, dates, loc, bullets) in enumerate(ROLES):
        y = top + i * block
        col = t["a1"] if i % 2 == 0 else t["a2"]
        current = "Present" in dates
        b.append(f'    <circle cx="{x_line}" cy="{y + 10}" r="8" fill="{t["bg"]}" stroke="{col}" stroke-width="3"/>')
        if current:
            b.append(f'    <circle cx="{x_line}" cy="{y + 10}" r="8" fill="none" stroke="{col}" stroke-width="2"><animate attributeName="r" values="8;15" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/></circle>')
        b.append(f'    <text x="{x_text}" y="{y + 16}" font-family="{SANS}" font-size="20" font-weight="700" fill="{t["text"]}">{esc(co)}<tspan dx="14" font-size="15" font-weight="600" fill="{col}">{esc(title)}</tspan></text>')
        b.append(f'    <text x="{x_right}" y="{y + 16}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["text"]}">{esc(dates)}</text>')
        b.append(f'    <text x="{x_right}" y="{y + 36}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(loc)}</text>')
        for j, line in enumerate(bullets):
            check_fits("▸ " + line, 14, x_right - x_text - 4, where=co)
            b.append(f'    <text x="{x_text}" y="{y + 50 + j * 24}" font-family="{SANS}" font-size="14" fill="{t["muted"]}"><tspan fill="{col}">▸</tspan> {esc(line)}</text>')
    return frame(t, H, "\n".join(b), "Experience: " + "; ".join(f"{r[1]} at {r[0]} ({r[2]})" for r in ROLES))


def toolbox(t):
    x_label, x0, x_max, row_h = 48, 230, WIDTH - 40, 42
    cols = [t["a1"], t["a2"], t["a3"], t["a4"]]
    rows, y = [], 66
    for i, (label, items) in enumerate(TOOLBOX):
        col = cols[i % 4]
        rows.append(f'    <text x="{x_label}" y="{y + 20}" font-family="{MONO}" font-size="13" fill="{col}">{esc(label)}/</text>')
        x = x0
        for it in items:
            w = len(it) * 12.5 * 0.62 + 24
            if x + w > x_max:
                x, y = x0, y + 38
            w, s = chip(t, x, y, it, col, size=12.5, h=28)
            rows.append(s.rstrip("\n"))
            x += w + 8
        y += row_h
    H = y + 14
    count = sum(len(i) for _, i in TOOLBOX)
    b = [header(t, 48, 38, "ls ~/toolbox", f"{count} tools · {len(TOOLBOX)} domains")] + rows
    return frame(t, H, "\n".join(b), "Toolbox: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in TOOLBOX))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("hero", hero), ("impact", impact), ("experience", experience), ("toolbox", toolbox)):
        for mode, t in THEMES.items():
            path = os.path.join(OUT, f"{name}-{mode}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(fn(t))
            print("wrote", path)
