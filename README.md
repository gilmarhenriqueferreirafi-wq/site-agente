# IA Local · Dois Agentes

Chat local com dois agentes de IA (Geral e Coder) rodando via [Ollama](https://ollama.com), servido dentro de um Codespace/devcontainer.

## Estrutura

```
.
├── .devcontainer/
│   └── devcontainer.json   # config do Codespace (Ollama, portas, env vars)
├── index.html              # interface web do chat
├── server.py                # servidor HTTP simples pra servir o index.html
└── README.md
```

## Pré-requisitos

- GitHub Codespaces (ou VS Code com Dev Containers)
- Nenhuma instalação manual necessária — o `postCreateCommand` do devcontainer cuida de tudo na criação do Codespace

## Como iniciar

### 1. Abrir/criar o Codespace

Ao abrir o Codespace pela primeira vez (ou fazer rebuild), o `postCreateCommand` já instala o Ollama, sobe o servidor e baixa os modelos automaticamente. Isso pode levar alguns minutos na primeira vez.

### 2. Confirmar que o Ollama está rodando

```bash
curl http://localhost:11434/api/tags
```

Se voltar um JSON com a lista de modelos (`phi3:mini`, `qwen2.5-coder:1.5b`), está tudo certo.

Se der erro de conexão, suba manualmente:

```bash
OLLAMA_ORIGINS=* OLLAMA_MODELS=/workspaces/.ollama-models ollama serve &
```

### 3. Subir a interface web

```bash
python server.py
```

O Codespaces deve abrir a aba da porta **8000** automaticamente. Se não abrir sozinho, vai na aba **Ports** do VS Code e clica no ícone de globo ao lado da porta 8000.

### 4. Verificar a porta 11434 (API do Ollama)

Na aba **Ports**, confirme que a porta **11434** está com visibilidade **Public**. Se estiver como "Private", clica com o botão direito nela → **Port Visibility** → **Public**. Sem isso, o navegador recebe um redirect de login do GitHub em vez da resposta da API (erro de CORS na interface).

## Variáveis de ambiente importantes

| Variável | Valor | Motivo |
|---|---|---|
| `OLLAMA_ORIGINS` | `*` | Sem isso, o Ollama bloqueia por CORS as chamadas vindas do domínio `*.app.github.dev` da interface web |
| `OLLAMA_MODELS` | `/workspaces/.ollama-models` | `/tmp` é apagado a cada restart do Codespace — os modelos precisam ficar em `/workspaces`, que persiste |

Essas variáveis só são aplicadas de verdade quando o container é **criado ou reconstruído** (rebuild). Se você instalar/rodar o Ollama manualmente no terminal, precisa passar as variáveis na mão:

```bash
OLLAMA_ORIGINS=* OLLAMA_MODELS=/workspaces/.ollama-models ollama serve &
```

## Modelos usados

- **Agente Geral:** `phi3:mini` (~2,3GB)
- **Agente Coder:** `qwen2.5-coder:1.5b` (~1GB)

Modelo coder foi escolhido leve de propósito — o storage do Codespace nesta conta é limitado a 32GB, e o sistema já ocupa ~23GB. Se precisar de mais qualidade em código e tiver espaço sobrando, dá pra trocar por `qwen2.5-coder:3b` ou `qwen2.5-coder:7b` no `devcontainer.json` e no `index.html` (variável `AGENTS.coder.model`).

Para baixar/atualizar os modelos manualmente:

```bash
ollama pull phi3:mini
ollama pull qwen2.5-coder:1.5b
```

## Solução de problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| Interface mostra "ollama offline" | Ollama não está rodando | `ollama serve &` |
| Erro de CORS no console do navegador | Porta 11434 está "Private" | Mudar visibilidade pra "Public" na aba Ports |
| `403 Forbidden` nas chamadas | `OLLAMA_ORIGINS` não aplicado | Rebuild container, ou subir com `OLLAMA_ORIGINS=*` na mão |
| `{"error":"model 'x' not found"}` | Modelo não foi baixado | `ollama pull <nome-do-modelo>` |
| `bash: ollama: command not found` | Ollama não instalado nesse container | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Modelos somem após reiniciar o Codespace | `OLLAMA_MODELS` apontando pra `/tmp` | Trocar para `/workspaces/.ollama-models` no devcontainer.json e fazer rebuild |
| Pouco espaço em disco (`df -h /workspaces`) | Storage do Codespace limitado (32GB) | Usar modelos menores, ou aumentar a máquina se o plano permitir |

## Aplicar mudanças no devcontainer.json

Depois de editar o `devcontainer.json`, é preciso reconstruir o container pra que `containerEnv`, `postCreateCommand` e `postStartCommand` novos sejam aplicados:

```
Ctrl+Shift+P → Codespaces: Rebuild Container
```
