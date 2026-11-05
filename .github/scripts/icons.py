#!/usr/bin/env python3
"""Vendor brand icons into icons.json so card builds never depend on the network.

Sources (both open source):
  - Simple Icons (CC0)   https://simpleicons.org         -> single-path logos + brand hex
  - skill-icons  (MIT)   https://github.com/tandpfun/skill-icons -> AWS / Azure (not in Simple Icons)
Run after adding a new slug to SIMPLE or SKILL:  python3 .github/scripts/icons.py
"""
import json, os, re, urllib.request

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "icons.json")

SIMPLE = [
    "kubernetes", "helm", "argo", "flux", "istio", "traefikproxy", "nginx", "githubactions", "gitlab", "jenkins",
    "terraform", "ansible", "docker", "sonarqubeserver", "trivy", "zap", "owasp", "dependabot", "burpsuite",
    "prometheus", "grafana", "elastic", "elasticsearch", "uptimekuma", "k6", "postgresql", "redis", "apachekafka",
    "redhat", "ubuntu", "linux", "go", "python", "gnubash", "apachegroovy", "hashicorp", "yaml", "json",
    "googlecloud", "cloudflare", "digitalocean", "hetzner", "haproxy", "nvidia", "github",
]
SKILL = ["aws", "azure"]

# Simple shapes (24x24) for generic concepts that have no brand logo.
GLYPHS = {
    "g-shield": "M12 2l8 3v6c0 5.2-3.4 9.6-8 11-4.6-1.4-8-5.8-8-11V5l8-3zm-1.2 13.6l6-6-1.4-1.4-4.6 4.6-2.2-2.2-1.4 1.4 3.6 3.6z",
    "g-key": "M7.5 15.5a5.5 5.5 0 1 1 5.3-7H22v4h-2.5v3h-3.5v-3h-3.2a5.5 5.5 0 0 1-5.3 3zm0-3.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    "g-network": "M11 2h2v5h3v2H8V7h3V2zM4 11h16v2h-7v3h3v6H8v-6h3v-3H6v3h2v6H2v-6h2v-3zm16 0v3h2v6h-6v-6h2v-3h2z",
    "g-db": "M12 2c4.4 0 8 1.3 8 3v14c0 1.7-3.6 3-8 3s-8-1.3-8-3V5c0-1.7 3.6-3 8-3zm6 7.6C16.6 10.4 14.4 11 12 11s-4.6-.6-6-1.4V12c0 .6 2.3 1.8 6 1.8s6-1.2 6-1.8V9.6zm0 5.4c-1.4.8-3.6 1.4-6 1.4s-4.6-.6-6-1.4V19c0 .6 2.3 1.8 6 1.8s6-1.2 6-1.8v-4zM12 4C8.3 4 6 5.2 6 5.8s2.3 1.8 6 1.8 6-1.2 6-1.8S15.7 4 12 4z",
    "g-chain": "M10.6 13.4a4 4 0 0 1 0-5.7l3-3a4 4 0 1 1 5.7 5.7l-1.5 1.5-1.4-1.4 1.5-1.5a2 2 0 1 0-2.9-2.9l-3 3a2 2 0 0 0 0 2.9l-1.4 1.4zm2.8-2.8a4 4 0 0 1 0 5.7l-3 3a4 4 0 1 1-5.7-5.7l1.5-1.5 1.4 1.4-1.5 1.5a2 2 0 1 0 2.9 2.9l3-3a2 2 0 0 0 0-2.9l1.4-1.4z",
    "g-cloud": "M6.5 19a4.5 4.5 0 0 1-.9-8.9A6.5 6.5 0 0 1 18.2 9 5 5 0 0 1 18 19H6.5z",
    "g-scale": "M3 20h18v2H3v-2zm2-6h3v5H5v-5zm5-4h3v9h-3v-9zm5-6h3v15h-3V4zM14 2h6v6l-2-2-4 4-1.4-1.4 4-4L14 2z",
    "g-server": "M3 3h18v7H3V3zm0 11h18v7H3v-7zm3-8v1h2V6H6zm0 11v1h2v-1H6z",
    "g-code": "M8.6 16.6L4 12l4.6-4.6L10 8.8 6.8 12l3.2 3.2-1.4 1.4zm6.8 0L14 15.2l3.2-3.2L14 8.8l1.4-1.4L20 12l-4.6 4.6z",
    "g-gauge": "M12 4a10 10 0 0 1 10 10c0 2-.6 3.9-1.6 5.5H3.6A10 10 0 0 1 12 4zm0 2a8 8 0 0 0-7.4 11.5h14.8A8 8 0 0 0 12 6zm4.2 3.4l1.4 1.4-4.3 4.3a1.5 1.5 0 1 1-1.4-1.4l4.3-4.3z",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "profile-cards"}), timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    meta = {i["slug"]: i["hex"] for i in json.loads(get("https://cdn.jsdelivr.net/npm/simple-icons@latest/data/simple-icons.json"))}
    icons = {}
    for slug in SIMPLE:
        svg = get(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg")
        path = re.search(r'<path d="([^"]+)"', svg).group(1)
        icons[slug] = {"type": "path", "d": path, "hex": "#" + meta[slug]}
    for slug in SKILL:
        for theme in ("dark", "light"):
            svg = get(f"https://skillicons.dev/icons?i={slug}&theme={theme}")
            inner = re.search(r'<g transform="translate\(0, 0\)">\s*(<svg.*</svg>)\s*</g>', svg, re.S).group(1)
            inner = re.sub(r'<svg[^>]*>', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="none">', inner, count=1)
            icons[f"{slug}:{theme}"] = {"type": "svg", "svg": inner}
    for k, d in GLYPHS.items():
        icons[k] = {"type": "path", "d": d, "hex": None}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(icons, f, indent=1, sort_keys=True)
    print(f"wrote {OUT}: {len(icons)} icons")


if __name__ == "__main__":
    main()
