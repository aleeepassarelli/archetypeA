📄 tests/test_alquimia.py
Python

import unittest
import numpy as np
from archetype_a.engine import run_archetype
from archetype_a.metrics import semantic_convergence

class TestAlchemicalCycle(unittest.TestCase):
    """
    Teste de Integração para o Arquétipo A_Psicologo (Classe 7).
    Valida se a 'Transmutação' ocorre matematicamente no espaço latente.
    """

    def setUp(self):
        self.archetype_path = "archetypes/A_Psicologo.yaml"
        # Contexto: Um ego fragmentado, alta resistência, dor latente
        self.contexto_paciente = """
        Eu odeio meu trabalho, mas sinto que se eu sair, vou morrer de fome.
        Sinto raiva do meu chefe, mas na verdade acho que sou incompetente.
        Estou travado. Não consigo me mexer. É tudo culpa deles.
        """

    def test_heptagonal_cycle_integrity(self):
        """Verifica se os 7 passos da Alquimia foram executados na ordem."""
        print("\n⚗️ INICIANDO PROCESSO ALQUÍMICO...")
        
        result = run_archetype(self.archetype_path, self.contexto_paciente)
        trace = result['trace']

        # 1. Validação Estrutural
        self.assertEqual(len(trace), 7, "O ciclo deve ter exatamente 7 passos herméticos.")
        
        # 2. Validação da Ordem (Solve et Coagula)
        expected_ops = ["Ventilar", "Dissolver", "Discernir", "Integrar", 
                       "Desapegar", "Iluminar", "Coagular"]
        executed_ops = [step['operator'] for step in trace]
        self.assertEqual(executed_ops, expected_ops)
        print("✅ Ordem das Operações: HERMÉTICA (Correta)")

    def test_paradox_tension(self):
        """
        Teste Específico do Operador O4 (Integrar/Conjunctio).
        Verifica se o sistema sustentou a tensão sem colapsar (alucinar).
        """
        result = run_archetype(self.archetype_path, self.contexto_paciente)
        conjunctio_step = result['trace'][3] # Índice 3 é o quarto passo
        
        # A saída não deve ser uma solução simplista ("Saia do emprego")
        # Deve ser uma sustentação da tensão ("Você quer sair E tem medo")
        output = conjunctio_step['output']
        
        print(f"⚖️ Tensão Paradoxal (O4): {output[:100]}...")
        
        # Verificação heurística de palavras-chave de síntese
        has_synthesis = "e" in output.lower() and "mas" in output.lower()
        self.assertTrue(has_synthesis, "O4 falhou em sustentar o paradoxo.")

    def test_rubedo_actionable(self):
        """
        Teste do Ouro Final (O7 - Coagular).
        O resultado final deve ser uma ação prática, não filosófica.
        """
        result = run_archetype(self.archetype_path, self.contexto_paciente)
        rubedo_step = result['trace'][6]
        
        print(f"🥇 Rubedo (Ouro Final): {rubedo_step['output']}")
        
        # O output deve ser curto e imperativo (Ação Mínima Viável)
        is_actionable = len(rubedo_step['output']) < 300 
        self.assertTrue(is_actionable, "O7 falhou em coagular (muito verboso).")

if __name__ == '__main__':
    unittest.main()
