import torch
import gc
import re
import config
from utils.data import load_json, save_json

class EnglishCoach:
    def __init__(self):
        # 1. Definimos el flujo de preguntas ordenado
        self.ONBOARDING_STEPS = [
            {"key": "name", "q": "Hello! I am **Emma**, your AI Coach. Let's build your profile. **What is your name?**"},
            {"key": "goal", "q": "Nice to meet you! **Why are you learning English?** (e.g., Work, Travel, Exams, Fun)"},
            {"key": "age", "q": "Got it. Just to know your demographic, **how old are you?**"},
            {"key": "education", "q": "Tell me about your background. **What did you study or what is your profession?**"},
            {"key": "hobbies", "q": "I want to make examples fun for you. **Do you have any hobbies or sports you like?**"},
            {"key": "movies", "q": "Great! Pop culture is important. **What kind of movies or TV shows do you watch?**"},
            {"key": "travel", "q": "Last question! **Have you traveled to other countries? Which ones?** (Or where would you like to go?)"}
        ]

        # 2. Inicializamos el perfil asegurando que todas las claves existan
        default_profile = {step["key"]: None for step in self.ONBOARDING_STEPS}
        default_profile["facts"] = [] # Lista extra para hechos aleatorios
        
        self.profile = load_json("student_profile.json", default_profile)
        
        # Validar consistencia del JSON cargado (por si agregaste preguntas nuevas)
        for step in self.ONBOARDING_STEPS:
            if step["key"] not in self.profile:
                self.profile[step["key"]] = None

        # Cargar progreso
        self.progress = load_json("student_progress.json", {"current_level": list(config.CURRICULUM.keys())[0], "current_topic_index": 0})

    def is_onboarding_complete(self):
        # El onboarding termina si TODAS las claves de los pasos tienen valor
        for step in self.ONBOARDING_STEPS:
            if not self.profile.get(step["key"]):
                return False
        return True

    def get_intro_message(self):
        # 1. Modo Onboarding: Buscar la primera pregunta sin respuesta
        for step in self.ONBOARDING_STEPS:
            if not self.profile.get(step["key"]):
                # Si ya tenemos el nombre, personalizamos un poco la pregunta
                if self.profile.get("name") and "{name}" not in step["q"]:
                    return step["q"]
                return step["q"] # Retorna la pregunta correspondiente al campo vacío
        
        # 2. Modo Lección (Ya terminó el onboarding)
        level = self.progress["current_level"]
        topics = config.CURRICULUM.get(level, [])
        idx = self.progress["current_topic_index"]
        topic = topics[idx] if idx < len(topics) else "Review"
        
        return (
            f"✅ **Profile Completed!** Thanks {self.profile['name']}.\n"
            f"I know you like **{self.profile.get('hobbies', 'many things')}** and you want to travel to **{self.profile.get('travel', 'places')}**.\n\n"
            f"Let's start! Level: **{level}**.\n"
            f"Topic: **{topic}**.\n"
            "Are you ready?"
        )

    def auto_learn(self, text):
        """Guarda la respuesta del usuario en el campo correcto automáticamente"""
        if not self.is_onboarding_complete():
            text_clean = text.strip()
            updated = False
            
            # Recorremos los pasos para ver cuál es el PRIMERO que falta
            for step in self.ONBOARDING_STEPS:
                key = step["key"]
                
                # Si este campo está vacío, la respuesta actual del usuario PERTENECE a este campo
                if not self.profile[key]:
                    
                    # Lógica específica para limpiar datos según el tipo
                    if key == "name":
                        clean_val = text_clean.lower().replace("my name is", "").replace("i am", "").replace("i'm", "").strip(" .!")
                        self.profile[key] = clean_val.title()
                    
                    elif key == "age":
                        nums = re.findall(r'\d+', text_clean)
                        if nums:
                            self.profile[key] = nums[0]
                        else:
                            # Si no escribe número, guardamos el texto tal cual
                            self.profile[key] = text_clean
                    
                    else:
                        # Para hobbies, travel, movies, education -> Guardamos todo el texto
                        self.profile[key] = text_clean
                    
                    updated = True
                    break # Importante: Solo llenamos UNO a la vez por turno
            
            if updated:
                save_json("student_profile.json", self.profile)
                return True
                
        return False

    def get_system_prompt(self):
        # Generar prompt dinámico basado en toda la info recopilada
        if not self.is_onboarding_complete():
            # Buscar qué estamos preguntando ahora para orientar al bot
            current_field = "UNKNOWN"
            for step in self.ONBOARDING_STEPS:
                if not self.profile[step["key"]]:
                    current_field = step["key"].upper()
                    break
            
            return (
                f"You are Emma, a friendly English Coach. "
                f"Current Goal: Ask the student for their {current_field}. "
                f"Do not teach yet. Be polite and encouraging."
            )

        # Prompt completo con toda la riqueza del perfil nuevo
        user_context = ", ".join([f"{step['key'].capitalize()}: {self.profile[step['key']]}" for step in self.ONBOARDING_STEPS])
        
        level = self.progress["current_level"]
        topics = config.CURRICULUM.get(level, [])
        idx = self.progress["current_topic_index"]
        current_topic = topics[idx] if idx < len(topics) else "Free Talk"

        return f"""
        ROLE: You are Emma, an expert English Coach.
        STUDENT PROFILE: [{user_context}]
        CURRENT LEVEL: {level}
        TOPIC: "{current_topic}"

        INSTRUCTIONS:
        1. Use the student's profile! Example: If talking about 'Future Tense' and they like '{self.profile.get('movies')}', ask "Which movie will you watch next?".
        2. If they studied '{self.profile.get('education')}', use related vocabulary context.
        3. Correct grammar gently.
        4. If the student masters "{current_topic}", append [PASSED] (hidden).
        """
    
    # ... (El resto de métodos check_grammar, advance, learn_cmd siguen igual) ...
    def check_grammar(self, text, tokenizer, model):
        input_ids = tokenizer(f"grammar: {text}", return_tensors="pt").input_ids
        with torch.no_grad():
            outputs = model.generate(input_ids, max_new_tokens=128)
        corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
        del input_ids, outputs; gc.collect()
        clean_in = text.strip().lower().rstrip(".!?")
        clean_out = corrected.strip().lower().rstrip(".!?")
        return (clean_in == clean_out), corrected

    def advance(self):
        level = self.progress["current_level"]
        topics = config.CURRICULUM.get(level, [])
        self.progress["current_topic_index"] += 1
        if self.progress["current_topic_index"] >= len(topics):
            # Lógica simple de avance de nivel (puedes usar la dinámica anterior si prefieres)
            levels = list(config.CURRICULUM.keys())
            try:
                curr_idx = levels.index(level)
                if curr_idx + 1 < len(levels):
                    self.progress["current_level"] = levels[curr_idx + 1]
                    self.progress["current_topic_index"] = 0
            except: pass
        save_json("student_progress.json", self.progress)

    def learn_cmd(self, text):
        if text not in self.profile["facts"]: self.profile["facts"].append(text)
        save_json("student_profile.json", self.profile)