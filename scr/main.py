import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from inspection import LEDInspector
from camera_interface import CameraController
import os
import json
from datetime import datetime

class LEDInspectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de LEDs Quebrados")
        
        # Configurações
        self.load_config()
        self.setup_ui()
        self.setup_camera()
        
        # Variáveis de estado
        self.operator = ""
        self.last_result = None
    
    def load_config(self):
        try:
            with open('../config/config.json') as f:
                self.config = json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar configurações: {str(e)}")
            self.config = {"threshold": 0.9}
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualização da câmera
        self.camera_frame = ttk.LabelFrame(main_frame, text="Visualização")
        self.camera_frame.pack(fill=tk.BOTH, expand=True)
        
        self.video_label = ttk.Label(self.camera_frame)
        self.video_label.pack()
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Operador:").pack(side=tk.LEFT)
        self.operator_entry = ttk.Entry(control_frame)
        self.operator_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Capturar", command=self.capture).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Inspecionar", command=self.inspect).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        self.result_frame = ttk.LabelFrame(main_frame, text="Resultado")
        self.result_frame.pack(fill=tk.X)
        
        self.result_label = ttk.Label(self.result_frame, text="Aguardando inspeção...", font=('Arial', 14))
        self.result_label.pack(pady=10)
        
        self.details_label = ttk.Label(self.result_frame, text="")
        self.details_label.pack()
    
    def setup_camera(self):
        self.camera = CameraController()
        self.camera.initialize()
        self.update_camera_view()
    
    def update_camera_view(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img.thumbnail((800, 600))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(50, self.update_camera_view)
    
    def capture(self):
        self.operator = self.operator_entry.get()
        if not self.operator:
            messagebox.showwarning("Aviso", "Informe o nome do operador")
            return
        
        self.current_frame = self.camera.capture()
        if self.current_frame is not None:
            messagebox.showinfo("Sucesso", "Imagem capturada com sucesso!")
    
    def inspect(self):
        if not hasattr(self, 'current_frame'):
            messagebox.showwarning("Aviso", "Capture uma imagem primeiro")
            return
        
        inspector = LEDInspector()
        result = inspector.inspect(self.current_frame)
        self.last_result = result
        
        if result['approved']:
            self.result_label.config(text="APROVADO", foreground="green")
            save_path = "../captures/approved/"
        else:
            self.result_label.config(text="REJEITADO", foreground="red")
            save_path = "../captures/rejected/"
        
        # Salvar imagem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_path}led_{timestamp}.png"
        cv2.imwrite(filename, self.current_frame)
        
        # Mostrar detalhes
        details = f"Operador: {self.operator}\n"
        details += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        details += f"Similaridade: {result['similarity']:.2%}\n"
        details += f"Defeitos: {', '.join(result['defects']) if result['defects'] else 'Nenhum'}"
        self.details_label.config(text=details)
        
        # Log
        self.log_inspection(result, filename)
    
    def log_inspection(self, result, filename):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operator": self.operator,
            "result": "approved" if result['approved'] else "rejected",
            "similarity": result['similarity'],
            "defects": result['defects'],
            "image_path": filename
        }
        
        os.makedirs("../logs", exist_ok=True)
        log_file = f"../logs/inspection_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDInspectionApp(root)
    root.mainloop()class LEDInspectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de LEDs Quebrados")
        
        # Configurações
        self.load_config()
        self.setup_ui()
        self.setup_camera()
        
        # Variáveis de estado
        self.operator = ""
        self.last_result = None
        self.current_frame = None
    
    def load_config(self):
        try:
            with open('../config/config.json') as f:
                self.config = json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar configurações: {str(e)}")
            self.config = {"threshold": 0.9}
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualização da câmera
        self.camera_frame = ttk.LabelFrame(main_frame, text="Visualização")
        self.camera_frame.pack(fill=tk.BOTH, expand=True)
        
        self.video_label = ttk.Label(self.camera_frame)
        self.video_label.pack()
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Operador:").pack(side=tk.LEFT)
        self.operator_entry = ttk.Entry(control_frame)
        self.operator_entry.pack(side=tk.LEFT, padx=5)
        
        self.capture_button = ttk.Button(control_frame, text="Capturar", command=self.capture)
        self.capture_button.pack(side=tk.LEFT, padx=5)
        
        self.inspect_button = ttk.Button(control_frame, text="Inspecionar", command=self.inspect)
        self.inspect_button.pack(side=tk.LEFT, padx=5)
        
        # Resultados
        self.result_frame = ttk.LabelFrame(main_frame, text="Resultado")
        self.result_frame.pack(fill=tk.X)
        
        self.result_label = ttk.Label(self.result_frame, text="Aguardando inspeção...", font=('Arial', 14))
        self.result_label.pack(pady=10)
        
        self.details_label = ttk.Label(self.result_frame, text="")
        self.details_label.pack()
    
    def setup_camera(self):
        self.camera = CameraController()
        self.camera.initialize()
        self.update_camera_view()
    
    def update_camera_view(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img.thumbnail((800, 600))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(50, self.update_camera_view)
    
    def capture(self):
        self.operator = self.operator_entry.get()
        if not self.operator:
            messagebox.showwarning("Aviso", "Informe o nome do operador")
            return
        
        self.current_frame = self.camera.capture()
        if self.current_frame is not None:
            messagebox.showinfo("Sucesso", "Imagem capturada com sucesso!")
            self.capture_button.config(state="disabled")
            self.inspect_button.config(state="normal")
    
    def inspect(self):
        if self.current_frame is None:
            messagebox.showwarning("Aviso", "Capture uma imagem primeiro")
            return
        
        inspector = LEDInspector()
        result = inspector.inspect(self.current_frame)
        self.last_result = result
        
        if result['approved']:
            self.result_label.config(text="APROVADO", foreground="green")
            save_path = "../captures/approved/"
        else:
            self.result_label.config(text="REJEITADO", foreground="red")
            save_path = "../captures/rejected/"
        
        # Salvar imagem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_path}led_{timestamp}.png"
        cv2.imwrite(filename, self.current_frame)
        
        # Mostrar detalhes
        details = f"Operador: {self.operator}\n"
        details += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        details += f"Similaridade: {result['similarity']:.2%}\n"
        details += f"Defeitos: {', '.join(result['defects']) if result['defects'] else 'Nenhum'}"
        self.details_label.config(text=details)
        
        # Log
        self.log_inspection(result, filename)
        self.inspect_button.config(state="disabled")
        self.capture_button.config(state="normal")
    
    def log_inspection(self, result, filename):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operator": self.operator,
            "result": "approved" if result['approved'] else "rejected",
            "similarity": result['similarity'],
            "defects": result['defects'],
            "image_path": filename
        }
        
        os.makedirs("../logs", exist_ok=True)
        log_file = f"../logs/inspection_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")