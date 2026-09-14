# E.V. Theme

Tema escuro roxo para VS Code, com paleta de UI customizada (sidebar, tabs, terminal, status bar, etc)
e realce de sintaxe vibrante.

## Instalação

### Via arquivo `.vsix` (local)

1. Abra o VS Code.
2. `Ctrl+Shift+P` / `Cmd+Shift+P` → `Extensions: Install from VSIX...`
3. Selecione o arquivo `ev-theme-1.0.0.vsix`.
4. `Ctrl+Shift+P` → `Preferences: Color Theme` → escolha **E.V. Theme**.

### Via Marketplace (se publicado)

```
ext install ryanditko.ev-theme
```

## Desenvolvimento

```bash
npm install -g @vscode/vsce
vsce package
```

Isso gera o `.vsix` na raiz do projeto.

## Créditos

- As regras de realce de sintaxe (`tokenColors`) desta extensão foram originalmente derivadas do tema
  open-source [1984](https://github.com/juanmnl/vs-1984), © juanmnl, licenciado sob MIT (ver `LICENSE`
  para o aviso de copyright completo).
- Paleta de UI (background, sidebar, tabs, terminal) e empacotamento por Ryanditko.
