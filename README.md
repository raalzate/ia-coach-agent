

# 🎓 Coach Agent

**Coach Agent** es un tutor de inglés inteligente e interactivo construido con **Python** y **Streamlit**. Utiliza Modelos de Lenguaje Locales (LLMs) para mantener conversaciones naturales, corregir gramática en tiempo real y adaptar el currículum (A1-C2) basándose en los intereses y objetivos del estudiante.

-----

## ✨ Características Principales

  * **🧠 IA Local y Privada:** Ejecuta modelos LLM (Llama/Mistral) y corrección gramatical (T5) localmente. ¡No requiere API keys de pago\!
  * **🗣️ Conversación Natural:** Chat fluido con memoria de contexto.
  * **🔧 Corrector Gramatical en Tiempo Real:** Detecta errores antes de que la IA responda y sugiere correcciones amigables.
  * **📈 Sistema de Progreso Dinámico:** Currículum alineado al MCER (A1 a C2) que avanza automáticamente cuando el estudiante domina un tema.
  * **🎧 Experiencia Auditiva (TTS):** Reproducción automática de audio para practicar *listening* y pronunciación.
  * **👤 Perfil Inteligente (Auto-Learn):** El sistema aprende tu nombre, hobbies y objetivos a través de la conversación natural ("Onboarding Invisible").
  * **🎨 UI/UX Moderna:** Interfaz limpia con feedback visual no intrusivo (`toasts`), modo oscuro y métricas de progreso.

-----

## 📂 Estructura del Proyecto

```text
ai-coach/
├── main.py                  # 🚀 Punto de entrada (Interfaz Streamlit)
├── config.py                # ⚙️ Configuración (Curriculum, Títulos)
├── requirements.txt         # 📦 Dependencias de Python
├── models/                  # 🧠 Carpeta para modelos (.gguf, .bin)
│   ├── chat_model.gguf      # Modelo principal (Llama-3/Mistral) Debe descargarse
├── core/
│   ├── coach.py             # 🧠 Lógica pedagógica (Estado, Onboarding, Reglas)
│   └── engine.py            # ⚙️ Carga de modelos (Torch, LlamaCPP)
├── utils/
│   ├── audio.py             # 🎧 Generación y renderizado de audio (TTS)
│   └── data.py              # 💾 Manejo de JSON (Guardar/Cargar)
├── data/ (Auto-generado)
│   ├── student_profile.json # Datos del usuario
│   └── student_progress.json# Progreso del curso
└── docs/                    # 📄 Documentación adicional
```

-----

## 🚀 Instalación y Uso

### 1\. Requisitos Previos

  * Python 3.10+
  * RAM recomendada: 8GB+ (para ejecutar modelos cuantizados).

### 2\. Instalación

Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/raalzate/ia-coach-agent.git
cd ia-coach-agent
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3\. Configuración de Modelos

Debes descargar los modelos y colocarlos en la carpeta `models/`:

1.  **Chat Model:** Descarga un modelo `.gguf` (ej. *Llama-3-8B-Instruct-Q4\_K\_M.gguf*) y guárdalo en `models/`.
2.  **Grammar Model:** Descarga *vennify/t5-base-grammar-correction* (o similar) desde HuggingFace.

### 4\. Ejecución

```bash
streamlit run main.py
```

-----

## 🧠 Arquitectura Técnica

### Flujo de Interacción (The Interaction Loop)

1.  **Input:** El usuario escribe en el chat.
2.  **Interceptor:**
      * Comandos (`/learn`): Ejecuta acciones de sistema.
      * Auto-Learn: Extrae entidades (Nombre, Edad, Hobbies) silenciosamente.
3.  **Grammar Guardrail (T5):**
      * El input pasa por un modelo T5 especializado.
      * Si hay error -\> Se muestra una alerta suave (Toast + Warning) y se pide reintentar.
      * Si es correcto -\> Pasa al LLM.
4.  **Coach Brain (LLM):**
      * Recibe un *System Prompt* dinámico inyectado con el perfil del usuario y el tema actual.
      * Genera respuesta vía *Streaming* (token a token).
5.  **Audio (TTS):**
      * Se genera audio en segundo plano.
      * Se reproduce con un `autoplay` invisible para fluidez inmediata.

### Gestión de Estado (Session State)

El sistema utiliza persistencia híbrida:

  * **Session State (RAM):** Para el historial de chat inmediato y objetos de modelos cargados.
  * **JSON (Disco):** Para persistencia a largo plazo (Progreso del estudiante y Perfil).

-----

## ⚙️ Personalización (Config.py)

Puedes ajustar el plan de estudios en `config.py`. El sistema se adapta automáticamente a nuevos niveles.

```python
CURRICULUM = {
    "Level 1 (Beginner)": [
        "Present Simple", 
        "Verb To Be",
        "Family & Hobbies"
    ],
    "Level 2 (Elementary)": [
        "Past Simple",
        "Future Plans"
    ]
    # ... Agrega niveles libremente
}
```

-----

## 🎨 Guía de Estilos UI/UX

La interfaz utiliza hacks de CSS inyectados para mejorar la experiencia nativa de Streamlit:

  * **Toasts (`st.toast`):** Usados para notificaciones de éxito ("Memory Updated") o avisos rápidos ("Checking grammar...").
  * **Avatares:**
      * 👩‍🏫 **Emma (Coach):** Guía principal.
      * 🧐 **Corrector:** Aparece solo cuando hay errores gramaticales.
  * **Sidebar:** Actúa como el "Cuaderno del Estudiante", mostrando métricas claras y barra de progreso verde (`#4CAF50`).

