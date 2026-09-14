import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_DIR = os.path.join(BASE_DIR, "themes")

# Base ("Purple") token identity used as the find target across all variant files.
BASE = {
    "keyword": "#FF16B0",
    "keyword_hover": "#ff16b196",
    "keyword_alpha": "#ff16b17a",
    "string": "#DF81FC",
    "variable": "#96A1FF",
    "variable_alpha": "#96a0ff7c",
    "type": "#46BDFF",
    "type_alpha": "#46BDFF66",
    "func": "#fcfcfc",
    "comment": "#525863",
    "quote": "#FF407B",
}

# New token palettes per variant. Purple is intentionally omitted (it IS the base).
PALETTES = {
    "brand-new-day-ev-theme-amber-color-theme.json": {
        "keyword": "#FFB454",
        "string": "#7DD3FC",
        "variable": "#FFCC80",
        "type": "#F4A261",
        "func": "#fff6e8",
        "comment": "#6b5a3f",
        "quote": "#C084FC",
    },
    "brand-new-day-ev-theme-crimson-color-theme.json": {
        "keyword": "#FF5C7A",
        "string": "#FFD166",
        "variable": "#C9A0FF",
        "type": "#FF9EB0",
        "func": "#ffeef1",
        "comment": "#7a4b52",
        "quote": "#7DD3FC",
    },
    "brand-new-day-ev-theme-neon-color-theme.json": {
        "keyword": "#39F3FF",
        "string": "#FF71CE",
        "variable": "#B967FF",
        "type": "#C724E0",
        "func": "#f5e9ff",
        "comment": "#6a4b7a",
        "quote": "#FFD166",
    },
    "brand-new-day-ev-theme-midnight-color-theme.json": {
        "keyword": "#6EA8FE",
        "string": "#93C5FD",
        "variable": "#A5B4FC",
        "type": "#38BDF8",
        "func": "#e6edfb",
        "comment": "#4a5a73",
        "quote": "#F472B6",
    },
    "brand-new-day-ev-theme-emerald-color-theme.json": {
        "keyword": "#34D399",
        "string": "#FBBF24",
        "variable": "#6EE7B7",
        "type": "#10B981",
        "func": "#e5faf0",
        "comment": "#4a6b58",
        "quote": "#F472B6",
    },
}


def alpha_variant(hex_color, suffix):
    return f"{hex_color}{suffix}"


def apply_palette(fname, palette):
    path = os.path.join(THEMES_DIR, fname)
    with open(path) as f:
        text = f.read()

    replacements = [
        (BASE["keyword"], palette["keyword"]),
        (BASE["keyword_hover"], alpha_variant(palette["keyword"], "96")),
        (BASE["keyword_alpha"], alpha_variant(palette["keyword"], "7a")),
        (BASE["string"], palette["string"]),
        (BASE["variable"], palette["variable"]),
        (BASE["variable_alpha"], alpha_variant(palette["variable"], "7c")),
        (BASE["type"], palette["type"]),
        (BASE["type_alpha"], alpha_variant(palette["type"], "66")),
        (BASE["func"], palette["func"]),
        (BASE["comment"], palette["comment"]),
        (BASE["quote"], palette["quote"]),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    with open(path, "w") as f:
        f.write(text)
    print("updated", fname)


if __name__ == "__main__":
    for fname, palette in PALETTES.items():
        apply_palette(fname, palette)
