# import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import tempfile
# import os
# from textblob import TextBlob
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer

# def summarize_text(text):
#     try:
#         parser = PlaintextParser.from_string(text, Tokenizer("english"))
#         summarizer = LsaSummarizer()
#         summary = summarizer(parser.document, 3)  # Summarize into 3 sentences
#         return ' '.join([str(sentence) for sentence in summary])
#     except Exception as e:
#         return f"Erreur lors de la génération du résumé : {e}"

# # Initialisation
# translator = Translator()
# recognizer = sr.Recognizer()

# # Fonction de transcription
# def transcribe_audio(language):
#     with sr.Microphone() as source:
#         st.write("Enregistrement en cours...")
#         audio = recognizer.listen(source)
#         st.write("Enregistrement terminé.")
#         try:
#             transcription = recognizer.recognize_google(audio, language=language)
#             return transcription
#         except sr.UnknownValueError:
#             return "Erreur : impossible de comprendre l'audio."
#         except sr.RequestError as e:
#             return f"Erreur de service : {e}"

# # Fonction de traduction
# def translate_text(text, dest_language):
#     try:
#         return translator.translate(text, dest=dest_language).text
#     except Exception as e:
#         return f"Erreur de traduction : {e}"

# # Fonction d'analyse des sentiments
# def analyze_sentiment(text):
#     blob = TextBlob(text)
#     return blob.sentiment.polarity, blob.sentiment.subjectivity  # Renvoie deux scores

# # Fonction de synthèse vocale
# def text_to_speech(text, lang):
#     tts = gTTS(text=text, lang=lang)  # Utiliser la langue choisie
#     with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
#         tts.save(temp_audio_file.name)
#         os.system(f'start {temp_audio_file.name}')  # Utiliser pour Windows


# # Interface Streamlit
# def main():
#     st.title("Transcription et Traduction Audio")
    
#     # Sélection de la langue de transcription
#     language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr-FR", "en-US"])
    
#     if st.button("Transcrire"):
#         transcription = transcribe_audio(language)
#         st.session_state.transcription = transcription
#         st.text_area("Transcription :", value=transcription, height=200)

#         # Analyse des sentiments
#         sentiment_score, subjectivity_score = analyze_sentiment(transcription)
#         st.write("Analyse de sentiment (score) :", sentiment_score)
#         st.write("Subjectivité (score) :", subjectivity_score)

#         # Résumé
#         if st.button("Résumé"):
#             summary = summarize_text(transcription)
#             st.text_area("Résumé :", value=summary, height=200)

#         # Traduction
#         if st.button("Traduire"):
#             translated_text = translate_text(transcription, "en")
#             st.text_area("Traduction :", value=translated_text, height=200)
            
#             # Synthèse vocale
#             if st.button("Lire la traduction"):
#                 text_to_speech(translated_text, "en")  # Changez 'en' selon la langue désirée

#         # Commentaires
#         comment = st.text_area("Laissez un commentaire sur la transcription :")
        
#         # Recherche
#         search_query = st.text_input("Rechercher dans la transcription :")
#         if search_query and search_query in transcription:
#             st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
#         elif search_query:
#             st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import tempfile
# import os
# from textblob import TextBlob
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer

# def summarize_text(text):
#     try:
#         parser = PlaintextParser.from_string(text, Tokenizer("english"))
#         summarizer = LsaSummarizer()
#         summary = summarizer(parser.document, 3)  # Summarize into 3 sentences
#         return ' '.join([str(sentence) for sentence in summary])
#     except Exception as e:
#         return f"Erreur lors de la génération du résumé : {e}"

# # Initialisation
# translator = Translator()
# recognizer = sr.Recognizer()

# # Fonction de transcription
# def transcribe_audio(language):
#     try:
#         with sr.Microphone() as source:
#             st.write("Enregistrement en cours...")
#             audio = recognizer.listen(source)
#             st.write("Enregistrement terminé.")
#             # transcription = recognizer.recognize_google(audio, language=language)
#             # return transcription
#             return audio
#     except sr.UnknownValueError:
#         return "Erreur : impossible de comprendre l'audio."
#     except sr.RequestError as e:
#         return f"Erreur de service : {e}"
#     except Exception as e:
#         return f"Erreur : {e}"

# # Fonction de traduction
# def translate_text(text, dest_language):
#     try:
#         return translator.translate(text, dest=dest_language).text
#     except Exception as e:
#         return f"Erreur de traduction : {e}"

