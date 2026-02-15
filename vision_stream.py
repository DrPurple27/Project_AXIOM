import cv2
import ollama
import time

class AxiomVision:
    def __init__(self, interval=5):
        self.interval = interval
        self.last_description = "Aguardando primeira análise..."
        self.running = True
        self.cap = cv2.VideoCapture(0)

    def analyze_frame(self, frame):
        # Salva o frame atual para análise
        cv2.imwrite("current_view.jpg", frame)
        try:
            with open("current_view.jpg", "rb") as f:
                # Mudamos para o modelo LLaVA que é mais robusto
                response = ollama.generate(
                    model='llava:7b', 
                    prompt='O que você vê nesta imagem? Descreva de forma curta e clara.',
                    images=[f.read()]
                )
            return response['response']
        except Exception as e:
            return f"Erro na visão: {e}"

    def vision_loop(self):
        print("\n[OLHOS DO AXIOM ATIVOS - Pressione Ctrl+C para parar]")
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.last_description = self.analyze_frame(frame)
                print(f"\n[AXIOM VIU]: {self.last_description}")
            
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.cap.release()

if __name__ == "__main__":
    vision = AxiomVision(interval=5)
    try:
        vision.vision_loop()
    except KeyboardInterrupt:
        vision.stop()
        print("\n[Visão encerrada]")
