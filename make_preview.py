#!/usr/bin/env python3
from pathlib import Path
import base64
import io
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"c:\Users\abdul\Desktop\AIVM\Abdul-Rehman-DevOps")
svg = (ROOT / "dark.svg").read_text(encoding="utf-8")
m = re.search(r'xlink:href="data:image/png;base64,([^"]+)"', svg)
assert m, "photo not embedded"
photo = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGB")

W, H = 1180, 610
img = Image.new("RGB", (W, H), (7, 11, 22))
d = ImageDraw.Draw(img)


def f(sz, bold=False):
    paths = (
        ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/consola.ttf"]
        if bold
        else ["C:/Windows/Fonts/consola.ttf"]
    )
    for p in paths:
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


d.rounded_rectangle((8, 8, 1172, 602), radius=16, outline=(34, 211, 238), width=3)
d.rectangle((8, 8, 1172, 54), fill=(11, 18, 34))
d.ellipse((30, 25, 42, 37), fill=(255, 95, 86))
d.ellipse((50, 25, 62, 37), fill=(255, 189, 46))
d.ellipse((70, 25, 82, 37), fill=(39, 201, 63))
d.text((350, 28), "abdulrehman.devops@gmail.com - % ./profile.sh --live", fill=(148, 163, 184), font=f(14))

# VISUAL.MAP photo (coding style, no studio bg)
photo = photo.resize((400, 470))
img.paste(photo, (56, 96))
d.rounded_rectangle((52, 92, 464, 570), radius=14, outline=(34, 211, 238), width=3)
d.text((76, 548), "./identity.png  --  coding profile", fill=(34, 211, 238), font=f(12))

d.text((500, 78), "SYSTEM.INFO", fill=(34, 211, 238), font=f(12, True))
rows = [
    ("Subject", "Abdul Rehman"),
    ("Role", "Senior DevOps / DevSecOps"),
    ("Origin", "Islamabad, Pakistan"),
    ("Focus", "Cloud / Platform / Security"),
    ("Status", "Building Secure Platforms"),
    ("ToolChain", "Terraform / K8s / GitOps"),
    ("Core.Cloud", "AWS / Azure / Multi-cloud"),
    ("Core.CICD", "Actions / Jenkins / ArgoCD"),
    ("Core.Mesh", "Istio / Helm / Karpenter"),
    ("Core.Sec", "Vault / Trivy / Falco / IAM"),
]
y = 110
for k, v in rows:
    d.text((500, y), f"{k} ...... {v}", fill=(226, 232, 240), font=f(14))
    y += 24
d.text((500, 370), "- Contact", fill=(100, 116, 139), font=f(12))
d.text((500, 394), "Grid.Mail ...... abdulrehman.devops@gmail.com", fill=(34, 211, 238), font=f(13))
d.text((500, 416), "Grid.Port ...... www.abdulrehman.cz", fill=(167, 139, 250), font=f(13))

out = ROOT / "preview-dark.png"
img.save(out)
print("wrote", out)
