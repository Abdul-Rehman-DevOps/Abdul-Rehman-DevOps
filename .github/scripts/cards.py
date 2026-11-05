#!/usr/bin/env python3
"""Build the profile cards (dark + light) into cards/.

Edit the DATA section below, then run:  python3 .github/scripts/cards.py
Every fact here mirrors the resume - keep them in sync.
Cards are drawn at the real README width (theme.WIDTH) so text renders ~1:1.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES, SANS, MONO, WIDTH, esc, check_fits, wrap, frame, header  # noqa: E402

OUT = os.environ.get("CARDS_DIR", "cards")
PAD = 32  # left/right card padding

# ============================== DATA ==============================
NAME = "Abdul Rehman"
TITLE = "Senior DevOps / DevSecOps / Cloud Engineer"
TAGLINE = "I build, secure and run production Kubernetes platforms on AWS, Azure and GCP, for AI/GPU, SaaS and Web3 workloads."
PILLS = ["Kubernetes", "Terraform", "GitOps", "DevSecOps", "Multi-Cloud", "AI/GPU", "Web3 infra"]
STATUS = "Open to full-time & freelance"
LOCATION = "Islamabad, Pakistan · UTC+5"

IMPACT = [  # (big number, label)
    ("4+", "years of production DevOps & DevSecOps"),
    ("3", "clouds in production: AWS · Azure · GCP"),
    ("30+", "microservices run on Kubernetes"),
    ("~50%", "compute cost cut with Karpenter + Spot"),
    ("<4 min", "deploy time, down from 15 minutes"),
]

ROLES = [  # company, title, dates, location, bullets
    ("Funavry Technologies", "Senior DevOps / DevSecOps Engineer", "01/2026 — Present", "Islamabad", [
        "Architect and run 3–5 production Kubernetes clusters on Amazon EKS, Azure AKS and Google GKE, provisioned with Terraform (remote state, Checkov-scanned)",
        "GitOps with ArgoCD and FluxCD across all three clouds; KEDA + Karpenter autoscaling on Spot cut compute cost by ~50%",
        "DevSecOps gates (Semgrep, SonarQube, OWASP ZAP, Trivy, Gitleaks), Istio mTLS, Cloudflare WAF; multi-node blockchain RPC; incident RCA",
    ]),
    ("IKONIC", "DevOps Engineer", "03/2025 — 01/2026", "Islamabad", [
        "Ran AWS EKS and Google GKE clusters plus DigitalOcean container workloads in production",
        "Deployed Python/React AI applications, including GPU-enabled inference workloads",
        "GitHub Actions CI/CD with dev → staging → prod promotion; Docker multi-stage builds to ECR, Artifact Registry and Docker Hub",
    ]),
    ("Forbmax", "DevOps / DevSecOps Engineer", "08/2023 — 03/2025", "Islamabad", [
        "Built and operated 3–4 Kubernetes clusters across cloud and an on-premises data center for a 30+ microservice media-streaming platform",
        "ArgoCD GitOps across all 30+ services; Jenkins pipelines gated by SonarQube, OWASP Dependency-Check and Trivy",
        "Helm, NGINX / Traefik ingress with automated TLS, Prometheus + Grafana monitoring, Ansible automation",
    ]),
    ("Onyx Tech", "Linux System Administrator", "10/2022 — 08/2023", "Lahore", [
        "Administered enterprise RHEL 7/8 servers: patching, YUM/RPM, LVM and RAID storage",
        "Supported Apache, DNS, NFS and FTP; iptables firewalls and SELinux hardening; monitoring, backup and recovery",
    ]),
]

CLOUDS = [  # provider, services
    ("AWS", ["EC2", "EKS", "ECS", "ECR", "Lambda", "S3", "RDS", "VPC", "Route 53", "ALB / NLB", "CloudFront",
             "IAM", "KMS", "Secrets Manager", "CloudWatch", "CloudTrail", "WAF"]),
    ("Azure", ["AKS", "VMs", "VNet", "ACR", "Key Vault", "Entra ID", "App Gateway", "Azure Monitor", "DevOps Pipelines"]),
    ("GCP", ["GKE", "Compute Engine", "Cloud Run", "Cloud Storage", "VPC", "IAM", "Artifact Registry", "Cloud Logging", "Cloud Monitoring"]),
]
OTHER_HOSTS = ["DigitalOcean", "Hetzner", "On-Premises data center"]

TOOLBOX = [
    ("kubernetes", ["EKS", "AKS", "GKE", "On-prem clusters", "Helm", "Karpenter", "KEDA", "HPA", "Istio", "Kiali", "Ingress-NGINX", "Traefik"]),
    ("gitops-ci", ["ArgoCD", "FluxCD", "GitHub Actions", "GitLab CI/CD", "Jenkins", "Azure DevOps Pipelines"]),
    ("iac", ["Terraform", "Ansible", "CloudFormation"]),
    ("containers", ["Docker", "Multi-stage builds", "Docker Compose", "Docker Hub", "ECR", "Artifact Registry"]),
    ("devsecops", ["SAST", "DAST", "SCA", "Container & IaC scanning", "Secrets scanning", "SonarQube", "Semgrep", "Trivy",
                   "OWASP ZAP", "OWASP Dependency-Check", "Gitleaks", "Checkov", "Dependabot", "Burp Suite"]),
    ("security", ["IAM / RBAC", "Least privilege", "Secrets management", "KMS", "Encryption at rest & in transit", "mTLS",
                  "Network policies", "Security Groups / NSG", "Cloudflare WAF & Turnstile", "AWS WAF", "SELinux"]),
    ("observability", ["Prometheus", "Grafana", "ELK Stack", "CloudWatch", "Uptime Kuma", "k6 load testing"]),
    ("data", ["PostgreSQL", "Redis", "Elasticsearch", "Kafka"]),
    ("linux-net", ["RHEL", "Ubuntu", "LVM", "RAID", "DNS", "NFS", "TCP/IP", "Load balancing", "iptables", "Nginx", "HAProxy"]),
    ("languages", ["Go", "Python", "Bash", "Groovy", "HCL", "YAML", "JSON", "SQL"]),
    ("web3", ["Blockchain node ops", "Distributed & hybrid nodes", "RPC infrastructure"]),
]
# ==================================================================

# Logo shown inside each chip (keys from icons.json; "g-*" are generic glyphs).
ICON = {
    # clouds / hosts
    "AWS": "aws", "Azure": "azure", "GCP": "googlecloud", "DigitalOcean": "digitalocean", "Hetzner": "hetzner",
    "On-Premises data center": "g-server", "Multi-Cloud": "g-cloud",
    # kubernetes
    "Kubernetes": "kubernetes", "EKS": "aws", "AKS": "azure", "GKE": "googlecloud", "On-prem clusters": "kubernetes",
    "Helm": "helm", "Karpenter": "g-scale", "KEDA": "g-scale", "HPA": "kubernetes", "Istio": "istio", "Kiali": "istio",
    "Ingress-NGINX": "nginx", "Traefik": "traefikproxy",
    # gitops / ci
    "GitOps": "argo", "ArgoCD": "argo", "FluxCD": "flux", "GitHub Actions": "githubactions", "GitLab CI/CD": "gitlab",
    "Jenkins": "jenkins", "Azure DevOps Pipelines": "azure",
    # iac / containers
    "Terraform": "terraform", "Ansible": "ansible", "CloudFormation": "aws",
    "Docker": "docker", "Multi-stage builds": "docker", "Docker Compose": "docker", "Docker Hub": "docker",
    "ECR": "aws", "Artifact Registry": "googlecloud",
    # devsecops / security
    "DevSecOps": "g-shield", "SAST": "g-code", "DAST": "g-shield", "SCA": "g-shield", "Container & IaC scanning": "g-shield",
    "Secrets scanning": "g-key", "SonarQube": "sonarqubeserver", "Semgrep": "g-code", "Trivy": "trivy", "OWASP ZAP": "zap",
    "OWASP Dependency-Check": "owasp", "Gitleaks": "g-key", "Checkov": "g-shield", "Dependabot": "dependabot",
    "Burp Suite": "burpsuite", "IAM / RBAC": "g-key", "Least privilege": "g-shield", "Secrets management": "g-key",
    "KMS": "g-key", "Encryption at rest & in transit": "g-key", "mTLS": "istio", "Network policies": "kubernetes",
    "Security Groups / NSG": "g-shield", "Cloudflare WAF & Turnstile": "cloudflare", "AWS WAF": "aws", "SELinux": "redhat",
    # observability / data
    "Prometheus": "prometheus", "Grafana": "grafana", "ELK Stack": "elastic", "CloudWatch": "aws",
    "Uptime Kuma": "uptimekuma", "k6 load testing": "k6",
    "PostgreSQL": "postgresql", "Redis": "redis", "Elasticsearch": "elasticsearch", "Kafka": "apachekafka",
    # linux / networking / languages
    "RHEL": "redhat", "Ubuntu": "ubuntu", "LVM": "linux", "RAID": "g-db", "DNS": "g-network", "NFS": "g-server",
    "TCP/IP": "g-network", "Load balancing": "g-network", "iptables": "linux", "Nginx": "nginx", "HAProxy": "haproxy",
    "Go": "go", "Python": "python", "Bash": "gnubash", "Groovy": "apachegroovy", "HCL": "hashicorp", "YAML": "yaml",
    "JSON": "json", "SQL": "g-db",
    # misc
    "AI/GPU": "nvidia", "Web3 infra": "g-chain", "Blockchain node ops": "g-chain", "Distributed & hybrid nodes": "g-network",
    "RPC infrastructure": "g-chain",
}
with open(os.path.join(os.path.dirname(__file__), "icons.json"), encoding="utf-8") as _f:
    ICONS = json.load(_f)


def _lum(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def icon(t, key, x, y, size, fallback):
    """Draw logo `key` with its top-left at (x, y). Brand colours are kept unless
    they would vanish on this theme's background, then the text colour is used."""
    if not key:
        return ""
    ic = ICONS.get(key) or ICONS.get(f"{key}:{t['mode']}")
    if ic is None:
        raise SystemExit(f"icon {key!r} missing - add it to icons.py and rerun it")
    if ic["type"] == "svg":
        return ic["svg"].replace("<svg ", f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" ', 1)
    col = ic["hex"] or fallback
    if ic["hex"]:
        l = _lum(col)
        if (t["mode"] == "dark" and l < 0.16) or (t["mode"] == "light" and l > 0.72):
            col = t["text"]
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})" fill="{col}" d="{ic["d"]}"/>'


