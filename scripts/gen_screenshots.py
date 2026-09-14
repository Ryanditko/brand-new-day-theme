import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_DIR = os.path.join(BASE_DIR, "themes")
SHOTS_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(SHOTS_DIR, exist_ok=True)

VARIANTS = [
    ("brand-new-day-ev-theme-color-theme.json", "purple"),
    ("brand-new-day-ev-theme-crimson-color-theme.json", "crimson"),
    ("brand-new-day-ev-theme-neon-color-theme.json", "neon"),
    ("brand-new-day-ev-theme-midnight-color-theme.json", "midnight"),
    ("brand-new-day-ev-theme-emerald-color-theme.json", "emerald"),
    ("brand-new-day-ev-theme-amber-color-theme.json", "amber"),
]

CODE_LINES = [
    ("comment", "// Brand New Day EV Theme — sample module"),
    ("keyword", "import", "plain", " { createServer } ", "keyword", "from", "string", " 'node:http';"),
    ("keyword", "import", "plain", " { readFileSync } ", "keyword", "from", "string", " 'node:fs';"),
    ("blank",),
    ("keyword", "const", "variable", " PORT ", "op", "=", "number", " 8080", "plain", ";"),
    ("keyword", "const", "variable", " MAX_RETRIES ", "op", "=", "number", " 3", "plain", ";"),
    ("blank",),
    ("comment", "  // retry wrapper with exponential backoff"),
    ("keyword", "async function", "func", " handleRequest", "plain", "(", "param", "req, res", "plain", ") {"),
    ("indent", "keyword", "  const", "variable", " payload ", "op", "=", "plain", " {"),
    ("indent2", "prop", "    status:", "string", " 'ok'", "plain", ","),
    ("indent2", "prop", "    retries:", "number", " MAX_RETRIES", "plain", ","),
    ("indent2", "prop", "    uptime:", "func", " process", "plain", ".", "func", "uptime", "plain", "(),"),
    ("indent", "plain", "  };"),
    ("blank",),
    ("indent", "func", "  res", "plain", ".", "func", "writeHead", "plain", "(", "number", "200", "plain", ", { ", "prop", "'Content-Type'", "plain", ": ", "string", "'application/json'", "plain", " });"),
    ("indent", "func", "  res", "plain", ".", "func", "end", "plain", "(", "func", "JSON", "plain", ".", "func", "stringify", "plain", "(payload));"),
    ("plain0", "}"),
    ("blank",),
    ("func0", "createServer", "plain", "(handleRequest).", "func", "listen", "plain", "(PORT, ", "func", "()", "plain", " => {"),
    ("indent", "func", "  console", "plain", ".", "func", "log", "plain", "(", "string", "`Server ready on :${PORT}`", "plain", ");"),
    ("plain0", "});"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_code(token_palette):
    COLORS = {
        "keyword": token_palette["keyword"],
        "string": token_palette["string"],
        "number": token_palette["keyword"],
        "func": token_palette["func"],
        "variable": token_palette["variable"],
        "prop": token_palette["type"],
        "comment": token_palette["comment"],
        "op": token_palette["keyword"],
        "param": token_palette["variable"],
        "plain": token_palette["func"],
    }
    html = []
    for line in CODE_LINES:
        if line[0] == "blank":
            html.append("<div class='line'>&nbsp;</div>")
            continue
        indent = ""
        rest = line
        if line[0] == "indent":
            indent = "&nbsp;&nbsp;"
            rest = line[1:]
        elif line[0] == "indent2":
            indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
            rest = line[1:]
        elif line[0] in ("plain0", "func0"):
            rest = line[1:] if line[0] == "plain0" else line
            if line[0] == "func0":
                rest = line
        spans = indent
        it = iter(rest) if line[0] not in ("plain0",) else iter(line[1:])
        if line[0] == "comment":
            spans += f"<span style='color:{COLORS['comment']};font-style:italic'>{esc(line[1])}</span>"
            html.append(f"<div class='line'>{spans}</div>")
            continue
        if line[0] == "func0":
            pairs = list(zip(line[0::2], line[1::2])) if len(line) % 2 == 0 else list(zip(line[::2], line[1::2]))
            spans = "".join(f"<span style='color:{COLORS.get(k,'#f1f1f1')}'>{esc(v)}</span>" for k, v in zip(line[0::2], line[1::2]))
            html.append(f"<div class='line'>{spans}</div>")
            continue
        pairs = list(zip(rest[0::2], rest[1::2]))
        spans = indent + "".join(f"<span style='color:{COLORS.get(k,'#f1f1f1')}'>{esc(v)}</span>" for k, v in pairs)
        html.append(f"<div class='line'>{spans}</div>")
    return "\n".join(html)


def render_minimap(token_palette):
    palette_cycle = [
        token_palette["keyword"], token_palette["string"], token_palette["variable"],
        token_palette["type"], token_palette["func"], token_palette["comment"],
    ]
    widths = [38, 62, 90, 20, 70, 55, 84, 30, 66, 48, 76, 40, 58, 88, 22, 64, 42, 80, 34, 60,
              50, 72, 28, 68, 44, 82, 36, 56]
    lines = []
    for i, w in enumerate(widths):
        color = palette_cycle[i % len(palette_cycle)]
        opacity = 0.85 if i % 4 else 0.5
        lines.append(f"<div class='mline' style='width:{w}%;background:{color};opacity:{opacity}'></div>")
    return "\n".join(lines)


def extract_token_palette(theme):
    by_name = {t["name"]: t["settings"]["foreground"] for t in theme["tokenColors"] if "foreground" in t.get("settings", {})}
    return {
        "keyword": by_name["Keyword"],
        "string": by_name["String"],
        "variable": by_name["Variable"],
        "type": by_name["Entity"],
        "func": by_name["Function"],
        "comment": by_name["Comment"],
    }

HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; background: {editor_bg}; }}
body {{
  font-family: -apple-system, 'Segoe UI', sans-serif;
  display: flex; align-items: center; justify-content: center;
  background:
    radial-gradient(circle at 20% 15%, {accent}14 0%, transparent 45%),
    radial-gradient(circle at 100% 100%, {accent}0d 0%, transparent 50%),
    {editor_bg};
}}
.stage {{ padding: 56px; }}
.window {{
  width: 1280px; height: 760px; background: {editor_bg}; color: {editor_fg};
  display: flex; flex-direction: column; overflow: hidden;
  border-radius: 10px; border: 1px solid {border};
  box-shadow: 0 40px 90px -20px #000000aa, 0 0 0 1px #00000033, 0 0 60px -10px {accent}33;
}}
.titlebar {{
  height: 34px; background: {titlebar_bg}; display: flex; align-items: center;
  padding: 0 12px; gap: 8px; border-bottom: 1px solid {border};
}}
.dot {{ width: 12px; height: 12px; border-radius: 50%; }}
.titlebar .title {{ margin-left: 12px; font-size: 12px; color: {sidebar_fg}; }}
.body {{ flex: 1; display: flex; overflow: hidden; }}
.activitybar {{
  width: 48px; background: {activitybar_bg}; display: flex; flex-direction: column;
  align-items: center; padding-top: 12px; gap: 22px; border-right: 1px solid {border};
}}
.abicon {{ width: 22px; height: 22px; border-radius: 5px; }}
.abicon.active {{ background: {accent}22; }}
.sidebar {{
  width: 220px; background: {sidebar_bg}; padding: 12px 8px; border-right: 1px solid {border};
}}
.sidebar .header {{ font-size: 11px; letter-spacing: 1px; color: {sidebar_fg}; margin-bottom: 10px; opacity: .8; }}
.sidebar .item {{ font-size: 13px; color: {sidebar_fg}; padding: 4px 6px; border-radius: 4px; }}
.sidebar .item.active {{ background: {selection_bg}; color: {editor_fg}; }}
.sidebar .folder {{ opacity: .85; margin-top: 6px; }}
.editorarea {{ flex: 1; display: flex; flex-direction: column; min-width: 0; }}
.tabs {{ height: 36px; background: {tabsbar_bg}; display: flex; border-bottom: 1px solid {border}; }}
.tab {{
  padding: 0 16px; display: flex; align-items: center; font-size: 13px;
  color: {tab_inactive_fg}; background: {tab_inactive_bg}; border-right: 1px solid {border};
}}
.tab.active {{ background: {editor_bg}; color: {accent}; border-top: 2px solid {accent}; }}
.editor {{ flex: 1; padding: 16px 20px; font-family: 'SF Mono', Menlo, monospace; font-size: 13px; line-height: 1.65; position: relative; }}
.editor .line {{ white-space: pre; }}
.editor .cursorline {{ background: {linehighlight}; margin: 0 -20px; padding: 0 20px; }}
.minimap {{
  width: 90px; border-left: 1px solid {border}; background: {sidebar_bg};
  padding: 16px 14px; display: flex; flex-direction: column; gap: 4px; opacity: .9;
}}
.minimap .mline {{ height: 3px; border-radius: 2px; }}
.statusbar {{
  height: 26px; background: {statusbar_bg}; display: flex; align-items: center;
  padding: 0 12px; gap: 16px; font-size: 11px; color: {editor_fg}; opacity: .85;
}}
.statusbar .accent {{ color: {accent}; font-weight: 600; }}
.badge {{ background: {accent}; color: #000; border-radius: 8px; padding: 0 6px; font-size: 10px; font-weight: 700; }}
</style></head>
<body>
<div class="stage">
<div class="window">
  <div class="titlebar">
    <div class="dot" style="background:#ff5f57"></div>
    <div class="dot" style="background:#febc2e"></div>
    <div class="dot" style="background:#28c840"></div>
    <div class="title">server.js — {variant_label}</div>
  </div>
  <div class="body">
    <div class="activitybar">
      <div class="abicon active" style="background:{accent}22"></div>
      <div class="abicon" style="background:{sidebar_fg}22"></div>
      <div class="abicon" style="background:{sidebar_fg}22"></div>
      <div class="abicon" style="background:{sidebar_fg}22"></div>
    </div>
    <div class="sidebar">
      <div class="header">EXPLORER</div>
      <div class="item folder">▾ ev-theme</div>
      <div class="item folder" style="padding-left:14px">▾ src</div>
      <div class="item active" style="padding-left:28px">server.js</div>
      <div class="item" style="padding-left:28px">routes.js</div>
      <div class="item" style="padding-left:28px">utils.js</div>
      <div class="item folder" style="padding-left:14px">▸ themes</div>
      <div class="item" style="padding-left:14px">package.json</div>
      <div class="item" style="padding-left:14px">README.md</div>
    </div>
    <div class="editorarea">
      <div class="tabs">
        <div class="tab active">server.js</div>
        <div class="tab">routes.js</div>
        <div class="tab">package.json</div>
      </div>
      <div class="editor">
        {code}
      </div>
    </div>
    <div class="minimap">
      {minimap}
    </div>
  </div>
  <div class="statusbar">
    <span class="accent">●</span>
    <span>main</span>
    <span>UTF-8</span>
    <span>LF</span>
    <span>JavaScript</span>
    <span class="badge">{variant_label}</span>
  </div>
</div>
</div>
</body></html>
"""


def build_html(theme_path, variant_label):
    theme = json.load(open(os.path.join(THEMES_DIR, theme_path)))
    c = theme["colors"]
    token_palette = extract_token_palette(theme)
    code_html = render_code(token_palette)
    minimap_html = render_minimap(token_palette)
    html = HTML_TEMPLATE.format(
        editor_bg=c["editor.background"],
        editor_fg=c.get("editor.foreground", "#f1f1f1"),
        titlebar_bg=c["titleBar.activeBackground"],
        sidebar_bg=c["sideBar.background"],
        sidebar_fg=c["sideBar.foreground"],
        activitybar_bg=c["activityBar.background"],
        accent=c["activityBar.foreground"],
        border=c["sideBar.border"],
        selection_bg=c["list.activeSelectionBackground"],
        tabsbar_bg=c["editorGroupHeader.tabsBackground"],
        tab_inactive_bg=c["tab.inactiveBackground"],
        tab_inactive_fg=c["sideBar.foreground"],
        linehighlight=c["editor.lineHighlightBackground"],
        statusbar_bg=c["statusBar.background"],
        variant_label=variant_label.capitalize(),
        code=code_html,
        minimap=minimap_html,
    )
    return html


if __name__ == "__main__":
    for fname, key in VARIANTS:
        html = build_html(fname, key)
        out = os.path.join(SHOTS_DIR, f"{key}.html")
        with open(out, "w") as f:
            f.write(html)
        print("wrote", out)
