import asyncio
import edge_tts
import base64
import streamlit as st

async def _gen_audio_bytes(text):
    file_path = "temp_audio_buffer.mp3"
    # Voz AriaNeural (Profesora)
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(file_path)
    with open(file_path, "rb") as f:
        data = f.read()
    return data

def get_audio_bytes(text):
    # Limpiar texto de marcas internas
    clean_text = text.replace("[PASSED]", "").replace("*", "").replace("#", "").strip()
    if not clean_text: return None
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(_gen_audio_bytes(clean_text))
        loop.close()
        return audio_bytes
    except Exception as e:
        print(f"Audio Error: {e}")
        return None

def render_audio_player(audio_bytes, autoplay=False):
    """
    Renderiza un reproductor de audio.
    Si autoplay=True, añade el atributo autoplay al HTML.
    """
    if not audio_bytes: return
    
    b64 = base64.b64encode(audio_bytes).decode()
    autoplay_attr = 'autoplay="true"' if autoplay else ''
    
    # HTML5 Audio Player (Visible y con controles)
    md = f"""
        <audio controls {autoplay_attr} style="width: 100%; margin-bottom: 10px;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)