# ⚙️ Archetype A Engine (`archetype_a`)

> **Runtime de Execução para Engenharia Latente Semântica (ELS).**

Este pacote Python é o motor responsável por carregar, validar e executar os **Arquétipos Cognitivos** definidos em YAML. Ele atua como um orquestrador determinístico que guia Large Language Models (LLMs) através de ciclos formais de raciocínio.

## 📦 Instalação

Se você estiver na raiz do repositório:

```bash
pip install -e .
```

## 🚀 Quick Start

A engine é agnóstica ao modelo. Você deve fornecer uma função de conector (`model_connector`) que receba uma string (prompt) e retorne uma string (resposta).

```python
from archetype_a import ArchetypeEngine

# 1. Defina seu conector (ex: Gemini, OpenAI, Claude, ou Mock)
def my_llm_connector(prompt: str, context: str) -> str:
    # Aqui vai a chamada real à API (ex: google.generativeai)
    return "Simulação de resposta do modelo..."

# 2. Instancie a Engine
engine = ArchetypeEngine(model_connector=my_llm_connector)

# 3. Execute um Arquétipo
result = engine.run(
    archetype_path="../archetypes/A_Psicologo.yaml",
    context="Sinto que meu trabalho não tem sentido.",
    verbose=True
)

# 4. Acesse o Traço de Execução (Audit Trail)
print(f"Estado Final: {result.final_state}")
for step in result.trace:
    print(f"[{step['operator']}] -> {step['output'][:50]}...")
```

-----

## 🏗️ Estrutura do Pacote

### 1\. `ArchetypeEngine` (em `engine.py`)

A classe principal que gerencia o ciclo de vida da cognição.

#### Métodos Principais:

  - **`__init__(model_connector)`**:
    Recebe um callable `(prompt, state) -> str`. Isso permite plugar qualquer LLM (Gemini, GPT-4, Llama local).

  - **`load_archetype(filepath)`**:
    Lê o YAML, valida a presença de chaves obrigatórias (`identity`, `cycle`) e prepara a estrutura em memória.

  - **`resolve_tensioners(op, user_tensioners)`**:
    Aplica a lógica de álgebra vetorial para combinar os tensionadores padrão do arquétipo com os ajustes finos (overrides) do usuário em tempo de execução.

  - **`run(archetype_path, context, user_tensioners)`**:
    O loop principal. Itera sobre cada operador ($\mathcal{O}_n$), constrói o System Prompt contextualizado, invoca a LLM e atualiza o estado latente.

### 2\. `ArchetypeResult` (Data Class)

Objeto de retorno padronizado contendo:

  - `trace`: Lista completa de inputs/outputs por etapa (para auditoria).
  - `final_state`: O resultado da "Coagulação" (última etapa).
  - `timestamp`: Momento da execução.
  - `context`: O input original.

-----

## 🔌 Integração com Modelos

A engine espera que o `model_connector` tenha a seguinte assinatura:

```python
from typing import Any

def connector(system_prompt: str, user_context: str) -> str:
    """
    Args:
        system_prompt: As regras estritas da etapa atual (Regras + Tensionadores).
        user_context: O estado acumulado da conversa até agora.
    Returns:
        String contendo apenas a resposta da etapa.
    """
    pass
```

### Exemplo com Google Gemini:

```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')

def gemini_adapter(sys, ctx):
    # Combina System + Contexto para modelos que não suportam system_instruction nativo
    full_prompt = f"{sys}\n\nCONTEXTO ATUAL:\n{ctx}"
    response = model.generate_content(full_prompt)
    return response.text

engine = ArchetypeEngine(model_connector=gemini_adapter)
```

-----

## 🧠 Conceitos Internos

### Tensionadores ($T$)

Parâmetros flutuantes (`0.0` a `1.0`) que modulam o comportamento da instrução.

  - **Engine Logic:** Se o YAML define `T_rigor: 0.8`, a engine injeta explicitamente no prompt: `[MODULATION]: Rigor level is 0.8 (High). Prioritize logic over empathy.`

### Traceability (Rastreabilidade)

Diferente de frameworks como LangChain que abstraem muito a execução, o `ArchetypeA` foca na transparência. O objeto `result.trace` é um log imutável de "como a IA pensou", passo a passo.

-----

## 🤝 Contribuindo

Para adicionar novas métricas ou funcionalidades à engine:

1.  Edite `engine.py`.
2.  Adicione testes em `../tests`.
3.  Garanta que a tipagem (`mypy`) esteja estrita.

-----

*Parte do projeto **Códice Cognitivo Vol. 1**.*
