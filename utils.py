import os
from transformers import pipeline
import tempfile
import streamlit as st
from gtts import gTTS
from io import BytesIO
import whisper
import queue 
import srt
from datetime import timedelta
from moviepy.editor import VideoFileClip
import tempfile
import numpy as np 
import sounddevice as sd


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

# Fonction de transcription en temps réel avec Whisper
def transcribe_real_time():
    st.write("Démarrage de l'enregistrement...")
    with sd.InputStream(callback=audio_callback, channels=2, samplerate=16000):
        while True:
            if not audio_queue.empty():
                audio_data = audio_queue.get()
                audio_data = np.squeeze(audio_data)  # Supprimer les dimensions supplémentaires
                audio_data = audio_data.astype(np.float32)  # S'assurer que les données sont en float32
                
                # Transcription de l'audio
                result = model.transcribe(audio_data, language="fr")  # Spécifier la langue 
                st.text(result['text'])

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


def show_audio_or_video(audio_file):
    if audio_file is not None:
        file_extension = audio_file.name.split('.')[-1].lower()

        # Afficher la vidéo si c'est un fichier vidéo
        if file_extension in ['mp4', 'mov', 'avi']:
            st.video(audio_file)
        else:
            st.audio(audio_file)

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

# Fonction de transcription Whisper avec génération des sous-titres
def generate_subtitles(audio_path, language="fr"):
    result = model.transcribe(audio_path, language=language, verbose=True)
    segments = result['segments']

    # Génération du fichier .srt
    subtitles = []
    for segment in segments:
        start = timedelta(seconds=segment['start'])
        end = timedelta(seconds=segment['end'])
        content = segment['text']
        subtitle = srt.Subtitle(index=len(subtitles) + 1, start=start, end=end, content=content)
        subtitles.append(subtitle)
    
    return srt.compose(subtitles)

# Fonction pour extraire l'audio d'une vidéo
def extract_audio_from_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.read())
        tmp_path = tmp.name
    video = VideoFileClip(tmp_path)
    audio_path = tmp_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_path)
    return audio_path
