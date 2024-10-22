import streamlit as st
import whisper
from googletrans import Translator, LANGUAGES
from moviepy.editor import VideoFileClip
import tempfile
import os
import srt
from datetime import timedelta

# Initialisation du modèle Whisper
translator = Translator()
try:
    model = whisper.load_model("base")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# Fonction pour extraire l'audio d'une vidéo
def extract_audio_from_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.read())
        tmp_path = tmp.name
    video = VideoFileClip(tmp_path)
    audio_path = tmp_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_path)
    return audio_path

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

# Interface Streamlit
def main():
    st.title("Générateur de Sous-titres pour Vidéos")

    # Sélection de la langue de transcription
    transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["en", "fr" , "wo"])

    # Chargement du fichier vidéo
    video_file = st.file_uploader("Téléchargez une vidéo", type=["mp4", "mov", "avi"])

    if video_file:
        # Afficher la vidéo
        st.video(video_file)

        if st.button("Générer les sous-titres"):
            with st.spinner("Transcription en cours..."):
                audio_path = extract_audio_from_video(video_file)
                subtitles = generate_subtitles(audio_path, language=transcription_language)
                
                # Sauvegarder le fichier .srt
                with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as srt_file:
                    srt_file.write(subtitles.encode("utf-8"))
                    srt_path = srt_file.name
                
                st.success("Sous-titres générés avec succès !")
                st.download_button("Télécharger les sous-titres (.srt)", data=subtitles, file_name="sous-titres.srt")

if __name__ == "__main__":
    main()



# import streamlit as st
# import whisper
# from googletrans import Translator, LANGUAGES
# from moviepy.editor import VideoFileClip
# import tempfile
# import os
# import srt
# from datetime import timedelta
# import subprocess

# # Initialisation du modèle Whisper
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# # Fonction pour extraire l'audio d'une vidéo
# def extract_audio_from_video(video_file):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
#         tmp.write(video_file.read())
#         tmp_path = tmp.name
#     video = VideoFileClip(tmp_path)
#     audio_path = tmp_path.replace(".mp4", ".wav")
#     video.audio.write_audiofile(audio_path)
#     return tmp_path, audio_path  # Retourner également le chemin de la vidéo originale

# # Fonction de transcription Whisper avec génération des sous-titres
# def generate_subtitles(audio_path, language="fr"):
#     result = model.transcribe(audio_path, language=language, verbose=True)
#     segments = result['segments']

#     # Génération du fichier .srt
#     subtitles = []
#     for segment in segments:
#         start = timedelta(seconds=segment['start'])
#         end = timedelta(seconds=segment['end'])
#         content = segment['text']
#         subtitle = srt.Subtitle(index=len(subtitles) + 1, start=start, end=end, content=content)
#         subtitles.append(subtitle)
    
#     return srt.compose(subtitles)

# # Fonction pour ajouter les sous-titres à une vidéo avec ffmpeg
# def add_subtitles_to_video(video_path, srt_path):
#     output_path = video_path.replace(".mp4", "_with_subs.mp4")
#     command = [
#         "ffmpeg", "-i", video_path, "-vf", f"subtitles={srt_path}", output_path
#     ]
#     subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     return output_path

# # Interface Streamlit
# def main():
#     st.title("Générateur de Sous-titres pour Vidéos")

#     # Sélection de la langue de transcription
#     transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Chargement du fichier vidéo
#     video_file = st.file_uploader("Téléchargez une vidéo", type=["mp4", "mov", "avi"])

#     if video_file:
#         # Afficher la vidéo d'origine
#         st.video(video_file)

#         if st.button("Générer les sous-titres et les intégrer à la vidéo"):
#             with st.spinner("Transcription et génération des sous-titres en cours..."):
#                 video_path, audio_path = extract_audio_from_video(video_file)
#                 subtitles = generate_subtitles(audio_path, language=transcription_language)
                
#                 # Sauvegarder le fichier .srt
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as srt_file:
#                     srt_file.write(subtitles.encode("utf-8"))
#                     srt_path = srt_file.name
                
