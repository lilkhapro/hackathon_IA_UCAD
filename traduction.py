# from transformers import MarianMTModel, MarianTokenizer

# # Charger le modèle et le tokenizer
# model_name = "Helsinki-NLP/opus-mt-en-fr"
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

# # Fonction de traduction
# def translate(text):
#     # Tokeniser le texte
#     tokens = tokenizer(text, return_tensors="pt", padding=True)
#     # Traduire
#     translated = model.generate(**tokens)
#     # Décoder le texte traduit
#     return tokenizer.decode(translated[0], skip_special_tokens=True)

# if __name__ == "__main__":
#     text = " frankly appreciated. Our objective is to establish a reimagined and renewed partnership enriched by a shared vision of a more just international order that accurately reflects the realities of the current world we live in. A partnership that is ideally suited to the changes and fully capable of supporting the innovative momentum that we want to instill in our relationships. I also communicated to the president of the European Council that the friends and partners of Senegal are cordially invited to accompany us in the implementation of our program for a sovereign Senegal, a just Senegal, a prosperous Senegal in a progressing Africa and their support would be greatly appreciated."
#     translated_text = translate(text)
#     print(f'Translated text: {translated_text}')




# import speech_recognition as sr
# from googletrans import Translator
# translator = Translator()
# text = "frankly appreciated. Our objective is to establish a reimagined and renewed partnership enriched by a shared vision of a more just international order that accurately reflects the realities of the current world we live in. A partnership that is ideally suited to the changes and fully capable of supporting the innovative momentum that we want to instill in our relationships. I also communicated to the president of the European Council that the friends and partners of Senegal are cordially invited to accompany us in the implementation of our program for a sovereign Senegal, a just Senegal, a prosperous Senegal in a progressing Africa and their support would be greatly appreciated."

# translation = translator.translate(text, dest='fr')
# print(translation.text)

# recognizer = sr.Recognizer()

# # Fonction de transcription
# def transcribe_audio(language):

#     with sr.Microphone() as source:
#         print("Enregistrement en cours...")
#         audio = recognizer.listen(source)
#         print("Enregistrement terminé.")
        
#         if audio:  # Vérifiez si l'objet audio est valide
#             transcription = recognizer.recognize_google(audio, language=language)
#             return transcription
#         else:
#             return "Erreur : aucun audio n'a été enregistré."


# transcribe_audio()
#output: 'The sky is blue and I like bananas'



# import speech_recognition as sr


# def transcribe_audio(language="en"):
#     recognizer = sr.Recognizer()
#     try:
#         # Utiliser 'with' pour s'assurer que la ressource est correctement ouverte/fermée
#         with sr.Microphone(device_index=0) as source:
#             print("Enregistrement en cours...")
#             # audio = recognizer.listen(source)
#             # # Reconnaissance de la parole
#             # text = recognizer.recognize_google(audio, language=language)
#             print(f"Texte reconnu : ")
#     except sr.RequestError:
#         print("Erreur lors de la requête à l'API.")
#     except sr.UnknownValueError:
#         print("Impossible de reconnaître l'audio.")

# if __name__ == "__main__":
#     # Lister les microphones disponibles
#     for index, name in enumerate(sr.Microphone.list_microphone_names()):
#         print(f"Microphone {index}: {name}")
#     transcribe_audio("en")


# import streamlit as st
# from gtts import gTTS
# from io import BytesIO

# # Titre de l'application
# st.title("Text-to-Speech avec Streamlit")

# # Entrée de texte pour l'utilisateur
# text = st.text_area("Entrez le texte que vous souhaitez convertir en audio:", "Bonjour, ceci est un exemple de conversion de texte en audio avec Python et Streamlit.")

# # Sélection de la langue
# language = st.selectbox("Sélectionnez la langue", ['fr', 'en'])

# # Bouton pour générer l'audio
# if st.button("Générer l'audio"):
#     # Conversion du texte en audio
#     tts = gTTS(text=text, lang=language, slow=False)
    
#     # Utilisation d'un objet BytesIO pour stocker l'audio en mémoire
#     audio_file = BytesIO()
#     tts.write_to_fp(audio_file)
#     audio_file.seek(0)  # Revenir au début du fichier pour la lecture
    
#     # Affichage et lecture de l'audio
#     st.audio(audio_file, format='audio/mp3')


# import sounddevice as sd
# import numpy as np
# # from scipy.io.wavfile import write
# import streamlit as st

# # Titre de l'application
# st.title("Enregistrement audio avec le microphone")

# # Paramètres de l'enregistrement
# sample_rate = 44100  # Taux d'échantillonnage
# duration = st.number_input("Durée d'enregistrement (en secondes)", min_value=1, max_value=60, value=5)

# if st.button("Démarrer l'enregistrement"):
#     st.write("Enregistrement en cours...")
    
#     # Enregistrement de l'audio
#     audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
#     sd.wait()  # Attendre la fin de l'enregistrement
    
#     # Sauvegarde de l'audio en tant que fichier WAV
#     # write("enregistrement.wav", sample_rate, audio)
    
#     st.write("Enregistrement terminé !")
#     st.audio("enregistrement.wav")  # Afficher l'audio pour lecture



import sounddevice as sd
import soundfile as sf
import streamlit as st
import tempfile
import whisper

# Titre de l'application
st.title("Enregistrement audio avec le microphone")

# Liste des périphériques audio
st.write("Périphériques audio disponibles :")
devices = sd.query_devices()
for i, device in enumerate(devices):
    st.write(f"{i}: {device['name']} - {'Input' if device['max_input_channels'] > 0 else 'Output'}")

# Demande à l'utilisateur de sélectionner un périphérique
device_index = st.number_input("Sélectionnez l'index du périphérique d'entrée", min_value=0, max_value=len(devices)-1, value=0)

# Paramètres de l'enregistrement
sample_rate = 44100  # Taux d'échantillonnage
duration = st.number_input("Durée d'enregistrement (en secondes)", min_value=1, max_value=60, value=5)

try:
    model = whisper.load_model("base")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# Fonction de transcription avec Whisper
# def transcribe_audio(audio_file):
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
# Fonction de transcription avec Whisper
def transcribe_audio(audio_file):
    if audio_file is not None:
        try:
            # Écriture de l'audio dans un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            
            # Transcription audio
            transcription = model.transcribe(tmp_path)
            return transcription['text']
        except Exception as e:
            return f"Erreur lors de la transcription : {e}"
    return None
if st.button("Démarrer l'enregistrement"):
    st.write("Enregistrement en cours...")
    
    # Enregistrement de l'audio avec le périphérique spécifié
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64', device=device_index)
    
    sd.wait()  # Attendre la fin de l'enregistrement

    audio_file_path = "enregistrement.wav"
    sf.write(audio_file_path, audio, sample_rate)

    st.write("Enregistrement terminé !")
    
    # Affichage de l'audio enregistré
    st.audio(audio_file_path)  # Spécifier le chemin du fichier audio
    
    with st.spinner("Transcription en cours..."):
        # Transcription
        texttt = transcribe_audio(open(audio_file_path, "rb"))
        st.write("Transcription :", texttt)
