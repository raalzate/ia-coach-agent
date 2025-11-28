import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# --- CONFIGURACIÓN CRÍTICA M1 ---
# Se ejecuta al importar este archivo
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Variables Globales
MODEL_PATH = os.getenv("MODEL_PATH", "model.gguf")
APP_TITLE = os.getenv("APP_TITLE", "Emma AI")

CURRICULUM = {
    "Level 1 (A1: Beginner)": [
        "The Alphabet & Spelling Names",
        "Subject Pronouns (I, You, He...)",
        "Verb To Be: Affirmative (I am...)",
        "Verb To Be: Negative & Questions",
        "Countries & Nationalities",
        "Possessive Adjectives (My, Your...)",
        "A / An / Plural Nouns",
        "Demonstratives (This, That, These, Those)",
        "Family Members & Genitive 's",
        "Prepositions of Place (In, On, Under)",
        "Present Simple: Habits (I work...)",
        "Present Simple: 3rd Person (He works...)",
        "Present Simple: Questions (Do/Does)",
        "Adverbs of Frequency (Always, Sometimes)",
        "Object Pronouns (Me, You, Him...)",
        "Can/Can't for Ability",
        "Present Continuous (Action right now)",
        "Imperatives (Give instructions)"
    ],
    "Level 2 (A2: Elementary)": [
        "Past Simple: To Be (Was/Were)",
        "Past Simple: Regular Verbs (-ed)",
        "Past Simple: Common Irregular Verbs",
        "Past Simple: Negatives & Questions",
        "Time Expressions (Yesterday, Ago, Last...)",
        "Countable & Uncountable Nouns (Some/Any)",
        "Quantifiers (Much, Many, A lot of)",
        "Comparatives (Better, Faster, More interesting)",
        "Superlatives (The best, The most...)",
        "Present Continuous for Future Arrangements",
        "Future with 'Going to' (Plans)",
        "Future with 'Will' (Predictions/Promises)",
        "Adverbs of Manner (Quickly, Well...)",
        "Verb Patterns (Like doing / Want to do)",
        "Have to / Don't have to (Obligation)",
        "Should / Shouldn't (Advice)",
        "Present Perfect: Introduction (Have done)",
        "Present Perfect vs Past Simple"
    ],
    "Level 3 (B1: Intermediate)": [
        "Present Perfect: For & Since",
        "Present Perfect: Just, Already, Yet",
        "First Conditional (Real possibilities)",
        "Second Conditional (Hypothetical)",
        "Used to (Past habits)",
        "Past Continuous (Interrupted actions)",
        "Defining Relative Clauses (Who, Which, That)",
        "Modal Verbs: Must/Mustn't (Rules)",
        "Modal Verbs: May/Might (Possibility)",
        "Passive Voice: Present Simple",
        "Passive Voice: Past Simple",
        "Reported Speech: Statements",
        "Question Tags",
        "Phasals Verbs: Separable vs Inseparable",
        "So / Neither do I (Agreeing)",
        "Reflexive Pronouns (Myself, Yourself)",
        "Past Perfect (The past before the past)"
    ],
    "Level 4 (B2: Upper Intermediate)": [
        "Third Conditional (Regrets)",
        "Mixed Conditionals",
        "Passive Voice: Advanced Tenses",
        "Have something done (Causative)",
        "Reported Speech: Questions & Commands",
        "Future Continuous (Will be doing)",
        "Future Perfect (Will have done)",
        "Modals of Deduction (Must have been...)",
        "Wish / If only (Desires)",
        "Gerunds vs Infinitives: Change in meaning",
        "Non-defining Relative Clauses",
        "Connectors of Contrast (Although, Despite...)",
        "Connectors of Purpose (So that, In order to...)",
        "Quantifiers: Either, Neither, Both, None",
        "Articles: Specific vs General usage",
        "Narrative Tenses Review"
    ],
    "Level 5 (C1: Advanced)": [
        "Inversion (Rarely do I...)",
        "Cleft Sentences (What I need is...)",
        "Subjunctive Mood (It is vital that...)",
        "Participle Clauses",
        "Advanced Passive Structures",
        "Future in the Past (Was going to...)",
        "Ellipsis & Substitution",
        "Causative Verbs (Let, Make, Have, Get)",
        "Compound Adjectives",
        "Discourse Markers in Speech",
        "Nuance: Verbs of seeing/walking/speaking",
        "Idioms & Fixed Expressions"
    ],
    "Level 6 (C2: Mastery / Business)": [
        "Formal Letter Writing Structure",
        "Negotiation Vocabulary & Phrases",
        "Presenting Data & Graphs",
        "Softening & Politeness Strategies",
        "Academic Linking Words",
        "Metaphorical Language",
        "Humor & Sarcasm in English",
        "Analyzing Tone & Register",
        "Debating Techniques",
        "English for Specific Purposes (Tech/Med/Law)"
    ]
}