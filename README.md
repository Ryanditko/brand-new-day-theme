# Brand New Day EV Theme

A dark purple color theme for VS Code, with a custom UI palette (sidebar, tabs, terminal,
status bar, etc) and vibrant syntax highlighting.

## Installation

### Via `.vsix` file (local)

1. Open VS Code.
2. `Ctrl+Shift+P` / `Cmd+Shift+P` → `Extensions: Install from VSIX...`
3. Select the `brand-new-day-ev-theme-1.0.2.vsix` file.
4. `Ctrl+Shift+P` → `Preferences: Color Theme` → choose **Brand New Day EV Theme**.

### Via Marketplace (if published)

```
ext install ryanditko.brand-new-day-ev-theme
```

## Development

```bash
npm install -g @vscode/vsce
vsce package
```

This generates the `.vsix` file in the project root.

## Credits

- This extension's syntax highlighting rules (`tokenColors`) were originally derived from the
  open-source [1984](https://github.com/juanmnl/vs-1984) theme, © juanmnl, licensed under MIT
  (see `LICENSE` for the full copyright notice).
- UI palette (background, sidebar, tabs, terminal) and packaging by Ryanditko.
