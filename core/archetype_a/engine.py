import os
import yaml
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Se quiser usar Rich para logs bonitos no terminal
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None

@dataclass
class ArchetypeResult:
    archetype_name: str
    context: str
    trace: List[Dict]
    final_state: str
    timestamp: str

class ArchetypeEngine:
    def __init__(self, model_connector: Any = None):
        """
        Inicializa a Engine.
        :param model_connector: Objeto ou função que conecta à LLM (ex: google.generativeai)
        """
        self.model = model_connector

    def load_archetype(self, filepath: str) -> Dict:
        """Carrega e valida o arquivo YAML do arquétipo."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquétipo não encontrado: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return data

    def resolve_tensioners(self, operation: Dict, user_tensioners: Optional[Dict] = None) -> Dict:
        """
        Combina tensionadores padrão do YAML com overrides do usuário.
        """
        base = operation.get('default_tensioners', {}).copy() # Evita mutação
        # Se o operador tiver tensionadores específicos
        op_tensioners = operation.get('tensioners', {})
        base.update(op_tensioners)
        
        if user_tensioners:
            # Apenas atualiza chaves que já existem (segurança de tipo)
            valid_updates = {k: v for k, v in user_tensioners.items() if k in base}
            base.update(valid_updates)
            
        return base

    def _build_system_prompt(self, identity: Dict, op: Dict, tensioners: Dict) -> str:
        """Constrói o prompt estruturado para a etapa atual."""
        return f"""
        [ARCHETYPE SYSTEM: {identity['name']} v{identity['version']}]
        DOMAIN: {identity['domain']}
        CLASS: {identity.get('class', {}).get('purpose', 'General')}
        
        >>> CURRENT OPERATOR: {op['name']} (ID: {op['operator_id']})
        FUNCTION: {op['function']}
        
        [RULES & CONSTRAINTS]
        {json.dumps(op.get('rules', []), indent=2, ensure_ascii=False)}
        
        [TENSIONERS (Modulation)]
        {json.dumps(tensioners, indent=2)}
        
        INSTRUCTION: Execute this cognitive operator strictly. Do not hallucinate outside the rules.
        """

    def run(self, archetype_path: str, context: str, user_tensioners: Optional[Dict] = None, verbose: bool = True) -> ArchetypeResult:
        """
        Executa o ciclo completo do arquétipo.
        """
        arch_data = self.load_archetype(archetype_path)
        identity = arch_data['identity']
        cycle = arch_data['cycle']
        
        trace = []
        current_state = context
        
        if verbose and console:
            console.print(Panel(f"[bold cyan]Iniciando {identity['name']}[/bold cyan]\nContexto: {context[:100]}...", title="ELS Engine"))

        for step in cycle:
            # 1. Preparação
            t_vals = self.resolve_tensioners(step, user_tensioners)
            sys_prompt = self._build_system_prompt(identity, step, t_vals)
            
            # 2. Execução (Chamada à LLM)
            # Aqui simulamos se não houver conector, ou chamamos a API real
            if self.model:
                # Adapte esta chamada conforme a lib da LLM (Gemini, OpenAI, LangChain)
                # Exemplo genérico: response = self.model.generate(sys_prompt, current_state)
                # Para este esqueleto, vamos assumir que self.model é uma função callable
                output = self.model(sys_prompt, current_state)
            else:
                output = f"[SIMULATION] Executed {step['name']} with tensioners {t_vals}"

            # 3. Registro (Trace)
            step_record = {
                "operator": step['name'],
                "operator_id": step['operator_id'],
                "tensioners": t_vals,
                "input_snapshot": current_state[:50] + "...",
                "output": output
            }
            trace.append(step_record)
            
            # 4. Atualização de Estado (Waterfall)
            # O output de hoje vira o input de amanhã (ou acumulamos no histórico)
            current_state = f"{current_state}\n\n[PREVIOUS OUTPUT ({step['name']})]: {output}"
            
            if verbose and console:
                console.print(f"[bold green]✓ {step['name']}[/bold green]")

        return ArchetypeResult(
            archetype_name=identity['name'],
            context=context,
            trace=trace,
            final_state=trace[-1]['output'], # O resultado da coagulação final
            timestamp=datetime.now().isoformat()
        )

# Exemplo de uso se rodar o arquivo diretamente
if __name__ == "__main__":
    # Mock connector para teste rápido sem API Key
    def mock_llm(sys, user):
        return "Cognitive process simulated."
        
    engine = ArchetypeEngine(model_connector=mock_llm)
    # Certifique-se de ter o arquivo YAML no caminho correto para testar
    # res = engine.run("archetypes/A_Psicologo.yaml", "Estou confuso.")
    # print(res)
