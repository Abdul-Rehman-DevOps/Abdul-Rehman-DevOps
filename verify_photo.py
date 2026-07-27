#!/usr/bin/env python3
from pathlib import Path
import base64
import io
import re

from PIL import Image

ROOT = Path(r"c:\Users\abdul\Desktop\AIVM\Abdul-Rehman-DevOps")
svg = (ROOT / "dark.svg").read_text(encoding="utf-8")
print("size", len(svg))
print("has base64 image", "data:image/png;base64" in svg)
print("has image tag", "<image" in svg)
print("particle markers", svg.count("h1v1h-1"))
m = re.search(r"data:image/png;base64,([^\"']+)", svg)
print("match", bool(m))
if m:
    img = Image.open(io.BytesIO(base64.b64decode(m.group(1))))
    out = ROOT / "assets" / "embedded-photo-check.png"
    img.save(out)
    print("saved", out, img.size)
