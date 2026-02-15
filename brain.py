import ollama
import json
from datetime import datetime

class AxiomBrain:
    def __init__(self, model="deepseek-r1:14b"):
        self.model = model
        self.history = []

    def think(self, user_input):
        print(f"\n[AXIOM está pensando...]")
        
        # Chamada ao DeepSeek R1
        response = ollama.chat(model=self.model, messages=[
            {'role': 'system', 'content': 'Você é o AXIOM, um robô humanoide autônomo. Seu criador é o Raphael. Seja lógico, amigável e protetor.'},
            {'role': 'user', 'content': user_input},
        ])

        reply = response['message']['content']
        
        # Simulação de Motor Epistêmico: Salvando a experiência
        self.save_memory(user_input, reply)
        
        return reply

    def save_memory(self, prompt, response):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        }
        with open("long_term_memory.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# Teste Real
if __name__ == "__main__":
    axiom = AxiomBrain()
    while True:
        pergunta = input("\nVocê (Raphael): ")
        if pergunta.lower() in ['sair', 'stop']: break
        
        resposta = axiom.think(pergunta)
        print(f"\nAXIOM: {resposta}")
