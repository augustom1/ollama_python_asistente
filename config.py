from dotenv import load_dotenv
import os

load_dotenv()

# Host de Ollama (por defecto el local)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Modelo pensado para código Python (puedes cambiarlo si quieres otro)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")

# Archivo .md con los códigos/apuntes del profesor
TEACHER_CONTEXT_PATH = os.getenv("TEACHER_CONTEXT_PATH", "python_context.md")

# Opciones del modelo (baja temperatura para respuestas más simples y estables)
MAX_OUTPUT_TOKENS = 300

OLLAMA_OPTIONS = {
    "temperature": 0.1,
    "top_k": 40,
    "top_p": 0.9,
    "num_predict": MAX_OUTPUT_TOKENS,
}