# # Fonction d'analyse des sentiments
# def analyze_sentiment(text):
#     blob = TextBlob(text)
#     return blob.sentiment.polarity, blob.sentiment.subjectivity  # Renvoie deux scores

# # Fonction de synthèse vocale
# def text_to_speech(text, lang):
#     tts = gTTS(text=text, lang=lang)  # Utiliser la langue choisie
#     with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
#         tts.save(temp_audio_file.name)
#         os.system(f'start {temp_audio_file.name}')  # Utiliser pour Windows

# # Interface Streamlit
# def main():
#     st.title("Transcription et Traduction Audio")
    
#     # Sélection de la langue de transcription
#     language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr-FR", "en-US"])
    
#     if st.button("Transcrire"):
#         transcription = transcribe_audio(language)
#         st.session_state.transcription = transcription
#         st.text_area("Transcription :", value=transcription, height=200)

#         # Analyse des sentiments
#         if transcription:
#             sentiment_score, subjectivity_score = analyze_sentiment(transcription)
#             st.write("Analyse de sentiment (score) :", sentiment_score)
#             st.write("Subjectivité (score) :", subjectivity_score)

#         # Résumé
#         if st.button("Résumé"):
#             if transcription:
#                 summary = summarize_text(transcription)
#                 st.text_area("Résumé :", value=summary, height=200)
#             else:
#                 st.warning("Veuillez d'abord transcrire l'audio.")

#         # Traduction
#         if st.button("Traduire"):
#             if transcription:
#                 translated_text = translate_text(transcription, "en")
#                 st.text_area("Traduction :", value=translated_text, height=200)

#                 # Synthèse vocale
#                 if st.button("Lire la traduction"):
#                     text_to_speech(translated_text, "en")  # Changez 'en' selon la langue désirée
#             else:
#                 st.warning("Veuillez d'abord transcrire l'audio.")

#         # Commentaires
#         comment = st.text_area("Laissez un commentaire sur la transcription :")
        
#         # Recherche
#         search_query = st.text_input("Rechercher dans la transcription :")
#         if search_query and search_query in transcription:
#             st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
#         elif search_query:
#             st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

# if __name__ == "__main__":
#     main()



# import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import tempfile
# import os
# from textblob import TextBlob
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer

# def summarize_text(text):
#     try:
#         parser = PlaintextParser.from_string(text, Tokenizer("english"))
#         summarizer = LsaSummarizer()
#         summary = summarizer(parser.document, 3)  # Résumer en 3 phrases
#         return ' '.join([str(sentence) for sentence in summary])
#     except Exception as e:
#         return f"Erreur lors de la génération du résumé : {e}"

# # Initialisation
# translator = Translator()
# recognizer = sr.Recognizer()

# # Fonction de transcription
# def transcribe_audio(language):
#     try:
#         with sr.Microphone() as source:
#             st.write("Enregistrement en cours...")
#             audio = recognizer.listen(source)
#             st.write("Enregistrement terminé.")
#             transcription = recognizer.recognize_google(audio, language=language)
#             return transcription
#     except sr.UnknownValueError:
#         return "Erreur : impossible de comprendre l'audio."
#     except sr.RequestError as e:
#         return f"Erreur de service : {e}"
#     except Exception as e:
#         return f"Erreur : {e}"

# # Fonction de traduction
# def translate_text(text, dest_language):
#     try:
#         return translator.translate(text, dest=dest_language).text
#     except Exception as e:
#         return f"Erreur de traduction : {e}"

# # Fonction d'analyse des sentiments
# def analyze_sentiment(text):
#     blob = TextBlob(text)
#     return blob.sentiment.polarity, blob.sentiment.subjectivity  # Renvoie deux scores

# # Fonction de synthèse vocale
# def text_to_speech(text, lang):
#     tts = gTTS(text=text, lang=lang)  # Utiliser la langue choisie
#     with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
#         tts.save(temp_audio_file.name)
#         os.system(f'start {temp_audio_file.name}')  # Utiliser pour Windows

# # Interface Streamlit
# def main():
#     st.title("Transcription et Traduction Audio")
    
#     # Sélection de la langue de transcription
#     language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr-FR", "en-US"])
    
#     if st.button("Transcrire"):
#         transcription = transcribe_audio(language)
#         st.session_state.transcription = transcription
#         st.text_area("Transcription :", value=transcription, height=200)