CHIP_SIZE, CHIP_H = 13, 28
ICON_SIZE = 15


def chip_w(label, size=CHIP_SIZE, logos=True):
    return len(label) * size * 0.62 + 22 + (ICON_SIZE + 7 if logos and ICON.get(label) else 0)


def chip(t, x, y, label, color, size=CHIP_SIZE, h=CHIP_H, logos=True):
    w = chip_w(label, size, logos)
    key = ICON.get(label) if logos else None
    tx = x + 11 + (ICON_SIZE + 7 if key else 0)
    logo = icon(t, key, x + 11, y + (h - ICON_SIZE) / 2, ICON_SIZE, color)
    return w, (f'    <rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["panel"]}" stroke="{color}" stroke-opacity="0.6"/>\n'
               f'    {logo}<text x="{tx:.0f}" y="{y + h / 2 + size * 0.36:.1f}" font-family="{MONO}" font-size="{size}" fill="{t["text"]}">{esc(label)}</text>')


def flow_chips(t, items, color, x0, y0, x_max, gap=8, row_gap=8, logos=True):
    """Lay chips left-to-right, wrapping inside [x0, x_max]. Returns (svg, bottom_y)."""
    out, x, y = [], x0, y0
    for it in items:
        w = chip_w(it, logos=logos)
        if x + w > x_max and x > x0:
            x, y = x0, y + CHIP_H + row_gap
        if x0 + w > x_max:
            raise SystemExit(f"chip wider than its area: {it!r}")
        w, s = chip(t, x, y, it, color, logos=logos)
        out.append(s)
        x += w + gap
    return out, y + CHIP_H


