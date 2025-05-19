📌 Visão Geral
O projeto detecta LEDs quebrados ou defeituosos em faróis automotivos, comparando imagens capturadas com uma "golden sample" (imagem de referência) e analisando componentes individuais.

✨ Funcionalidades
✔ Captura de imagens via câmera
✔ Comparação com golden sample
✔ Detecção de LEDs defeituosos
✔ Classificação automática (Aprovado/Rejeitado)
✔ Geração de logs e relatórios
✔ Interface gráfica amigável

🛠️ Tecnologias Utilizadas
Python (Linguagem principal)

OpenCV (Processamento de imagens)

Tkinter (Interface gráfica)

Pillow (PIL) (Manipulação de imagens)

scikit-image (Análise de similaridade)

📂 Estrutura do Projeto
/leds_conectores/
├── /detector_de_led_quebrado/
│   ├── /scr/                  # Código-fonte
│   │   ├── main.py            # Interface principal
│   │   ├── inspection.py      # Lógica de inspeção
│   │   ├── camera_interface.py # Controle da câmera
│   │   └── hardware_control.py # Controle de hardware (CLP/atuadores)
│   │
│   ├── /config/               # Configurações
│   │   ├── config.json        # Parâmetros do sistema
│   │   └── camera_settings.json # Config da câmera
│   │
│   ├── /reference/            # Imagens de referência
│   │   ├── golden_sample.png  # Modelo "perfeito"
│   │   └── /component_templates/ # Templates de LEDs
│   │
│   ├── /captures/             # Imagens capturadas
│   │   ├── /approved/         # LEDs aprovados
│   │   └── /rejected/         # LEDs rejeitados
│   │
│   ├── /logs/                 # Registros de inspeção
│   └── requirements.txt       # Dependências
│
└── README.md                  # Este arquivo
⚙️ Configuração
Pré-requisitos
Python 3.8+

Câmera conectada (ou webcam)

Ambiente bem iluminado
