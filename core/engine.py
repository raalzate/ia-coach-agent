import streamlit as st
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from llama_cpp import Llama
import config

@st.cache_resource(show_spinner=False)
def load_grammar_engine():
    try:
        # use_fast=False es obligatorio en Mac
        tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction", use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error Vennify: {e}")
        st.stop()

@st.cache_resource(show_spinner=False)
def load_chat_engine():
    if not os.path.exists(config.MODEL_PATH):
        st.error(f"❌ No encuentro el modelo: {config.MODEL_PATH}")
        st.stop()
    try:
        # n_gpu_layers=0 para estabilidad máxima
        return Llama(model_path=config.MODEL_PATH, n_ctx=4096, n_gpu_layers=0, verbose=False)
    except Exception as e:
        st.error(f"Error Llama: {e}")
        st.stop()