#                 # Intégrer les sous-titres à la vidéo
#                 video_with_subs_path = add_subtitles_to_video(video_path, srt_path)
                
#                 st.success("Sous-titres générés et intégrés avec succès à la vidéo !")

#                 # Afficher la vidéo avec les sous-titres intégrés
#                 st.video(video_with_subs_path)

# if __name__ == "__main__":
#     main()


# import os
# import streamlit as st
# import whisper
# from googletrans import Translator, LANGUAGES
# from moviepy.editor import VideoFileClip
# import tempfile
# import srt
# from datetime import timedelta
# import subprocess
# from pathlib import Path

# # Initialisation du modèle Whisper
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# # Fonction pour extraire l'audio d'une vidéo
# def extract_audio_from_video(video_file):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
#         tmp.write(video_file.read())
#         tmp_path = tmp.name
#     video = VideoFileClip(tmp_path)
#     audio_path = tmp_path.replace(".mp4", ".wav")
#     video.audio.write_audiofile(audio_path)
#     return tmp_path, audio_path  # Retourner également le chemin de la vidéo originale

# # Fonction de transcription Whisper avec génération des sous-titres
# def generate_subtitles(audio_path, language="fr"):
#     result = model.transcribe(audio_path, language=language, verbose=True)
#     segments = result['segments']

#     # Génération du fichier .srt
#     subtitles = []
#     for segment in segments:
#         start = timedelta(seconds=segment['start'])
#         end = timedelta(seconds=segment['end'])
#         content = segment['text']
#         subtitle = srt.Subtitle(index=len(subtitles) + 1, start=start, end=end, content=content)
#         subtitles.append(subtitle)
    
#     return srt.compose(subtitles)

# # Fonction pour ajouter les sous-titres à une vidéo avec ffmpeg
# def add_subtitles_to_video(video_path, srt_path):
#     output_dir = Path("videos_with_subs")
#     output_dir.mkdir(exist_ok=True)
#     output_path = output_dir / Path(video_path).name.replace(".mp4", "_with_subs.mp4")
    
#     command = [
#         "ffmpeg", "-i", video_path, "-vf", f"subtitles={srt_path}", str(output_path)
#     ]
#     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     if result.returncode != 0:
#         st.error(f"Erreur lors de l'intégration des sous-titres : {result.stderr.decode('utf-8')}")
#     else:
#         return str(output_path)

# # Interface Streamlit
# def main():
#     st.title("Générateur de Sous-titres pour Vidéos")

#     # Sélection de la langue de transcription
#     transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Chargement du fichier vidéo
#     video_file = st.file_uploader("Téléchargez une vidéo", type=["mp4", "mov", "avi"])

#     if video_file:
#         # Afficher la vidéo d'origine
#         st.video(video_file)

#         if st.button("Générer les sous-titres et les intégrer à la vidéo"):
#             with st.spinner("Transcription et génération des sous-titres en cours..."):
#                 video_path, audio_path = extract_audio_from_video(video_file)
#                 subtitles = generate_subtitles(audio_path, language=transcription_language)
                
#                 # Sauvegarder le fichier .srt
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as srt_file:
#                     srt_file.write(subtitles.encode("utf-8"))
#                     srt_path = srt_file.name
                
#                 # Intégrer les sous-titres à la vidéo
#                 video_with_subs_path = add_subtitles_to_video(video_path, srt_path)

#                 if video_with_subs_path and os.path.exists(video_with_subs_path):
#                     st.success("Sous-titres générés et intégrés avec succès à la vidéo !")
#                     st.video(video_with_subs_path)
#                 else:
#                     st.error("Échec de la génération de la vidéo avec sous-titres.")

# if __name__ == "__main__":
#     main()


# import os
# import streamlit as st
# import whisper
# from googletrans import Translator
# from moviepy.editor import VideoFileClip
# import tempfile
# import srt
# from datetime import timedelta
# import subprocess
# from pathlib import Path

# # Initialisation du modèle Whisper et du traducteur
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")
#     st.stop()