-----

# 📥 Guía de Descarga Manual: Modelo Llama 3 (GGUF)

Esta guía explica cómo obtener el archivo `.gguf` necesario para ejecutar el **AI English Coach**. Estamos buscando específicamente la versión `Q4_K_M` (4-bit Medium Quantization), que ofrece el mejor equilibrio entre velocidad, uso de memoria (aprox. 5-6 GB de RAM) e inteligencia.

## 📋 Información del Archivo

  * **Modelo Base:** Meta Llama 3 8B Instruct.
  * **Formato:** GGUF (Optimizado para CPU/Apple Silicon).
  * **Cuantización:** `Q4_K_M` (Recomendado).
  * **Tamaño:** Aproximadamente **4.9 GB**.
  * **Fuente:** Hugging Face (Repositorios de la comunidad como *Bartowski* o *MaziyarPanahi*).

-----

## 🚀 Opción 1: Descarga Directa desde el Navegador (Más Fácil)

Esta es la forma más sencilla si estás en tu ordenador personal.

1.  **Ir al Repositorio:**
    El modelo con las correcciones de tokenizador más estables actualmente es mantenido por **Bartowski**. Accede al siguiente enlace:
    🔗 **[Bartowski / Meta-Llama-3-8B-Instruct-GGUF en Hugging Face](https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/tree/main)**

2.  **Localizar el Archivo:**
    En la lista de archivos, busca el siguiente nombre (o uno muy similar):
    `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf`

    > **Nota:** Es posible que el nombre exacto y largo (`...correct-pre-tokenizer...`) haya sido simplificado en las versiones más nuevas porque la corrección ya es estándar. El archivo `Q4_K_M.gguf` de Bartowski ya incluye estas correcciones.

3.  **Descargar:**
    Haz clic en el icono de descarga (⬇️) situado a la derecha del nombre del archivo.

4.  **Ubicación en el Proyecto:**
    Una vez descargado, mueve el archivo a la carpeta `models/` dentro de tu proyecto.

    ```text
    ai-coach/
    ├── main.py
    ├── models/
    │   └── Meta-Llama-3-8B-Instruct-Q4_K_M.gguf  <-- ¡AQUÍ!
    ```

-----

## 💻 Opción 2: Descarga vía Terminal (Recomendado para Servidores)

Si estás en un entorno Linux/Mac o prefieres la terminal, usa `wget` para descargar el archivo directamente a la carpeta correcta.

1.  **Navega a la carpeta de modelos:**

    ```bash
    cd ruta/a/tu/proyecto/ai-coach
    mkdir -p models
    cd models
    ```

2.  **Ejecuta el comando de descarga:**
    Este enlace descarga la versión `Q4_K_M` del repositorio de Bartowski:

    ```bash
    wget https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
    ```

    *Si no tienes `wget`, puedes usar `curl`:*

    ```bash
    curl -L -O https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
    ```

-----

## ⚙️ Configuración Final

Una vez tengas el archivo descargado, debes asegurarte de que tu archivo `config.py` apunte al nombre correcto.

1.  Abre `config.py`.
2.  Busca la variable `MODEL_PATH`.
3.  Actualízala con el nombre exacto del archivo que descargaste.

<!-- end list -->

```python
# config.py
import os

# Asegúrate de que coincida con el nombre del archivo descargado
MODEL_NAME = "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", MODEL_NAME)
```

-----

## 📚 Referencias Técnicas del Modelo

### ¿Por qué este modelo específico?

1.  **Meta Llama 3:**

      * *AI at Meta (2024).* Lanzado en abril de 2024, Llama 3 superó a muchos modelos de código abierto anteriores en capacidades de razonamiento y seguimiento de instrucciones.
      * [Blog Oficial de Meta Llama 3](https://ai.meta.com/blog/meta-llama-3/)

2.  **El problema del "Correct Pre-tokenizer & EOS":**

      * Cuando Llama 3 salió, hubo un problema con cómo los archivos GGUF manejaban el token de "Fin de Secuencia" (EOS) y el tokenizador previo. Esto causaba que el modelo a veces no dejara de hablar o generara texto basura al final.
      * Los repositorios modernos (como Bartowski o QuantFactory) ya han parcheado esto. La referencia que tenías en el nombre del archivo alude a este parche crítico.

3.  **Formato GGUF & Quantization (Q4\_K\_M):**

      * **GGUF:** Es el formato estándar actual para inferencia en CPU con `llama.cpp`. Permite mapeo de memoria eficiente (mmap), lo que significa que el modelo carga casi al instante.
      * **Q4\_K\_M:** Utiliza el método de "k-quants". Reduce la precisión de los pesos de 16 bits a 4 bits.
          * *Dettmers, T., et al. (2022).* "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale". (Base teórica de la cuantización).
          * La pérdida de "inteligencia" (perplejidad) en Q4\_K\_M es insignificante comparada con la ganancia de velocidad y reducción de RAM (de 16GB a 5GB).

## 🤝 Contribución

1.  Haz un Fork del proyecto.
2.  Crea tu rama de funcionalidad (`git checkout -b feature/AmazingFeature`).
3.  Haz Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Push a la rama (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.

-----

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo `LICENSE.md` para detalles.