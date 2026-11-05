"""Shared design tokens for every profile card (dark + light).

All cards are static SVGs: content is visible immediately; the only
animations are small infinite accents (pulse dot, flowing links), so a card
never renders as an empty box.
"""

SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"
WIDTH = 1200

THEMES = {
    "dark": {
        "bg": "#0D1117",
        "panel": "#161B22",
        "border": "#30363D",
        "text": "#E6EDF3",
        "muted": "#8B949E",
        "faint": "#21262D",
        "a1": "#22D3EE",   # cyan
        "a2": "#A78BFA",   # violet
        "a3": "#3FB950",   # green
        "a4": "#F0B429",   # amber
    },
    "light": {
        "bg": "#FFFFFF",
        "panel": "#F6F8FA",
        "border": "#D0D7DE",
        "text": "#1F2328",
        "muted": "#59636E",
        "faint": "#EAEEF2",
        "a1": "#0E7490",
        "a2": "#6D28D9",
        "a3": "#1A7F37",
        "a4": "#9A6700",
    },
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text_width(s, size, mono=False, bold=False):
    """Conservative width estimate so text never overflows a card."""
    factor = 0.62 if mono else (0.6 if bold else 0.56)
    return len(s) * size * factor


def check_fits(s, size, max_w, mono=False, bold=False, where=""):
    w = text_width(s, size, mono, bold)
    if w > max_w:
        raise SystemExit(f"text too wide ({w:.0f} > {max_w}) in {where}: {s!r}")


def frame(t, height, body, label):
    """Outer card: rounded panel, hairline border, gradient accent bar on top."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{esc(label)}">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
    </linearGradient>
    <clipPath id="card"><rect width="{WIDTH}" height="{height}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{WIDTH}" height="{height}" fill="{t['bg']}"/>
    <rect width="{WIDTH}" height="3" fill="url(#accent)"/>
{body}
  </g>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="16" fill="none" stroke="{t['border']}"/>
</svg>
'''


def header(t, x, y, cmd, right=""):
    out = f'''    <circle cx="{x}" cy="{y - 4}" r="5" fill="#FF5F57"/><circle cx="{x + 16}" cy="{y - 4}" r="5" fill="#FEBC2E"/><circle cx="{x + 32}" cy="{y - 4}" r="5" fill="#28C840"/>
    <text x="{x + 52}" y="{y}" font-family="{MONO}" font-size="13" fill="{t['muted']}"><tspan fill="{t['a3']}">abdul@platform</tspan>:<tspan fill="{t['a1']}">~</tspan>$ {esc(cmd)}</text>'''
    if right:
        out += f'\n    <text x="{WIDTH - 32}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(right)}</text>'
    return out