# # Fonction pour extraire l'audio d'une vidéo en utilisant des chemins relatifs
# def extract_audio_from_video(video_file):
#     try:
#         video_path = Path("uploaded_videos") / video_file.name
#         audio_path = video_path.with_suffix(".wav")
        
#         # Assurer que le répertoire relatif "uploaded_videos" existe
#         video_path.parent.mkdir(exist_ok=True)

#         # Sauvegarder le fichier vidéo
#         with open(video_path, "wb") as f:
#             f.write(video_file.read())
        
#         # Extraire l'audio
#         video = VideoFileClip(str(video_path))
#         video.audio.write_audiofile(str(audio_path))
#         return str(video_path), str(audio_path)
#     except Exception as e:
#         st.error(f"Erreur lors de l'extraction de l'audio : {e}")
#         return None, None

# # Fonction pour ajouter les sous-titres à une vidéo avec ffmpeg (chemins relatifs)
# # def add_subtitles_to_video(video_path, srt_path):
# #     try:
# #         output_dir = Path("videos_with_subs")
# #         output_dir.mkdir(exist_ok=True)
# #         output_path = output_dir / Path(video_path).name.replace(".mp4", "_with_subs.mp4")
        
# #         command = [
# #             "ffmpeg", "-i", video_path, "-vf", f"subtitles={srt_path}", str(output_path)
# #         ]
# #         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# #         if result.returncode != 0:
# #             st.error(f"Erreur lors de l'intégration des sous-titres : {result.stderr.decode('utf-8')}")
# #             return None
# #         return str(output_path)
# #     except Exception as e:
# #         st.error(f"Erreur lors de l'intégration des sous-titres à la vidéo : {e}")
# #         return None

# # Fonction pour ajouter les sous-titres à une vidéo avec ffmpeg (chemins relatifs)
# def add_subtitles_to_video(video_path, srt_path):
#     try:
#         output_dir = Path("videos_with_subs")
#         output_dir.mkdir(exist_ok=True)

#         # Créer le nom de fichier de sortie en remplaçant les espaces
#         video_filename = Path(video_path).stem.replace(" ", "_") + "_with_subs.mp4"
#         output_path = output_dir / video_filename

#         # Commande pour FFmpeg avec guillemets autour des chemins
#         command = [
#             "ffmpeg",
#             "-i", str(Path(video_path).absolute()),
#             "-vf", f"subtitles='{str(Path(srt_path).absolute())}'",
#             str(output_path.absolute())
#         ]

#         # Exécuter la commande FFmpeg
#         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         if result.returncode != 0:
#             print(f"Erreur lors de l'intégration des sous-titres : {result.stderr.decode('utf-8')}")
#             return None
#         return str(output_path)
#     except Exception as e:
#         print(f"Erreur lors de l'intégration des sous-titres à la vidéo : {e}")
#         return None
# # Fonction de transcription Whisper
# def generate_subtitles(audio_path, language="fr"):
#     try:
#         result = model.transcribe(audio_path, language=language, verbose=True)
#         segments = result['segments']

#         # Génération du fichier .srt
#         subtitles = []
#         for segment in segments:
#             start = timedelta(seconds=segment['start'])
#             end = timedelta(seconds=segment['end'])
#             content = segment['text']
#             subtitle = srt.Subtitle(index=len(subtitles) + 1, start=start, end=end, content=content)
#             subtitles.append(subtitle)
        
#         return srt.compose(subtitles)
#     except Exception as e:
#         st.error(f"Erreur lors de la transcription : {e}")
#         return None

# # Interface Streamlit
# def main():
#     st.title("Générateur de Sous-titres pour Vidéos")

#     # Sélection de la langue de transcription
#     transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Chargement du fichier vidéo
#     video_file = st.file_uploader("Téléchargez une vidéo", type=["mp4", "mov", "avi"])

#     if video_file:
#         # Afficher la vidéo d'origine
#         st.video(video_file)

#         if st.button("Générer les sous-titres et les intégrer à la vidéo"):
#             with st.spinner("Transcription et génération des sous-titres en cours..."):
#                 video_path, audio_path = extract_audio_from_video(video_file)

#                 if not audio_path:
#                     st.error("Erreur lors de l'extraction de l'audio.")
#                     return

