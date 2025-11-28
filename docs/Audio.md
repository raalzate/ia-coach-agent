# 🎧 Audio System Documentation

Este módulo maneja la conversión de Texto a Voz (TTS) y la reproducción de audio en la interfaz web. Utiliza la biblioteca `edge-tts` para acceder a las voces neuronales de alta calidad de Microsoft sin necesidad de claves de API (aprovechando la API pública del navegador Edge).

## 📋 Descripción General del Módulo

  * **Archivo:** `utils/audio.py`
  * **Tecnología Principal:** `edge-tts` (Python wrapper para Microsoft Edge Read Aloud API).
  * **Voz Seleccionada:** `en-US-AriaNeural` (Voz femenina, acento americano estándar, optimizada para claridad pedagógica).
  * **Estrategia de Renderizado:** Incrustación directa en HTML5 mediante codificación Base64 (Data URI Scheme).

-----

## 🛠 Especificación de Funciones

### 1\. `_gen_audio_bytes(text)`

**Tipo:** Corrutina Asíncrona (`async def`).

Función interna que se comunica con el servicio remoto de TTS.

  * **Entrada:** Texto crudo (str).
  * **Proceso:**
    1.  Instancia un objeto `Communicate` con la voz `en-US-AriaNeural`.
    2.  Guarda el stream de audio en un archivo temporal (`temp_audio_buffer.mp3`).
    3.  Lee el archivo en modo binario (`rb`).
  * **Salida:** Bytes del archivo MP3.
  * **Nota Técnica:** Se utiliza un archivo intermedio en disco para garantizar la integridad del stream antes de cargarlo en memoria.

### 2\. `get_audio_bytes(text)`

**Tipo:** Función Síncrona (Wrapper).

Actúa como puente entre el entorno síncrono de Streamlit y el entorno asíncrono de `edge-tts`.

  * **Sanitización de Texto:**
      * Elimina etiquetas de control del sistema como `[PASSED]`.
      * Elimina caracteres Markdown (`*`, `#`) que no deben ser pronunciados (evita que la IA diga "asterisk").
  * **Gestión del Event Loop:**
      * Crea un nuevo bucle de eventos (`asyncio.new_event_loop()`) para cada llamada.
      * Esto es crucial porque Streamlit se ejecuta en su propio hilo y a menudo entra en conflicto con el bucle principal de asyncio si se intenta reutilizar.
  * **Manejo de Errores:** Captura excepciones de red o de codificación y retorna `None` para evitar romper la UI.

### 3\. `render_audio_player(audio_bytes, autoplay=False)`

**Tipo:** Componente UI.

Genera un reproductor de audio HTML5 y lo inyecta en el DOM de Streamlit.

  * **Codificación:** Convierte los bytes binarios a una cadena Base64.
  * **Construcción HTML:**
      * Crea una etiqueta `<audio controls>`.
      * Usa el esquema Data URI: `src="data:audio/mp3;base64,..."`. Esto hace que el audio sea parte del documento HTML, eliminando la necesidad de servir archivos estáticos desde un backend.
  * **Autoplay:** Si es `True`, inyecta el atributo `autoplay`, forzando al navegador a reproducir el audio inmediatamente (sujeto a las políticas de interacción del navegador).

-----

## 🧠 Arquitectura de Flujo de Audio

1.  **Input:** Texto del LLM ("Hello *student*\!").
2.  **Cleaner:** "Hello student\!" (Regex/Replace).
3.  **Async Loop:** Python abre un hilo asíncrono.
4.  **Edge API:** Envío de solicitud WebSocket a los servidores de Microsoft.
5.  **MP3 Stream:** Recepción de paquetes de audio.
6.  **Base64:** `b'\xff\xf3...'` -\> `"//uQZAAAA..."`.
7.  **Browser:** Decodificación del string Base64 y reproducción nativa.

-----

# 📚 Referencias Bibliográficas y Técnicas (Extendidas)

A continuación, se presenta una lista exhaustiva de las tecnologías subyacentes, los modelos teóricos de síntesis de voz y las bibliotecas utilizadas.

## 1\. Tecnología TTS (Text-to-Speech)

El motor utilizado (`en-US-AriaNeural`) pertenece a la familia de modelos **Neural TTS** de Microsoft. A diferencia del TTS cóncatenativo tradicional (pegar trozos de sonidos grabados), el Neural TTS utiliza redes neuronales profundas para sintetizar ondas de sonido desde cero.

  * **Arquitectura Base (Tacotron 2 & WaveNet):**

      * *Shen, J., et al. (2018).* **"Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Prediction"**. (Google AI). Este paper estableció el estándar moderno: una red recurrente (seq2seq) predice espectrogramas de Mel a partir de texto, y un vocoder (WaveNet) genera el audio.
      * [Leer Paper en ArXiv](https://arxiv.org/abs/1712.05884)

  * **Vocoders Rápidos (Parallel WaveGAN / HiFi-GAN):**

      * Para lograr la latencia casi instantánea que usa Edge, se suelen utilizar arquitecturas no auto-regresivas.
      * *Yamamoto, R., et al. (2020).* **"Parallel WaveGAN: A Fast Waveform Generation Model Based on Generative Adversarial Networks"**.
      * [Leer Paper en ArXiv](https://arxiv.org/abs/1910.11480)

  * **Microsoft Neural TTS:**

      * *Tan, X., et al. (2021).* **"A Survey on Neural Speech Synthesis"**. Microsoft Research Asia. Detalla la evolución de los modelos usados en Azure/Edge.
      * [Microsoft Research Blog: Neural TTS](https://www.google.com/search?q=https://www.microsoft.com/en-us/research/blog/neural-text-to-speech-extends-support-to-15-more-languages-with-state-of-the-art-ai-quality/)

## 2\. Bibliotecas y Protocolos

  * **Edge-TTS (Librería Python):**

      * Proyecto Open Source que realiza ingeniería inversa del protocolo WebSocket utilizado por la función "Read Aloud" de Microsoft Edge.
      * Repositorio Oficial: [https://github.com/rany2/edge-tts](https://github.com/rany2/edge-tts)
      * *Nota:* Utiliza el formato de servicio `wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud`.

  * **Asyncio (Python Concurrency):**

      * Biblioteca estándar de Python para escribir código concurrente usando la sintaxis `async/await`. Es fundamental aquí porque las operaciones de red (hablar con la API de Microsoft) son bloqueantes; `asyncio` permite gestionarlas eficientemente.
      * Documentación: [Python 3 Asyncio](https://docs.python.org/3/library/asyncio.html)

  * **Data URI Scheme (RFC 2397):**

      * Estándar de IETF que permite la inclusión de pequeños elementos de datos en línea, como si fueran referenciados externamente. Usamos esto para incrustar el MP3 directamente en el HTML de Streamlit.
      * Referencia: [RFC 2397 - The "data" URL scheme](https://datatracker.ietf.org/doc/html/rfc2397)

  * **Streamlit `unsafe_allow_html`:**

      * Mecanismo que permite inyectar HTML/JS arbitrario en la aplicación. Aunque se llama "unsafe", es el método estándar para integrar reproductores de audio personalizados o estilos CSS en Streamlit.
      * Documentación: [Streamlit API Reference](https://www.google.com/search?q=https://docs.streamlit.io/library/api-reference/text/st.markdown)