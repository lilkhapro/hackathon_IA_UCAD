# import streamlit as st
# import whisper
# from googletrans import Translator
# from gtts import gTTS
# import tempfile
# import os
# from textblob import TextBlob
# from transformers import pipeline

# # Initialisation
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # Fonction de transcription avec Whisper
# def transcribe_audio(language, audio_file):
#     if audio_file is not None:
#         st.audio(audio_file)
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
#                 tmp.write(audio_file.read())
#                 tmp_path = tmp.name
#             transcription = model.transcribe(tmp_path)
#             return transcription['text']
#         except Exception as e:
#             return f"Erreur lors de la transcription : {e}"
#     return None


# # # Fonction de traduction
# # def translate_text(text, dest_language):
# #     try:
# #         return translator.translate(text, dest=dest_language).text
# #     except Exception as e:
# #         return f"Erreur de traduction : {e}"

# # Fonction de traduction
# def translate_text(text, dest_language):
#     # Vérifier si la transcription est vide
#     if not text or text.strip() == "":
#         return "La transcription est vide, rien à traduire."
    
#     try:
        
#         return translator.translate(text, dest=dest_language)
#     except Exception as e:
#         return f"Erreur de traduction : {e}"

# # Fonction d'analyse des sentiments
# def analyze_sentiment(text):
#     try:
#         if not text.strip():
#             return 0.0, 0.0  # Pas de sentiment si le texte est vide
#         blob = TextBlob(text)
#         return blob.sentiment.polarity, blob.sentiment.subjectivity
#     except Exception as e:
#         return f"Erreur lors de l'analyse de sentiment : {e}", 0.0


# # Fonction de synthèse vocale
# def text_to_speech(text, lang):
#     try:
#         tts = gTTS(text=text, lang=lang)
#         with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
#             tts.save(temp_audio_file.name)
#             # Utilisation multiplateforme
#             if os.name == "nt":  # Pour Windows
#                 os.system(f'start {temp_audio_file.name}')
#             else:  # Pour Linux/Mac
#                 os.system(f'xdg-open {temp_audio_file.name}')
#     except Exception as e:
#         st.error(f"Erreur lors de la synthèse vocale : {e}")


# # # Fonction de résumé avec Hugging Face
# # def summarize_text(text):
# #     try:
# #         if len(text) < 30:
# #             return "Le texte est trop court pour être résumé."
# #         summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
# #         return summary[0]['summary_text']
# #     except Exception as e:
# #         return f"Erreur lors de la génération du résumé : {e}"

# def split_text(text, max_chunk_size=1024):
#     """Diviser le texte en morceaux plus petits pour éviter les dépassements de taille."""
#     words = text.split()
#     chunks = []
#     current_chunk = []
    
#     current_length = 0
#     for word in words:
#         if current_length + len(word) + 1 <= max_chunk_size:
#             current_chunk.append(word)
#             current_length += len(word) + 1
#         else:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = [word]
#             current_length = len(word)
    
#     if current_chunk:  # Ajouter le dernier chunk
#         chunks.append(" ".join(current_chunk))
    
#     return chunks

# def summarize_text(text, max_chunk_size=1024):
#     """Résumé du texte en divisant les textes longs en morceaux."""
#     try:
#         chunks = split_text(text, max_chunk_size)
#         summaries = []
        
#         for chunk in chunks:
#             summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
#             summaries.append(summary[0]['summary_text'])
        
#         return " ".join(summaries)
    
#     except Exception as e:
#         return f"Erreur lors de la génération du résumé : {e}"


# # Interface Streamlit
# def main():
#     st.title("Transcription et Traduction Audio")

#     # Sélection de la langue pour la transcription
#     language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Chargement du fichier audio
#     audio_file = st.file_uploader("Téléchargez un fichier audio", type=["wav", "mp3"])

#     if 'transcription' not in st.session_state:
#         st.session_state.transcription = None

#     if audio_file:
#         if st.button("Transcrire"):

#             st.session_state.transcription = transcribe_audio(language, audio_file)

#     if st.session_state.transcription:
#         st.text_area("Transcription :", value=st.session_state.transcription, height=200)

#         # Analyse des sentiments
#         sentiment_score, subjectivity_score = analyze_sentiment(st.session_state.transcription)
#         st.write("Analyse de sentiment (score) :", sentiment_score)
#         st.write("Subjectivité (score) :", subjectivity_score)