#                 subtitles = generate_subtitles(audio_path, language=transcription_language)

#                 if subtitles:
#                     # Sauvegarder le fichier .srt dans le répertoire courant
#                     srt_path = Path("subtitles") / f"{Path(video_file.name).stem}.srt"
#                     srt_path.parent.mkdir(exist_ok=True)

#                     with open(srt_path, "w", encoding="utf-8") as srt_file:
#                         srt_file.write(subtitles)

#                     # Intégrer les sous-titres à la vidéo
#                     video_with_subs_path = add_subtitles_to_video(video_path, str(srt_path))

#                     if video_with_subs_path and os.path.exists(video_with_subs_path):
#                         st.success("Sous-titres générés et intégrés avec succès à la vidéo !")
#                         st.video(video_with_subs_path)
#                     else:
#                         st.error("Échec de la génération de la vidéo avec sous-titres.")
#                 else:
#                     st.error("Échec de la transcription audio.")

# if __name__ == "__main__":
#     main()



# import streamlit as st
# import whisper
# from googletrans import Translator, LANGUAGES
# from moviepy.editor import VideoFileClip
# import tempfile
# import os
# import srt
# from datetime import timedelta
# import threading
# import time

# # Initialisation du modèle Whisper
# translator = Translator()
# try:
#     model = whisper.load_model("base")
# except Exception as e:
#     st.error(f"Erreur lors du chargement du modèle Whisper : {e}")

# # Fonction pour extraire l'audio d'une vidéo
# def extract_audio_from_video(video_file):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
#         tmp.write(video_file.read())
#         tmp_path = tmp.name
#     video = VideoFileClip(tmp_path)
#     audio_path = tmp_path.replace(".mp4", ".wav")
#     video.audio.write_audiofile(audio_path)
#     return audio_path

# # Fonction de transcription Whisper avec génération des sous-titres
# def generate_subtitles(audio_path, language="fr"):
#     result = model.transcribe(audio_path, language=language, verbose=True)
#     segments = result['segments']

#     # Génération des sous-titres
#     subtitles = []
#     for segment in segments:
#         start = segment['start']
#         end = segment['end']
#         content = segment['text']
#         subtitles.append((start, end, content))
    
#     return subtitles

# # Fonction pour afficher les sous-titres en temps réel
# def display_subtitles(subtitles):
#     start_time = time.time()
#     for start, end, content in subtitles:
#         # Attendre le bon moment pour afficher le sous-titre
#         while time.time() - start_time < start:
#             time.sleep(0.1)
#         st.write(content)
#         # Attendre la fin du sous-titre avant de passer au suivant
#         while time.time() - start_time < end:
#             time.sleep(0.1)

# # Interface Streamlit
# def main():
#     st.title("Générateur de Sous-titres pour Vidéos")

#     # Sélection de la langue de transcription
#     transcription_language = st.sidebar.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])

#     # Chargement du fichier vidéo
#     video_file = st.file_uploader("Téléchargez une vidéo", type=["mp4", "mov", "avi"])

#     if video_file:
#         # Afficher la vidéo
#         st.video(video_file)

#         if st.button("Générer les sous-titres"):
#             with st.spinner("Transcription en cours..."):
#                 audio_path = extract_audio_from_video(video_file)
#                 subtitles = generate_subtitles(audio_path, language=transcription_language)
                
#                 # Affichage des sous-titres dans un thread séparé
#                 threading.Thread(target=display_subtitles, args=(subtitles,)).start()

#                 # Sauvegarder le fichier .srt
#                 srt_content = srt.compose([srt.Subtitle(index=i+1, start=timedelta(seconds=start), end=timedelta(seconds=end), content=content) for i, (start, end, content) in enumerate(subtitles)])
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as srt_file:
#                     srt_file.write(srt_content.encode("utf-8"))
#                     srt_path = srt_file.name
                
#                 st.success("Sous-titres générés avec succès !")
#                 st.download_button("Télécharger les sous-titres (.srt)", data=srt_content, file_name="sous-titres.srt")

# if __name__ == "__main__":
#     main()
