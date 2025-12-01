from __future__ import annotations

import re
from typing import Any, Dict, Optional

import ollama


def _extract_content_from_ollama(result: Any) -> str:
    """
    Extrae el texto de la respuesta de Ollama, manejando distintos formatos.
    """

    # 1) dict (formato oficial)
    if isinstance(result, dict):
        msg = result.get("message", {})
        if isinstance(msg, dict):
            content = msg.get("content")
            if isinstance(content, str):
                return content

    # 2) objeto con .message.content
    try:
        msg = getattr(result, "message", None)
        if msg is not None:
            content = getattr(msg, "content", None)
            if isinstance(content, str):
                return content
    except Exception:
        pass

    # 3) si es string, devolverlo tal cual
    if isinstance(result, str):
        return result

    # 4) fallback: parsear repr con content="..."; (por si acaso)
    text = str(result)
    m = re.search(r'content="(.*)"', text, flags=re.DOTALL)
    if m:
        captured = m.group(1)
        captured = re.split(r'";\s*\w+=', captured)[0]
        return captured

    return text


class PythonAssistant:
    """
    Asistente para EXAMEN DE PYTHON.

    Modos:
      - mode="code": solo devolver CÓDIGO PYTHON (sin explicaciones).
      - mode="theory": explicar teoría y, si hace falta, incluir ejemplos de código.
    """

    def __init__(
        self,
        host: str,
        model: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.host = host
        self.model = model
        self.options = options or {}
        self.client = ollama.Client(host=self.host)

    def _system_prompt(self, mode: str) -> str:
        base = [
            "Eres un profesor de programación en Python.",
            "Tu estilo es sencillo y claro, parecido al de un docente humano.",
            "Respondes SIEMPRE en español neutro.",
            "Sigue el estilo de los códigos de referencia del profesor.",
            "Evita explicaciones largas, tecnicismos innecesarios y frases típicas de IA.",
        ]

        if mode == "code":
            base.append(
                "El alumno solo quiere el CÓDIGO PYTHON final. "
                "No expliques nada, no agregues texto antes ni después. "
                "No pongas comentarios extensos. "
                "Responde solo con el contenido de un bloque de código Python."
            )
        else:  # theory
            base.append(
                "El alumno ahora pidió una explicación TEÓRICA. "
                "Puedes explicar brevemente y, si ayuda, incluir ejemplos en un bloque "
                "de código Python. Aun así, mantén las respuestas cortas y simples."
            )

        return " ".join(base)

    def _post_process_code_only(self, text: str) -> str:
        """
        En modo 'code', nos quedamos solo con el contenido del bloque ```python``` si existe.
        Si no hay bloque, devolvemos todo el texto como está.
        """

        # Buscar bloque ```python ... ```
        code_block = re.search(
            r"```python(.*?)```", text, flags=re.DOTALL | re.IGNORECASE
        )
        if code_block:
            code = code_block.group(1)
        else:
            # Buscar cualquier bloque ``` ... ```
            generic_block = re.search(r"```(.*?)```", text, flags=re.DOTALL)
            if generic_block:
                code = generic_block.group(1)
            else:
                code = text

        # Limpiar espacios iniciales/finales
        return code.strip("\n\r ")

    def generate_response(self, full_prompt: str, mode: str = "code") -> str:
        """
        full_prompt: prompt ya construido por main.py (contexto + pregunta).
        mode: 'code' o 'theory'.
        """
        system_prompt = self._system_prompt(mode)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
        ]

        result = self.client.chat(
            model=self.model,
            messages=messages,
            options=self.options,
        )

        raw_text = _extract_content_from_ollama(result).strip()

        if mode == "code":
            return self._post_process_code_only(raw_text)
        return raw_text
