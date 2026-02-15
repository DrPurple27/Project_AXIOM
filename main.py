import threading
import time
import os
import subprocess # Adicionado para rodar o Piper

# Removido: from gtts import gTTS
# Removido: import pygame

from brain import AxiomBrain
from vision_stream import AxiomVision

# Removido: pygame.mixer.init()

def speak_worker(text):
    try:
        # Comando para o Piper gerar o áudio e o aplay tocar diretamente
        # Certifique-se de que o executável 'piper' está em ./piper/piper
        # E o modelo de voz está na mesma pasta ou no caminho especificado
        command = f'echo "{text}" | ./piper/piper --model pt_BR-faber-medium.onnx --output_raw | aplay -r 22050 -f S16_LE -t raw'
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"\n[Erro no Piper]: Comando falhou com código {e.returncode}. Saída: {e.stderr.decode()}")
    except Exception as e:
        print(f"\n[Erro no Piper]: {e}")

def speak(text):
    clean_text = text.split("</think>")[-1].strip()
    # Remove caracteres especiais que podem quebrar o shell ou o Piper
    clean_text = clean_text.replace("\"", "").replace("\"", "").replace("\n", " ")
    print(f"\nAXIOM: {clean_text}")
    threading.Thread(target=speak_worker, args=(clean_text,), daemon=True).start()

class AxiomRobot:
    def __init__(self):
        self.brain = AxiomBrain()
        self.vision = AxiomVision(interval=15) 
        self.vision_thread = threading.Thread(target=self.vision.vision_loop, daemon=True)

    def start(self):
        self.vision_thread.start()
        print("\n" + "="*30)
        print("   AXIOM ONLINE - MODO TERMINAL")
        print("="*30)
        speak("Sistemas iniciados. Olá Raphael, estou pronto.")
        
        while True:
            try:
                user_input = input("\nVocê (Raphael): ")
                if user_input.lower() in ["sair", "stop"]: break
                
                percepcao = self.vision.last_description
                
                prompt_completo = f"""
                [INSTRUÇÃO]: Use a percepção visual abaixo para enriquecer sua resposta se for relevante.
                [VISÃO ATUAL]: {percepcao}
                [USUÁRIO DIZ]: {user_input}
                """
                
                resposta = self.brain.think(prompt_completo)
                speak(resposta)
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    robot = AxiomRobot()
    robot.start()