#         # Résumé
#         if st.button("Résumé"):
#             summary = summarize_text(st.session_state.transcription)
#             st.text_area("Résumé :", value=summary, height=200)

#         # # Traduction
#         # if st.button("Traduire"):
#         #     text = """  frankly appreciated. Our objective is to establish a reimagined and renewed partnership enriched by a shared vision of a more just international order that accurately reflects the realities of the current world we live in. A partnership that is ideally suited to the changes and fully capable of supporting the innovative momentum that we want to instill in our relationships. I also communicated to the president of the European Council that the friends and partners of Senegal are cordially invited to accompany us in the implementation of our program for a sovereign Senegal, a just Senegal, a prosperous Senegal in a progressing Africa and their support would be greatly appreciated."""
#         #     translated_text = translate_text(text, "en")
#         #     st.text_area("Traduction :", value=translated_text, height=200)

#         #     # Synthèse vocale
#         #     if st.button("Lire la traduction"):
#         #         text_to_speech(translated_text, "en")

#         # Traduction
#         if st.button("Traduire"):
#             transcription = transcribe_audio(language, audio_file)
            
#             # Assurer que la transcription n'est pas vide avant la traduction
#             if transcription :
#                 english_text = "The Assembly will hear an address by the President of Senegal."
#                 translated_text = translate_text(english_text, "fr")
#                 st.text_area("Traduction :", value=translated_text, height=200)
#             else:
#                 st.warning("La transcription est vide, impossible de traduire.")

#         # Commentaires
#         comment = st.text_area("Laissez un commentaire sur la transcription :")
        
#         # Recherche
#         search_query = st.text_input("Rechercher dans la transcription :")
#         if search_query and search_query in st.session_state.transcription:
#             st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
#         elif search_query:
#             st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import whisper
# from googletrans import Translator, LANGUAGES
# from gtts import gTTS
# import tempfile
# import os
# from textblob import TextBlob
# from transformers import pipeline

# # Initialisation
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # Fonction de transcription avec Whisper
# def transcribe_audio(language, audio_file):
#     if audio_file is not None:
#         st.audio(audio_file)
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
#                 tmp.write(audio_file.read())
#                 tmp_path = tmp.name
#             transcription = model.transcribe(tmp_path)
#             return transcription['text']
#         except Exception as e:
#             return f"Erreur lors de la transcription : {e}"
#     return None

# # Fonction de traduction avec gestion des erreurs
# def translate_text(text, dest_language):
#     if not text or text.strip() == "":
#         return "La transcription est vide, rien à traduire."
    
#     try:
#         # Utiliser l'API pour traduire
#         translated = translator.translate(text, dest=dest_language)
#         return translated.text if translated else "Erreur lors de la traduction."
#     except Exception as e:
#         return f"Erreur de traduction : {e}"

# # Fonction d'analyse des sentiments
# def analyze_sentiment(text):
#     try:
#         if not text.strip():
#             return 0.0, 0.0  # Pas de sentiment si le texte est vide
#         blob = TextBlob(text)
#         return blob.sentiment.polarity, blob.sentiment.subjectivity
#     except Exception as e:
#         return f"Erreur lors de l'analyse de sentiment : {e}", 0.0

# # Fonction de synthèse vocale
# def text_to_speech(text, lang):
#     try:
#         tts = gTTS(text=text, lang=lang)
#         with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
#             tts.save(temp_audio_file.name)
#             # Utilisation multiplateforme
#             if os.name == "nt":  # Pour Windows
#                 os.system(f'start {temp_audio_file.name}')
#             else:  # Pour Linux/Mac
#                 os.system(f'xdg-open {temp_audio_file.name}')
#     except Exception as e:
#         st.error(f"Erreur lors de la synthèse vocale : {e}")

# # Fonction pour diviser le texte en morceaux plus petits
# def split_text(text, max_chunk_size=1024):
#     """Diviser le texte en morceaux plus petits pour éviter les dépassements de taille."""
#     words = text.split()
#     chunks = []
#     current_chunk = []
    
#     current_length = 0
#     for word in words:
#         if current_length + len(word) + 1 <= max_chunk_size:
#             current_chunk.append(word)
#             current_length += len(word) + 1
#         else:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = [word]
#             current_length = len(word)
    
#     if current_chunk:  # Ajouter le dernier chunk
#         chunks.append(" ".join(current_chunk))
    
#     return chunks

