import streamlit as st
import time
import os
# Imports locales (Asumimos que existen y funcionan)
import config
from core.coach import EnglishCoach
from core.engine import load_grammar_engine, load_chat_engine
from utils.audio import get_audio_bytes, render_audio_player

# --- 1. CONFIGURACIÓN Y ESTILOS (UX Visual) ---
st.set_page_config(
    page_title=config.APP_TITLE, 
    page_icon="🎓", 
    layout="wide", # Mejor uso del espacio en escritorio
    initial_sidebar_state="expanded"
)

# CSS Personalizado para pulir la UI
st.markdown("""
<style>
    .stChatMessage { padding: 1rem; border-radius: 10px; }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    /* Caja de corrección más amigable */
    div[data-testid="stAlert"] { border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- 2. CACHÉ DE RECURSOS (UX Performance) ---
# Usamos @st.cache_resource para que los modelos NO se recarguen con cada interacción.
# Esto reduce el tiempo de espera de segundos a milisegundos.
@st.cache_resource
def get_resources():
    grammar_tok, grammar_mod = load_grammar_engine()
    chat_llm = load_chat_engine()
    return grammar_tok, grammar_mod, chat_llm

# --- 3. INICIALIZACIÓN DE ESTADO ---
if "coach" not in st.session_state:
    # Feedback inicial limpio sin bloquear toda la UI visualmente feo
    with st.status("🚀 Booting up AI Teacher...", expanded=True) as status:
        st.write("Loading Neural Networks...")
        grammar_tok, grammar_mod, chat_llm = get_resources()
        st.session_state.grammar_tok = grammar_tok
        st.session_state.grammar_mod = grammar_mod
        st.session_state.chat_llm = chat_llm
        
        st.write("Waking up English Coach...")
        st.session_state.coach = EnglishCoach()
        
        # Mensaje de bienvenida
        intro = st.session_state.coach.get_intro_message()
        intro_audio = get_audio_bytes(intro)
        
        st.session_state.messages = [{
            "role": "assistant", 
            "content": intro, 
            "audio": intro_audio 
        }]
        status.update(label="Ready to learn!", state="complete", expanded=False)

coach = st.session_state.coach

# --- 4. SIDEBAR MEJORADO ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/classroom.png", width=80) # Icono visual
    st.title("My Class Notebook")
    
    if coach.is_onboarding_complete():
        # Métricas visuales en columnas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Level", coach.progress["current_level"])
        with col2:
            st.metric("Topic", str(coach.progress["current_topic_index"] + 1))
            
        st.divider()
        
        # Barra de progreso con contexto
        topics = config.CURRICULUM.get(coach.progress["current_level"], [])
        idx = coach.progress["current_topic_index"]
        val = idx/len(topics) if topics else 1.0
        st.caption(f"Current Lesson: **{topics[idx] if idx < len(topics) else 'Review'}**")
        st.progress(val)
    else:
        st.info("📝 **Onboarding Mode**: I'm getting to know you.")
    
    st.divider()
    with st.expander("⚙️ Settings & Data"):
        st.caption(f"Student Profile: **{coach.profile.get('name', 'Guest')}**")
        if st.button("🗑️ Reset Progress", use_container_width=True, type="primary"):
            if os.path.exists("student_progress.json"): os.remove("student_progress.json")
            if os.path.exists("student_profile.json"): os.remove("student_profile.json")
            st.rerun()

# --- 5. ÁREA DE CHAT ---
st.subheader(f"💬 {config.APP_TITLE}")

# Contenedor para el chat (mantiene el scroll manejable)
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        
        if role == "corrector":
            # Diseño visual distinto para correcciones (no un error rojo agresivo)
            with st.chat_message("assistant", avatar="🧐"):
                st.warning(f"**Let's polish that grammar:**\n\n❌ *{msg['original']}*\n✅ **{msg['correction']}**")
        
        else:
            avatar = "👩‍🏫" if role == "assistant" else "👤"
            with st.chat_message(role, avatar=avatar):
                st.markdown(msg["content"])
                # Audio solo para el asistente
                if role == "assistant" and msg.get("audio"):
                    # Usamos una clave única para evitar conflictos de renderizado
                    render_audio_player(msg["audio"], autoplay=False)

# --- 6. INPUT Y LÓGICA ---
if prompt := st.chat_input("Type your answer in English..."):
    
    # 1. Comandos de aprendizaje
    if prompt.startswith("/learn"):
        coach.learn_cmd(prompt.replace("/learn", "").strip())
        st.toast("✅ Memory updated successfully!", icon="🧠")
        time.sleep(1) # Breve pausa para que el usuario lea
        st.rerun()

    # 2. Validación Gramatical (Con UX mejorada)
    if coach.is_onboarding_complete():
        is_correct, correction = coach.check_grammar(prompt, st.session_state.grammar_tok, st.session_state.grammar_mod)
        if not is_correct:
            st.toast("Just a small grammar check...", icon="🔧") 
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "corrector", "original": prompt, "correction": correction})
            st.rerun()

    # 3. Procesamiento del Chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Renderizar mensaje de usuario inmediatamente
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

    # Respuesta del Asistente
    with chat_container:
        with st.chat_message("assistant", avatar="👩‍🏫"):
            # UI de "Pensando..."
            text_placeholder = st.empty()
            audio_placeholder = st.empty()
            
            # Auto-learn silencioso
            learned = coach.auto_learn(prompt)
            if learned:
                st.toast("I learned something new about you!", icon="💡")

            # Preparar contexto
            sys_p = coach.get_system_prompt()
            history = [{"role": "system", "content": sys_p}]
            for m in st.session_state.messages[-6:]:
                if m["role"] in ["user", "assistant"]: 
                    history.append({"role": m["role"], "content": m["content"]})

            # Streaming
            full_text = ""
            # Simular typing effect si la carga es lenta, o stream real
            stream = st.session_state.chat_llm.create_chat_completion(messages=history, max_tokens=256, temperature=0.7, stream=True)
            
            for chunk in stream:
                delta = chunk['choices'][0]['delta'].get('content', "")
                full_text += delta
                text_placeholder.markdown(full_text + "▌")
            
            final_text = full_text.replace("[PASSED]", "").strip()
            text_placeholder.markdown(final_text)
            
            # Audio (Generación asíncrona simulada visualmente)
            if final_text:
                with st.spinner("Creating audio..."):
                    audio_bytes = get_audio_bytes(final_text)
                
                # Autoplay invisible o mini player
                with audio_placeholder:
                    render_audio_player(audio_bytes, autoplay=True)
            
            # Actualizar estado
            st.session_state.messages.append({"role": "assistant", "content": final_text, "audio": audio_bytes})
            
            if "[PASSED]" in full_text or learned:
                coach.advance()
                st.toast("🎉 Progress Saved!", icon="🚀")