#         # Analyse des sentiments
#         if transcription and not transcription.startswith("Erreur"):
#             sentiment_score, subjectivity_score = analyze_sentiment(transcription)
#             st.write("Analyse de sentiment (score) :", sentiment_score)
#             st.write("Subjectivité (score) :", subjectivity_score)

#         # Résumé
#         if st.button("Résumé"):
#             if transcription and not transcription.startswith("Erreur"):
#                 summary = summarize_text(transcription)
#                 st.text_area("Résumé :", value=summary, height=200)
#             else:
#                 st.warning("Veuillez d'abord transcrire l'audio.")

#         # Traduction
#         if st.button("Traduire"):
#             if transcription and not transcription.startswith("Erreur"):
#                 translated_text = translate_text(transcription, "en")
#                 st.text_area("Traduction :", value=translated_text, height=200)

#                 # Synthèse vocale
#                 if st.button("Lire la traduction"):
#                     text_to_speech(translated_text, "en")  # Changez 'en' selon la langue désirée
#             else:
#                 st.warning("Veuillez d'abord transcrire l'audio.")

#         # Commentaires
#         comment = st.text_area("Laissez un commentaire sur la transcription :")
        
#         # Recherche
#         search_query = st.text_input("Rechercher dans la transcription :")
#         if search_query and search_query in transcription:
#             st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
#         elif search_query:
#             st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

# if __name__ == "__main__":
#     main()



import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Résumer en 3 phrases
        return ' '.join([str(sentence) for sentence in summary])
    except Exception as e:
        return f"Erreur lors de la génération du résumé : {e}"

# Initialisation
translator = Translator()
recognizer = sr.Recognizer()

# Fonction de transcription
def transcribe_audio(language):
    try:
        with sr.Microphone() as source:
            st.write("Enregistrement en cours...")
            audio = recognizer.listen(source)
            st.write("Enregistrement terminé.")
            
            if audio:  # Vérifiez si l'objet audio est valide
                transcription = recognizer.recognize_google(audio, language=language)
                return transcription
            else:
                return "Erreur : aucun audio n'a été enregistré."
    except sr.UnknownValueError:
        return "Erreur : impossible de comprendre l'audio."
    except sr.RequestError as e:
        return f"Erreur de service : {e}"
    except Exception as e:
        return f"Erreur : {e}"

# Fonction de traduction
def translate_text(text, dest_language):
    try:
        return translator.translate(text, dest=dest_language).text
    except Exception as e:
        return f"Erreur de traduction : {e}"

# Fonction d'analyse des sentiments
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity  # Renvoie deux scores

# Fonction de synthèse vocale
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)  # Utiliser la langue choisie
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
        tts.save(temp_audio_file.name)
        os.system(f'start {temp_audio_file.name}')  # Utiliser pour Windows

# Interface Streamlit
def main():
    st.title("Transcription et Traduction Audio")
    
    # Sélection de la langue de transcription
    language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr-FR", "en-US"])
    
    if st.button("Transcrire"):
        transcription = transcribe_audio(language)
        st.session_state.transcription = transcription
        st.text_area("Transcription :", value=transcription, height=200)

        # Analyse des sentiments
        if transcription and not transcription.startswith("Erreur"):
            sentiment_score, subjectivity_score = analyze_sentiment(transcription)
            st.write("Analyse de sentiment (score) :", sentiment_score)
            st.write("Subjectivité (score) :", subjectivity_score)

        # Résumé
        if st.button("Résumé"):
            if transcription and not transcription.startswith("Erreur"):
                summary = summarize_text(transcription)
                st.text_area("Résumé :", value=summary, height=200)
            else:
                st.warning("Veuillez d'abord transcrire l'audio.")

        # Traduction
        if st.button("Traduire"):
            if transcription and not transcription.startswith("Erreur"):
                translated_text = translate_text(transcription, "en")
                st.text_area("Traduction :", value=translated_text, height=200)

                # Synthèse vocale
                if st.button("Lire la traduction"):
                    text_to_speech(translated_text, "en")  # Changez 'en' selon la langue désirée
            else:
                st.warning("Veuillez d'abord transcrire l'audio.")

        # Commentaires
        comment = st.text_area("Laissez un commentaire sur la transcription :")
        
        # Recherche
        search_query = st.text_input("Rechercher dans la transcription :")
        if search_query and search_query in transcription:
            st.write(f"Le mot '{search_query}' a été trouvé dans la transcription.")
        elif search_query:
            st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

if __name__ == "__main__":
    main()