# # Fonction de résumé
# def summarize_text(text, max_chunk_size=1024):
#     """Résumé du texte en divisant les textes longs en morceaux."""
#     try:
#         chunks = split_text(text, max_chunk_size)
#         summaries = []
        
#         for chunk in chunks:
#             summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
#             summaries.append(summary[0]['summary_text'])
        
#         return " ".join(summaries)
    
#     except Exception as e:
#         return f"Erreur lors de la génération du résumé : {e}"

# # Vérifier si la langue est supportée
# def is_language_supported(language_code):
#     return language_code in LANGUAGES.values()

# # Interface Streamlit
# def main():
#     st.title("Transcription et Traduction Audio")

#     # Sélection de la langue pour la transcription
#     transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Sélection de la langue pour la traduction
#     target_language_name = st.sidebar.selectbox("Choisissez la langue de traduction :", list(LANGUAGES.keys()))
#     dest_language = LANGUAGES[target_language_name]  # Obtenir le code de la langue

#     # Chargement du fichier audio
#     audio_file = st.file_uploader("Téléchargez un fichier audio", type=["wav", "mp3"])

#     if 'transcription' not in st.session_state:
#         st.session_state.transcription = None

#     if audio_file:
#         if st.button("Transcrire"):
#             st.session_state.transcription = transcribe_audio(transcription_language, audio_file)

#     if st.session_state.transcription:
#         st.text_area("Transcription :", value=st.session_state.transcription, height=200)

#         # Analyse des sentiments
#         sentiment_score, subjectivity_score = analyze_sentiment(st.session_state.transcription)
#         st.write("Analyse de sentiment (score) :", sentiment_score)
#         st.write("Subjectivité (score) :", subjectivity_score)

#         # Résumé
#         if st.button("Résumé"):
#             summary = summarize_text(st.session_state.transcription)
#             st.text_area("Résumé :", value=summary, height=200)

#         # Traduction
#         if st.button("Traduire"):
#             if is_language_supported(dest_language):
#                 translated_text = translate_text(st.session_state.transcription, dest_language)
#                 st.text_area("Traduction :", value=translated_text, height=200)
#             else:
#                 st.error(f"Langue '{dest_language}' non supportée pour la traduction.")

#         # Synthèse vocale de la traduction
#         if st.button("Lire la traduction"):
#             text_to_speech(st.session_state.transcription, dest_language)

#         # Commentaires
#         comment = st.text_area("Laissez un commentaire sur la transcription :")

#         # Recherche dans la transcription
#         search_query = st.text_input("Rechercher dans la transcription :")
#         if search_query and search_query in st.session_state.transcription:
#             st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
#         elif search_query:
#             st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import whisper
from gtts import gTTS
import tempfile
import os
from textblob import TextBlob
from transformers import pipeline
# import sounddevice as sd
import numpy as np
import queue 
from googletrans import Translator, LANGUAGES
from io import BytesIO

# Initialisation
# translator = Translator()
try:
    model = whisper.load_model("base")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# File d'attente pour les échantillons audio
audio_queue = queue.Queue()

# Fonction pour récupérer les échantillons audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# Fonction de transcription en temps réel avec Whisper
# def transcribe_real_time():
#     st.write("Démarrage de l'enregistrement...")
#     with sd.InputStream(callback=audio_callback, channels=2, samplerate=16000):
#         while True:
#             if not audio_queue.empty():
#                 audio_data = audio_queue.get()
#                 audio_data = np.squeeze(audio_data)  # Supprimer les dimensions supplémentaires
#                 audio_data = audio_data.astype(np.float32)  # S'assurer que les données sont en float32
                
#                 # Transcription de l'audio
#                 result = model.transcribe(audio_data, language="fr")  # Spécifier la langue 
#                 st.text(result['text'])

# Fonction de transcription avec Whisper
def transcribe_audio(language, audio_file):
    if audio_file is not None:
        st.audio(audio_file)
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            transcription = model.transcribe(tmp_path)
            return transcription['text']
        except Exception as e:
            return f"Erreur lors de la transcription : {e}"
    return None

# Fonction de traduction avec gestion des erreurs
def translate_text(text, dest_language):
    # if not text or text.strip() == "":
    #     return "La transcription est vide, rien à traduire."
    
    # try:
    #     # Utiliser l'API pour traduire
    #     translated = translator.translate(text, dest=dest_language)
    #     return translated.text if translated else "Erreur lors de la traduction."
    # except Exception as e:
    #     return f"Erreur de traduction : {e}"
    translator = Translator(service_urls=['translate.googleapis.com'])
    translation = translator.translate("Der Himmel ist blau und ich mag Bananen", dest='fr')
    print(translation.text)
    return translation.text 


