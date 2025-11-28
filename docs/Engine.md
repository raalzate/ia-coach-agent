# ⚙️ AI Engine Documentation

Este módulo es responsable de la **carga, inicialización y gestión de memoria** de los modelos de Inteligencia Artificial. Utiliza el sistema de caché de Streamlit para asegurar que los modelos pesados se carguen solo una vez al iniciar la aplicación, y no con cada interacción del usuario.

## 📋 Descripción de Funciones

### 1. `load_grammar_engine()`
Carga el modelo especializado en Corrección de Errores Gramaticales (GEC).

* **Arquitectura:** T5 (Text-to-Text Transfer Transformer).
* **Modelo Específico:** `vennify/t5-base-grammar-correction`.
* **Biblioteca:** Hugging Face `transformers`.
* **Configuración Crítica:**
    * `use_fast=False`: Se fuerza el uso del tokenizador lento (basado en Python/SentencePiece) en lugar del rápido (Rust) para evitar problemas de compatibilidad conocidos en sistemas macOS con ciertas versiones de `transformers`.
* **Retorno:** Tupla `(tokenizer, model)`.

### 2. `load_chat_engine()`
Carga el Gran Modelo de Lenguaje (LLM) cuantizado para la conversación general.

* **Arquitectura:** Llama / Mistral (dependiendo del archivo `.gguf`).
* **Biblioteca:** `llama-cpp-python` (Binding de Python para `llama.cpp`).
* **Configuración Crítica:**
    * `n_ctx=4096`: Define la ventana de contexto (memoria a corto plazo de la conversación).
    * `n_gpu_layers=0`: Fuerza la ejecución en **CPU**. Esto garantiza estabilidad máxima y compatibilidad universal, evitando errores de VRAM o drivers de CUDA/Metal, aunque sacrifica velocidad de generación.
* **Retorno:** Instancia del objeto `Llama`.

---

## 🚀 Mecanismo de Caché (Performance)

El uso del decorador `@st.cache_resource` es fundamental para la experiencia de usuario.



**Sin caché:**
1. Usuario escribe "Hola".
2. Script se reinicia.
3. Carga modelo (5GB) -> Tarda 10 segundos.
4. Genera respuesta.

**Con caché (Implementado):**
1. Usuario escribe "Hola".
2. Script se reinicia.
3. Streamlit detecta que `load_chat_engine` ya se ejecutó.
4. Recupera el modelo de la RAM (0 segundos).
5. Genera respuesta.

---

# 📚 Referencias y Bibliografía Extensa

A continuación, se presenta una lista detallada de los modelos, arquitecturas y tecnologías base que componen este motor de IA.

## 1. Motor de Gramática (T5 & Vennify)

El corrector gramatical se basa en la arquitectura **Transformer Encoder-Decoder**.

* **Modelo Implementado:**
    * *Vennify T5 Base Grammar Correction*. (2021). Hugging Face Model Hub. Disponible en: [https://huggingface.co/vennify/t5-base-grammar-correction](https://huggingface.co/vennify/t5-base-grammar-correction). (Un fine-tune específico sobre el dataset C4_200M).

* **Arquitectura Base (T5):**
    * Raffel, C., et al. (2020). **"Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"**. *Journal of Machine Learning Research*. Esta es la publicación seminal que introdujo T5, proponiendo que cualquier tarea de NLP (traducción, resumen, corrección) puede plantearse como un problema de "texto a texto".
    * [Leer Paper en ArXiv](https://arxiv.org/abs/1910.10683)

* **Tecnología Subyacente:**
    * Vaswani, A., et al. (2017). **"Attention Is All You Need"**. *Advances in Neural Information Processing Systems*. El paper que inventó la arquitectura Transformer, base de T5 y GPT.
    * [Leer Paper en ArXiv](https://arxiv.org/abs/1706.03762)

## 2. Motor de Chat (Llama & GGUF)

El motor de chat utiliza modelos **Decoder-only** optimizados para ejecución local mediante cuantización.

* **Software de Inferencia:**
    * Gerganov, G. (2023). **llama.cpp**: Port of Facebook's LLaMA model in C/C++. Esta librería permite ejecutar LLMs en hardware de consumo (MacBooks, CPUs Intel) eficientemente.
    * Repositorio: [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)

* **Formato de Archivo (GGUF):**
    * **GGUF (GPT-Generated Unified Format)**. Introducido en agosto de 2023 por el equipo de `llama.cpp` para reemplazar a GGML. Es un formato binario optimizado para mapeo rápido en memoria y soporte de metadatos extensibles.

* **Arquitectura Base (Llama):**
    * **Llama 3 (2024):** AI at Meta. "The Llama 3 Herd of Models". El estado del arte actual en modelos abiertos.
        * [Leer Paper](https://ai.meta.com/research/publications/the-llama-3-herd-of-models/)
    * **Llama 2 (2023):** Touvron, H., et al. "Llama 2: Open Foundation and Fine-Tuned Chat Models".
        * [Leer Paper en ArXiv](https://arxiv.org/abs/2307.09288)
    * **Mistral 7B (Alternativa común):** Jiang, A., et al. (2023). "Mistral 7B". Introduce *Sliding Window Attention* para mayor eficiencia.
        * [Leer Paper en ArXiv](https://arxiv.org/abs/2310.06825)

## 3. Librerías de Python

* **Streamlit:**
    * Framework de código abierto para aplicaciones de Machine Learning. Su mecanismo de `st.session_state` y `st.cache_resource` maneja la reactividad de la aplicación.
    * Documentación: [https://docs.streamlit.io/](https://docs.streamlit.io/)

* **Hugging Face Transformers:**
    * Wolf, T., et al. (2020). **"Transformers: State-of-the-Art Natural Language Processing"**. EMNLP 2020.
    * [Leer Paper](https://www.aclweb.org/anthology/2020.emnlp-demos.6/)