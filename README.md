# Purple 1984

Tema escuro roxo para VS Code: combina o realce de sintaxe (tokenColors) do tema
[1984](https://github.com/juanmnl/vs-1984) por [juanmnl](https://github.com/juanmnl) com uma
paleta de UI roxa customizada (sidebar, tabs, terminal, status bar, etc).

## Instalação

### Via arquivo `.vsix` (local)

1. Abra o VS Code.
2. `Ctrl+Shift+P` / `Cmd+Shift+P` → `Extensions: Install from VSIX...`
3. Selecione o arquivo `purple-1984-theme-1.0.0.vsix`.
4. `Ctrl+Shift+P` → `Preferences: Color Theme` → escolha **Purple 1984**.

### Via Marketplace (se publicado)

```
ext install ryanditko.purple-1984-theme
```

## Desenvolvimento

```bash
npm install -g @vscode/vsce
vsce package
```

Isso gera o `.vsix` na raiz do projeto.

## Créditos

- Cores de sintaxe (`tokenColors`) derivadas do tema [1984](https://github.com/juanmnl/vs-1984),
  © juanmnl, licenciado sob MIT (ver `LICENSE`).
- Paleta de UI (background, sidebar, tabs, terminal) customizada por Ryanditko.
