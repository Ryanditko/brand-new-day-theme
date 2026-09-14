import math
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(SHOTS_DIR, exist_ok=True)

# hue-ordered variant accents
SEGMENTS = [
    ("amber",    "#ffb454"),
    ("emerald",  "#34d399"),
    ("neon",     "#39f3ff"),
    ("midnight", "#6ea8fe"),
    ("purple",   "#bd93f9"),
    ("crimson",  "#ff5c7a"),
]

CX, CY = 200, 200
R_OUT = 175
R_IN = 100
VIEWBOX = 400


def polar(cx, cy, r, angle_deg):
    a = math.radians(angle_deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def donut_wedge(cx, cy, r_out, r_in, a0, a1):
    x0o, y0o = polar(cx, cy, r_out, a0)
    x1o, y1o = polar(cx, cy, r_out, a1)
    x0i, y0i = polar(cx, cy, r_in, a1)
    x1i, y1i = polar(cx, cy, r_in, a0)
    large_arc = 1 if (a1 - a0) > 180 else 0
    return (
        f"M {x0o:.2f},{y0o:.2f} "
        f"A {r_out},{r_out} 0 {large_arc} 1 {x1o:.2f},{y1o:.2f} "
        f"L {x0i:.2f},{y0i:.2f} "
        f"A {r_in},{r_in} 0 {large_arc} 0 {x1i:.2f},{y1i:.2f} Z"
    )


def build_svg(glow=True):
    n = len(SEGMENTS)
    step = 360 / n
    paths = []
    for i, (_, color) in enumerate(SEGMENTS):
        a0 = i * step
        a1 = a0 + step
        d = donut_wedge(CX, CY, R_OUT, R_IN, a0, a1)
        paths.append(f'<path d="{d}" fill="{color}" fill-opacity="0.92" stroke="#0a0a0f" stroke-width="2"/>')

    ticks = []
    tick_count = 36
    for i in range(tick_count):
        angle = i * (360 / tick_count)
        r1 = R_OUT + 8
        r2 = R_OUT + (16 if i % 3 == 0 else 11)
        x1, y1 = polar(CX, CY, r1, angle)
        x2, y2 = polar(CX, CY, r2, angle)
        ticks.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#4a4a5a" stroke-width="1.5" opacity="0.55"/>')

    svg = f"""
<svg width="{VIEWBOX}" height="{VIEWBOX}" viewBox="0 0 {VIEWBOX} {VIEWBOX}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="core" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#e8eaff"/>
      <stop offset="75%" stop-color="#b9bfe8" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#b9bfe8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur1"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="blur2"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>

  {"<circle cx='" + str(CX) + "' cy='" + str(CY) + "' r='" + str(R_OUT+30) + "' fill='url(#glow)' filter='url(#blur2)' opacity='0.35'/>" if glow else ""}

  <circle cx="{CX}" cy="{CY}" r="{R_OUT+6}" fill="none" stroke="#2a2a38" stroke-width="2" opacity="0.8"/>
  {''.join(ticks)}

  <g>
    {''.join(paths)}
  </g>

  <circle cx="{CX}" cy="{CY}" r="{R_IN-4}" fill="#0a0a0f"/>
  <circle cx="{CX}" cy="{CY}" r="{R_IN-4}" fill="none" stroke="#3a3a4a" stroke-width="1.5" opacity="0.7"/>

  <circle cx="{CX}" cy="{CY}" r="{R_IN-14}" fill="url(#core)"/>
  <rect x="{CX-16}" y="{CY-16}" width="32" height="32" fill="#ffffff" opacity="0.9" transform="rotate(45 {CX} {CY})"/>
  <rect x="{CX-16}" y="{CY-16}" width="32" height="32" fill="none" stroke="#c9ccff" stroke-width="1.5" opacity="0.8" transform="rotate(45 {CX} {CY})"/>
</svg>
"""
    return svg


ICON_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:100%; height:100%; }}
body {{
  display:flex; align-items:center; justify-content:center;
  background: radial-gradient(circle at 40% 35%, #1c1830 0%, #0c0a16 60%, #08070d 100%);
}}
</style></head>
<body>{svg}</body></html>
"""

BANNER_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:100%; height:100%; background: #0a0a12; }}
body {{
  font-family: -apple-system, 'Segoe UI', sans-serif;
  display:flex; align-items:center; justify-content:center;
  background: radial-gradient(circle at 22% 50%, #14101f 0%, #0a0a12 55%, #08070d 100%);
}}
.wrap {{ display:flex; align-items:center; gap:70px; padding: 0 70px; }}
.icon {{ width:180px; height:180px; flex-shrink:0; }}
.icon svg {{ width:100%; height:100%; display:block; }}
.text h1 {{
  font-size:48px; letter-spacing:4px; font-weight:800; white-space:nowrap;
  background: linear-gradient(90deg, #bd93f9, #ff5c7a, #ffb454, #34d399, #39f3ff, #6ea8fe);
  -webkit-background-clip: text; background-clip:text; color:transparent;
  margin-bottom: 4px;
}}
.text h2 {{
  font-size:20px; letter-spacing:8px; font-weight:600; color:#e8e6f0; margin-bottom:14px;
}}
.text .tagline {{
  font-size:14px; letter-spacing:2.5px; color:#8a8a9e; text-transform:uppercase;
  border-top: 1px solid #34324a; padding-top: 12px; display:inline-block;
}}
</style></head>
<body>
<div class="wrap">
  <div class="icon">{svg}</div>
  <div class="text">
    <h1>BRAND NEW DAY</h1>
    <h2>EV THEME</h2>
    <div class="tagline">Six Vibrant Dark Themes for VS Code</div>
  </div>
</div>
</body></html>
"""


def main():
    icon_svg = build_svg(glow=True)
    with open(os.path.join(SHOTS_DIR, "icon.html"), "w") as f:
        f.write(ICON_HTML.format(svg=icon_svg))

    banner_svg = build_svg(glow=True)
    with open(os.path.join(SHOTS_DIR, "banner.html"), "w") as f:
        f.write(BANNER_HTML.format(svg=banner_svg))

    print("wrote icon.html and banner.html")


if __name__ == "__main__":
    main()
