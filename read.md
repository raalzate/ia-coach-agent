CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir

pkill -9 -f streamlit

MODEL_PATH = "/Users/raul.alzate/.lmstudio/models/NikolayKozloff/Meta-Llama-3-8B-Instruct-bf16-correct-pre-tokenizer-and-EOS-token-Q8_0-Q6_k-Q4_K_M-GGUF/Meta-Llama-3-8B-Instruct-bf16-correct-pre-tokenizer-and-EOS-token-Q4_K_M.gguf" 