# Fonction d'analyse des sentiments
def analyze_sentiment(text):
    try:
        if not text.strip():
            return 0.0, 0.0  # Pas de sentiment si le texte est vide
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except Exception as e:
        return f"Erreur lors de l'analyse de sentiment : {e}", 0.0

# Fonction de synthèse vocale
def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Utilisation d'un objet BytesIO pour stocker l'audio en mémoire
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)  # Revenir au début du fichier pour la lecture
        
        # Affichage et lecture de l'audio
        st.audio(audio_file, format='audio/mp3')
    except Exception as e:
        st.error(f"Erreur lors de la synthèse vocale : {e}")

# Fonction pour diviser le texte en morceaux plus petits
def split_text(text, max_chunk_size=1024):
    """Diviser le texte en morceaux plus petits pour éviter les dépassements de taille."""
    words = text.split()
    chunks = []
    current_chunk = []
    
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 <= max_chunk_size:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
    
    if current_chunk:  # Ajouter le dernier chunk
        chunks.append(" ".join(current_chunk))
    
    return chunks

# Fonction de résumé
def summarize_text(text, max_chunk_size=1024):
    """Résumé du texte en divisant les textes longs en morceaux."""
    try:
        chunks = split_text(text, max_chunk_size)
        summaries = []
        
        for chunk in chunks:
            summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        return " ".join(summaries)
    
    except Exception as e:
        return f"Erreur lors de la génération du résumé : {e}"

# Vérifier si la langue est supportée
def is_language_supported(language_code):
    return language_code in LANGUAGES.values()

# Interface Streamlit
def main():
    st.title("Transcription et Traduction Audio")

    # Sélection de la langue pour la transcription
    transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

    # Sélection de la langue pour la traduction
    target_language_name = st.sidebar.selectbox("Choisissez la langue de traduction :", list(LANGUAGES.keys()))
    dest_language = LANGUAGES[target_language_name]  # Obtenir le code de la langue

    # Chargement du fichier audio
    audio_file = st.file_uploader("Téléchargez un fichier audio", type=["wav", "mp3","mp4"])

    if 'transcription' not in st.session_state:
        st.session_state.transcription = None

    if audio_file:
        if st.button("Transcrire"):
            st.session_state.transcription = transcribe_audio(transcription_language, audio_file)
            text_transcription = st.session_state.transcription
    # Transcription en temps réel
    # if st.button("Démarrer la transcription en temps réel"):
    #     st.session_state.transcription = transcribe_real_time()

    if st.session_state.transcription:
        st.text_area("Transcription :", value=st.session_state.transcription, height=200)
        text_transcription = st.session_state.transcription

        # Analyse des sentiments
        sentiment_score, subjectivity_score = analyze_sentiment(st.session_state.transcription)
        st.write("Analyse de sentiment (score) :", sentiment_score)
        st.write("Subjectivité (score) :", subjectivity_score)

        # Résumé
        if st.button("Résumé"):
            summary = summarize_text(st.session_state.transcription)
            st.text_area("Résumé :", value=summary, height=200)

        # Traduction
        if st.button("Traduire"):
            if is_language_supported(dest_language):
                print("OK: sfdjsfdjnfsdnlsfk")
                translated_text = translate_text(st.session_state.transcription, dest_language)
                st.text_area("Traduction :", value=translated_text, height=200)
            else:
                st.error(f"Langue '{dest_language}' non supportée pour la traduction.")

        # # Synthèse vocale de la traduction
        # if st.button("Lire la traduction"):
        #     text_to_speech(st.session_state.transcription, dest_language)

        # Bouton pour générer l'audio
        # Sélection de la langue
        
        language = st.selectbox("Sélectionnez la langue", ['fr', 'en'])
        if st.button("Générer l'audio"):
            # Conversion du texte en audio
            text_to_speech(text_transcription,language)

        # Commentaires
        comment = st.text_area("Laissez un commentaire sur la transcription :")

        # Recherche dans la transcription
        search_query = st.text_input("Rechercher dans la transcription :")
        if search_query and search_query in st.session_state.transcription:
            st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
        elif search_query:
            st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

if __name__ == "__main__":
    main()