def hero(t):
    left_max = 560
    b = [header(t, PAD + 8, 40, "whoami")]
    check_fits(NAME, 46, left_max - PAD, bold=True, where="hero name")
    check_fits(TITLE, 20, left_max - PAD, bold=True, where="hero title")
    b.append(f'    <text x="{PAD}" y="106" font-family="{SANS}" font-size="46" font-weight="700" fill="{t["text"]}">{esc(NAME)}</text>')
    b.append(f'    <text x="{PAD}" y="140" font-family="{SANS}" font-size="20" font-weight="600" fill="url(#accent)">{esc(TITLE)}</text>')
    y = 172
    for line in wrap(TAGLINE, 16, left_max - PAD):
        b.append(f'    <text x="{PAD}" y="{y}" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{esc(line)}</text>')
        y += 23
    colors = [t["a1"], t["a2"], t["a3"], t["a4"]]
    x, py = PAD, y - 4
    for i, p in enumerate(PILLS):
        if x + chip_w(p) > left_max:
            x, py = PAD, py + CHIP_H + 8
        w, s = chip(t, x, py, p, colors[i % 4])
        b.append(s); x += w + 8
    sy = py + CHIP_H + 34
    b.append(f'''    <circle cx="{PAD + 7}" cy="{sy - 5}" r="6" fill="{t["a3"]}"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
    <text x="{PAD + 22}" y="{sy}" font-family="{MONO}" font-size="14" fill="{t["text"]}">{esc(STATUS)}<tspan fill="{t["muted"]}">  ·  {esc(LOCATION)}</tspan></text>''')
    check_fits(STATUS + "  ·  " + LOCATION, 14, WIDTH - PAD - 22 - PAD, mono=True, where="hero status")
    H = sy + 30

    # right: cluster diagram - control plane in the middle, environments around it
    cx, cy, r = 740, 168, 90
    nodes = ["AWS", "Azure", "GCP", "on-prem", "GPU", "edge"]
    g = [f'    <circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="none" stroke="{t["border"]}" stroke-dasharray="2 6"/>']
    for i, n in enumerate(nodes):
        a = -math.pi / 2 + i * 2 * math.pi / len(nodes)
        nx, ny = cx + r * math.cos(a), cy + r * math.sin(a)
        col = t["a1"] if i % 2 == 0 else t["a2"]
        g.append(f'    <line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{col}" stroke-opacity="0.65" stroke-width="1.5" stroke-dasharray="4 6">'
                 f'<animate attributeName="stroke-dashoffset" values="20;0" dur="{1.2 + i * 0.15:.2f}s" repeatCount="indefinite"/></line>')
        g.append(f'    <circle cx="{nx:.1f}" cy="{ny:.1f}" r="26" fill="{t["panel"]}" stroke="{col}" stroke-width="1.5"/>')
        g.append(f'    <text x="{nx:.1f}" y="{ny + 4:.1f}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["text"]}">{esc(n)}</text>')
    g.append(f'    <circle cx="{cx}" cy="{cy}" r="38" fill="{t["bg"]}" stroke="url(#accent)" stroke-width="2.5"/>')
    g.append(f'    <text x="{cx}" y="{cy}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["text"]}">k8s</text>')
    g.append(f'    <text x="{cx}" y="{cy + 16}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["muted"]}">gitops</text>')
    if cy + r + 30 > H - 6:
        H = cy + r + 36
    b += g
    return frame(t, H, "\n".join(b), f"{NAME} — {TITLE}. {TAGLINE}")


