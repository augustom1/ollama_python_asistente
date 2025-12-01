from pathlib import Path
import time

import config
from query_generator import PythonAssistant

# Máximo de caracteres del contexto del profesor para no hacer el prompt gigante
MAX_CONTEXT_CHARS = 8000  # si sigue lento, bajá a 4000 o 2000


def load_teacher_context(path: str) -> str:
    """
    Lee el archivo .md con los códigos/apuntes del profesor y lo recorta
    a un máximo de caracteres para que el prompt no se vuelva enorme.
    """
    p = Path(path)
    if not p.exists():
        return ""
    try:
        txt = p.read_text(encoding="utf-8").strip()
    except Exception:
        return ""

    if len(txt) > MAX_CONTEXT_CHARS:
        # Nos quedamos con el final, que suele tener lo más reciente/relevante
        txt = txt[-MAX_CONTEXT_CHARS:]

    return txt


def is_theory_question(text: str) -> bool:
    """
    Heurística sencilla para detectar si la pregunta es teórica.
    Si es teoría → el modelo puede explicar.
    Si no → solo código.
    """
    t = text.lower()

    theory_keywords = [
        "explica",
        "explícame",
        "explicame",
        "qué es",
        "que es",
        "definí",
        "definime",
        "teoría",
        "concepto",
        "diferencia entre",
        "para que sirve",
        "para qué sirve",
        "como funciona",
        "cómo funciona",
        "qué hace este código",
        "que hace este codigo",
    ]

    return any(kw in t for kw in theory_keywords)


def build_prompt(teacher_context: str, question: str, mode: str) -> str:
    """
    Construye el prompt que se envía al modelo.
    """
    parts: list[str] = []

    if teacher_context:
        parts.append(
            "Estos son apuntes y códigos de referencia del profesor, en formato Markdown.\n"
            "Úsalos solo como guía de estilo y nivel de dificultad. No copies todo literal.\n\n"
            "=== APUNTES DEL PROFESOR (INICIO) ===\n"
        )
        parts.append(teacher_context)
        parts.append("\n=== APUNTES DEL PROFESOR (FIN) ===\n\n")

    parts.append(
        "Contexto del alumno: está preparando un EXAMEN de programación en Python.\n"
        "Sigue el estilo de los ejemplos del profesor: código claro, directo y sencillo.\n\n"
    )

    if mode == "code":
        parts.append(
            "La siguiente petición del alumno requiere SOLO CÓDIGO PYTHON.\n"
            "No debes escribir explicaciones ni texto adicional, solo el código final.\n\n"
        )
    else:
        parts.append(
            "La siguiente petición del alumno es de TEORÍA o explicación.\n"
            "Puedes explicar brevemente en español neutro y, si ayuda, agregar ejemplos de código.\n\n"
        )

    parts.append("Pregunta / pedido del alumno:\n")
    parts.append(question.strip())

    return "".join(parts)


def main() -> None:
    print("=== Asistente de PYTHON para examen ===\n")
    print("Este asistente usa los códigos del profesor como referencia.\n")
    print("Modo de respuesta:")
    print("  - Pregunta normal (ej: 'haceme una función que...') → SOLO código Python.")
    print("  - Pregunta teórica (ej: 'explicame qué es un while') → explicación breve.\n")
    print("Comandos especiales:")
    print("  '!rapido ...' → NO usa el contexto del profesor (más rápido).")
    print("  'salir'       → terminar el programa.\n")

    teacher_context = load_teacher_context(config.TEACHER_CONTEXT_PATH)
    if teacher_context:
        print(f"Contexto del profesor cargado desde: {config.TEACHER_CONTEXT_PATH}\n")
    else:
        print(
            f"ADVERTENCIA: No se encontró '{config.TEACHER_CONTEXT_PATH}' "
            "o está vacío. El asistente funcionará sin ejemplos del profesor.\n"
        )

    assistant = PythonAssistant(
        host=config.OLLAMA_HOST,
        model=config.OLLAMA_MODEL,
        options=config.OLLAMA_OPTIONS,
    )

    while True:
        question = input("Tú: ").strip()
        if not question:
            continue

        if question.lower() in ("salir", "exit", "quit"):
            print("¡Éxitos en el examen! 👋")
            break

        # Modo rápido: no incluimos el contexto del profesor
        use_context = True
        if question.startswith("!rapido "):
            use_context = False
            question = question[len("!rapido "):].strip()

        mode = "theory" if is_theory_question(question) else "code"
        current_context = teacher_context if use_context else ""

        full_prompt = build_prompt(current_context, question, mode)

        start = time.time()
        response = assistant.generate_response(full_prompt, mode=mode)
        elapsed = time.time() - start

        print("\n--- Respuesta ---\n")
        print(response)
        print(f"\n--- Tiempo de respuesta: {elapsed:.2f} segundos ---\n")


if __name__ == "__main__":
    main()
