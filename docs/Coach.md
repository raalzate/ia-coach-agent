# 🧠 Core Documentation: EnglishCoach

La clase `EnglishCoach` actúa como el cerebro de la aplicación. Gestiona el ciclo de vida del estudiante, desde la recopilación inicial de datos (Onboarding) hasta la progresión curricular y la generación de contexto para la IA.

## 📋 Descripción General

  * **Ubicación:** `core/coach.py`
  * **Responsabilidad:** Mantener el estado del usuario, gestionar la lógica de negocio y preparar las instrucciones para los modelos de IA.
  * **Persistencia:** Utiliza archivos JSON (`student_profile.json` y `student_progress.json`) para guardar datos entre sesiones.

-----

## 🔄 Sistema de Onboarding (Perfilamiento)

El sistema utiliza un enfoque secuencial definido en la constante `self.ONBOARDING_STEPS`. En lugar de código "harcodeado" con múltiples `if/else`, el sistema itera sobre una lista de configuración.

### Configuración del Flujo

El flujo de preguntas se define en el constructor `__init__`. Cada paso es un diccionario con:

  * `key`: La clave donde se guardará el dato en el JSON.
  * `q`: La pregunta que formulará la IA.

<!-- end list -->

```python
self.ONBOARDING_STEPS = [
    {"key": "name", "q": "What is your name?"},
    {"key": "goal", "q": "Why are you learning English?"},
    # ... más pasos
]
```

### Lógica de Auto-Aprendizaje (`auto_learn`)

El método `auto_learn(text)` es una máquina de estados que procesa la entrada del usuario.

1.  **Iteración:** Recorre `ONBOARDING_STEPS` en orden.
2.  **Detección de Vacío:** Encuentra el *primer* campo (`key`) que tenga valor `None` en el perfil.
3.  **Asignación:** Asume que el texto actual del usuario es la respuesta a esa pregunta específica.
4.  **Limpieza:** Aplica limpieza específica (ej: extraer solo números para `age`, o quitar "my name is" para `name`).
5.  **Guardado:** Actualiza el JSON y detiene el proceso (solo aprende un dato a la vez).

-----

## 📚 Referencia de Métodos

### `__init__(self)`

Inicializa el coach.

  * Carga el perfil y el progreso desde disco.
  * Valida que el perfil existente contenga todas las claves definidas en `ONBOARDING_STEPS` (útil si se agregan nuevas preguntas a futuro).

### `is_onboarding_complete(self) -> bool`

Verifica si el estudiante ha completado el perfil.

  * **Retorna:** `True` si *todas* las claves en `ONBOARDING_STEPS` tienen un valor asignado.

### `get_intro_message(self) -> str`

Determina qué decir al iniciar la aplicación.

  * **Si está en Onboarding:** Busca la primera pregunta sin responder en la lista y la devuelve.
  * **Si es Estudiante Activo:** Devuelve el mensaje de bienvenida con el nivel y tema actual (ej: "Welcome back\! Today's topic: Past Simple").

### `get_system_prompt(self) -> str`

Construye la instrucción maestra (System Prompt) para el LLM.

  * **Modo Onboarding:** Instruye a la IA para que actúe como encuestadora. "Tu objetivo es preguntar por {CAMPO\_FALTANTE}".
  * **Modo Profesor:** Inyecta todo el contexto del usuario en una sola cadena.
      * *Input Context:* Nombre, Objetivo, Edad, Hobbies, Películas, Viajes.
      * *Instruction:* "Usa el perfil del estudiante. Si le gustan las películas, usa ejemplos de cine para explicar el tema actual".

### `check_grammar(self, text, tokenizer, model) -> (bool, str)`

Ejecuta la corrección gramatical utilizando un modelo T5 externo.

  * **Parámetros:**
      * `text`: Input del usuario.
      * `tokenizer`: Tokenizador HuggingFace cargado.
      * `model`: Modelo T5 cargado.
  * **Retorna:** Una tupla `(es_correcto, texto_corregido)`.

### `advance(self)`

Maneja la progresión del currículum.

  * Incrementa el índice del tema actual.
  * Si se acaban los temas del nivel actual, busca el siguiente nivel en `config.CURRICULUM` y avanza automáticamente.

-----

## 💾 Estructura de Datos (JSON)

### `student_profile.json`

Se genera dinámicamente basado en los pasos de onboarding.

```json
{
  "name": "Raul",
  "goal": "Work",
  "age": "30",
  "education": "Engineer",
  "hobbies": "Coding, Hiking",
  "movies": "Sci-Fi",
  "travel": "Japan",
  "facts": []
}
```

### `student_progress.json`

Controla la posición en el plan de estudios.

```json
{
  "current_level": "Level 1 (A1: Beginner)",
  "current_topic_index": 2
}
```

-----

## 🚀 Guía de Extensión

**¿Cómo agregar una nueva pregunta al onboarding?**

Simplemente añade un nuevo diccionario a la lista `self.ONBOARDING_STEPS` en el método `__init__`.

*Ejemplo: Preguntar por comida favorita*

```python
# En __init__
self.ONBOARDING_STEPS = [
    # ... pasos anteriores ...
    {"key": "travel", "q": "..."}, 
    {"key": "food", "q": "Yummy! What is your favorite food?"} # <--- Nuevo paso al final
]
```

  * No necesitas tocar `auto_learn` ni `get_intro_message`.
  * El sistema detectará la nueva clave, actualizará el JSON automáticamente y hará la pregunta al final del flujo.