def impact(t):
    n, gap = len(IMPACT), 10
    w = (WIDTH - 2 * PAD - gap * (n - 1)) / n
    cols = [t["a1"], t["a2"], t["a3"], t["a4"], t["a1"]]
    tiles, tile_h = [], 0
    for num, label in IMPACT:
        check_fits(num, 30, w - 28, bold=True, where="impact number")
        lines = wrap(label, 13, w - 28)
        tile_h = max(tile_h, 58 + 19 * len(lines) + 14)
        tiles.append((num, lines))
    y = 62
    b = [header(t, PAD + 8, 40, "cat impact.txt")]
    for i, (num, lines) in enumerate(tiles):
        x = PAD + i * (w + gap)
        b.append(f'    <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{tile_h}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        b.append(f'    <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="4" rx="2" fill="{cols[i]}"/>')
        b.append(f'    <text x="{x + 14:.0f}" y="{y + 44}" font-family="{SANS}" font-size="30" font-weight="700" fill="{cols[i]}">{esc(num)}</text>')
        for j, line in enumerate(lines):
            b.append(f'    <text x="{x + 14:.0f}" y="{y + 70 + j * 19}" font-family="{SANS}" font-size="13" fill="{t["text"]}">{esc(line)}</text>')
    H = y + tile_h + 26
    return frame(t, H, "\n".join(b), "Impact: " + "; ".join(f"{a} {b_}" for a, b_ in IMPACT))


def experience(t):
    x_line, x_text, x_right = PAD + 14, PAD + 44, WIDTH - PAD
    b = [header(t, PAD + 8, 40, "git log --career", f"{len(ROLES)} roles · 4+ years")]
    y, dots = 76, []
    for i, (co, title, dates, loc, bullets) in enumerate(ROLES):
        col = t["a1"] if i % 2 == 0 else t["a2"]
        dots.append((y, col, "Present" in dates))
        check_fits(co, 19, x_right - x_text - 170, bold=True, where="experience company")
        b.append(f'    <text x="{x_text}" y="{y + 6}" font-family="{SANS}" font-size="19" font-weight="700" fill="{t["text"]}">{esc(co)}</text>')
        b.append(f'    <text x="{x_text}" y="{y + 30}" font-family="{SANS}" font-size="15" font-weight="600" fill="{col}">{esc(title)}</text>')
        b.append(f'    <text x="{x_right}" y="{y + 6}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["text"]}">{esc(dates)}</text>')
        b.append(f'    <text x="{x_right}" y="{y + 28}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(loc)}</text>')
        by = y + 56
        for line in bullets:
            for k, part in enumerate(wrap(line, 14, x_right - x_text - 16)):
                if k == 0:
                    b.append(f'    <text x="{x_text}" y="{by}" font-family="{SANS}" font-size="14" fill="{col}">▸</text>')
                b.append(f'    <text x="{x_text + 16}" y="{by}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{esc(part)}</text>')
                by += 21
            by += 3
        y = by + 22
    first, last = dots[0][0], dots[-1][0]
    line = [f'    <line x1="{x_line}" y1="{first}" x2="{x_line}" y2="{last}" stroke="{t["border"]}" stroke-width="2"/>']
    for dy, col, current in dots:
        line.append(f'    <circle cx="{x_line}" cy="{dy}" r="8" fill="{t["bg"]}" stroke="{col}" stroke-width="3"/>')
        if current:
            line.append(f'    <circle cx="{x_line}" cy="{dy}" r="8" fill="none" stroke="{col}" stroke-width="2"><animate attributeName="r" values="8;15" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/></circle>')
    H = y - 6
    return frame(t, H, "\n".join(b[:1] + line + b[1:]), "Experience: " + "; ".join(f"{r[1]} at {r[0]} ({r[2]})" for r in ROLES))


def clouds(t):
    n, gap = len(CLOUDS), 12
    w = (WIDTH - 2 * PAD - gap * (n - 1)) / n
    cols = [t["a4"], t["a1"], t["a3"]]
    panels, bottoms = [], []
    top = 62
    for i, (name, svcs) in enumerate(CLOUDS):
        x = PAD + i * (w + gap)
        chips, bottom = flow_chips(t, svcs, cols[i], x + 14, top + 48, x + w - 14, gap=6, row_gap=7, logos=False)
        panels.append((x, name, chips, cols[i]))
        bottoms.append(bottom)
    ph = max(bottoms) - top + 16
    b = [header(t, PAD + 8, 40, "kubectl config get-clusters", "multi-cloud")]
    for (x, name, chips, col) in panels:
        b.append(f'    <rect x="{x:.0f}" y="{top}" width="{w:.0f}" height="{ph:.0f}" rx="12" fill="{t["panel"]}" fill-opacity="0.5" stroke="{t["border"]}"/>')
        b.append(f'    <rect x="{x:.0f}" y="{top}" width="{w:.0f}" height="4" rx="2" fill="{col}"/>')
        b.append("    " + icon(t, ICON.get(name), x + 14, top + 15, 24, col))
        b.append(f'    <text x="{x + 46:.0f}" y="{top + 34}" font-family="{SANS}" font-size="18" font-weight="700" fill="{col}">{esc(name)}</text>')
        b += chips
    oy = top + ph + 30
    other = "Also: " + " · ".join(OTHER_HOSTS)
    check_fits(other, 14, WIDTH - 2 * PAD, where="clouds footer")
    b.append(f'    <text x="{PAD}" y="{oy:.0f}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{esc(other)}</text>')
    H = oy + 22
    return frame(t, H, "\n".join(b), "Clouds: " + "; ".join(f"{n}: {', '.join(s)}" for n, s in CLOUDS) + "; also " + ", ".join(OTHER_HOSTS))


def toolbox(t):
    x_label, x0, x_max = PAD, PAD + 140, WIDTH - PAD
    cols = [t["a1"], t["a2"], t["a3"], t["a4"]]
    rows, y = [], 64
    for i, (label, items) in enumerate(TOOLBOX):
        col = cols[i % 4]
        check_fits(label + "/", 13, x0 - x_label - 8, mono=True, where="toolbox label")
        rows.append(f'    <text x="{x_label}" y="{y + 19}" font-family="{MONO}" font-size="13" fill="{col}">{esc(label)}/</text>')
        chips, bottom = flow_chips(t, items, col, x0, y, x_max)
        rows += chips
        y = bottom + 12
    count = sum(len(i) for _, i in TOOLBOX)
    b = [header(t, PAD + 8, 40, "ls ~/toolbox", f"{count} tools · {len(TOOLBOX)} domains")] + rows
    return frame(t, y + 14, "\n".join(b), "Toolbox: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in TOOLBOX))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("hero", hero), ("impact", impact), ("experience", experience),
                     ("clouds", clouds), ("toolbox", toolbox)):
        for mode, t in THEMES.items():
            path = os.path.join(OUT, f"{name}-{mode}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(fn(t))
            print("wrote", path)
