import streamlit as st
from traitement import *
from utils import *
from streamlit_option_menu import option_menu
import soundfile as sf
import sounddevice as sd

# Interface Streamlit
def main():

    # sation du markdown pour personnaliser la barre de navigation

    # Création de colonnes pour le logo et le menu
    col1, col2 = st.columns([1, 5])  # Ajuster les ratios pour définir l'espace entre le logo et le menu

    # Logo dans la première colonne
    with col1:
        st.image("logo.png", width=70)  # Taille du logo ajustée pour s'adapter à la barre de navigation

    # Menu dans la deuxième colonne
    with col2:
        selected = option_menu(
            menu_title=None,  # Titre retiré pour intégrer dans la navbar
            options=["Page d'accueil", "Traitement d'audio/vidéo", "Traitement de texte"],
            icons=["house", "upload", "file-earmark-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#F0F2D6"},
                "icon": {"color": "#191970", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#E1AD01","color": "black"}, 
                "nav-link-selected": {"background-color": "#E1AD01","color": "white"},
            },
        )
    
    # Gestion des états de session
    if 'transcription' not in st.session_state:
        st.session_state.transcription = None
        st.session_state.summary = None
        st.session_state.recordertranscription = None

    if selected == "Page d'accueil":
        st.title("ACCUEIL")
        st.write("""
Bienvenue sur **POLYGLOT_HUB**, votre outil tout-en-un pour la transcription et la traduction multilingue de fichiers audio, vidéo et texte. 
Que vous souhaitiez transcrire des conversations, traduire du contenu ou analyser des sentiments, notre plateforme est là pour vous aider.
""")

        st.subheader("Fonctionnalités Principales")
        st.markdown("""
- **Transcription Audio/Vidéo** : Transcrivez vos fichiers dans plusieurs langues.
- **Traduction Multilingue** : Traduisez du texte ou des transcriptions dans plus de 50 langues.
- **Analyse des Sentiments** : Obtenez des informations sur le ton et l'émotion d'un texte transcrit.
- **Synthèse Vocale** : Convertissez du texte en audio dans plusieurs langues.
- **Résumé Automatique** : Résumez automatiquement de longs textes.
""")

        st.subheader("Comment Utiliser l'Application")
        st.markdown("""
1. **Sélectionnez une fonctionnalité** dans le menu.
2. **Téléchargez votre fichier audio, vidéo ou texte** selon votre besoin.
3. **Cliquez sur les boutons d'action** pour transcrire, traduire, analyser ou résumer.
4. **Téléchargez les résultats** ou laissez des commentaires pour améliorer l'expérience.
""")

        st.subheader("Besoin d'aide ?")
        st.write("Contactez-nous à (mailto:ikg@gmail.com) pour toute question ou assistance.")

    
    elif selected == "Traitement d'audio/vidéo":
        st.header("Traitement audio et vidéo")  # Correction de la syntaxe pour afficher un titre
        
        # Sélection de l'option d'importation
        option = st.selectbox("Importer un audio ou vidéo", ["Importer un audio ou vidéo", "Enregistrement vocal"])

        if option == "Importer un audio ou vidéo":
            st.header("Importation de l'audio ou vidéo")
            st.markdown("Veuillez importer un audio ou une vidéo")
            audio_file = st.file_uploader("Téléchargez un fichier audio", type=["wav", "mp3", "mp4", "mov", "avi"])

            if 'transcription' not in st.session_state:
                st.session_state.transcription = None
                st.session_state.summary = None
                st.session_state.recordertranscription = None
            if audio_file:
                show_audio_or_video(audio_file)
                if st.button("Transcrire"):
                    st.session_state.transcription = transcribe_audio(audio_file)
                    text_transcription = st.session_state.transcription

            if st.session_state.transcription:
                st.text_area("Transcription :", value=st.session_state.transcription, height=200)
                text_transcription = st.session_state.transcription

                # Analyse des sentiments
                st.header("Analyse de sentiment et Subjectivité")
                sentiment_score, subjectivity_score = analyze_sentiment(st.session_state.transcription)
                st.write("Analyse de sentiment (score) :", sentiment_score)
                st.write("Subjectivité (score) :", subjectivity_score)

                # Résumé
                if st.button("Résumé"):
                    st.session_state.summary = summarize_text(st.session_state.transcription)
                
                if st.session_state.summary :
                    st.text_area("Résumé :", value=st.session_state.summary, height=200)
                    text_resume = st.session_state.summary
                    # Synthèse vocale de la traduction
                    # Sélection de la langue
                    st.header("Choisissez une langue pour la Synthèse vocale: ")
                    language = st.selectbox("Sélectionnez la langue de la transcription", ['en','fr'])
                    if st.button("Générer l'audio à partir du texte transcrit"):
                        # Conversion du texte en audio
                        text_to_speech(text_transcription,language)

                    if st.button("Générer l'audio à partir du résumé"):
                        # Conversion du texte en audio
                        text_to_speech(text_resume,language)
        if option == "Enregistrement vocal":
            st.header("Enregistrement vocal")
            st.markdown("Veuillez lancer l'enregistrement vocal")
            
            device_index = 19
            # Paramètres de l'enregistrement
            sample_rate = 44100
            duration = st.number_input("Durée d'enregistrement (en secondes)", min_value=1, max_value=60, value=5)

            if st.button("Démarrer l'enregistrement"):
                st.write("Enregistrement en cours...")
                audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64', device=device_index)
                sd.wait()
                
                # Sauvegarde de l'enregistrement
                audio_file_path = "enregistrement.wav"
                sf.write(audio_file_path, audio, sample_rate)

                st.write("Enregistrement terminé !")
                st.audio(audio_file_path)

                # Transcription de l'enregistrement
                with st.spinner("Transcription en cours..."):
                    st.session_state.recordertranscription = transcribe_audio(open(audio_file_path, "rb"))
                    

            # Transcription et analyse

            if st.session_state.recordertranscription:
                st.text_area("Transcription des paroles :", value=st.session_state.recordertranscription, height=200)
                sentiment_score, subjectivity_score = analyze_sentiment(st.session_state.recordertranscription)
                st.write("Analyse de sentiment (score) :", sentiment_score)
                st.write("Subjectivité (score) :", subjectivity_score)

                # Résumé du texte
                if st.button("Résumé"):
                    summary = summarize_text(st.session_state.recordertranscription)
                    st.text_area("Résumé :", value=summary, height=200)

                # Traduction

                # Génération de l'audio à partir de la transcription
                st.header("Selectionner la langue d'enregistrement")
                language = st.selectbox("Sélectionnez la langue", ['fr', 'en'])
                if st.button("Générer l'audio"):
                    text_to_speech(st.session_state.recordertranscription, language)
        st.title("Traitement audio/vidéo")
        
        option = st.selectbox("Choisissez une option", ["Importer un audio/vidéo", "Enregistrement vocal"])

        if option == "Importer un audio/vidéo":
            st.header("Importation d'un fichier audio/vidéo")
            audio_file = st.file_uploader("Téléchargez un fichier audio ou vidéo", type=["wav", "mp3", "mp4", "mov", "avi"])
            
            if audio_file:
                show_audio_or_video(audio_file)  # Cette fonction doit gérer l'affichage ou la lecture du média

                # Transcription
                transcription_language = st.selectbox("Choisissez la langue de transcription :", ["fr", "en", "wo"])
                if st.button("Transcrire"):
                    st.session_state.transcription = transcribe_audio(transcription_language, audio_file)
                    st.text_area("Transcription :", value=st.session_state.transcription, height=200)
    elif selected == "Traitement de texte":
        st.title("Traitement de texte")
        
        # Sélection du type de fichier à importer
        st.markdown("**Importer un fichier texte (PDF, Word, ou TXT)**")
        uploaded_file = st.file_uploader("Téléchargez un fichier", type=["pdf", "docx", "txt"])

        # Si un fichier est téléchargé
        if uploaded_file is not None:
            # Traitement des différents formats de fichiers
            if uploaded_file.type == "application/pdf":
                st.write("Fichier PDF importé.")
                text = extract_text_from_pdf(uploaded_file)

            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                st.write("Fichier Word importé.")
                text = extract_text_from_word(uploaded_file)

            elif uploaded_file.type == "text/plain":
                st.write("Fichier TXT importé.")
                text = uploaded_file.read().decode("utf-8")

            # Affichage du texte extrait
            st.text_area("Contenu du fichier :", value=text, height=300)
            
            if text:
                st.header("Choisissez une langue pour la Synthèse vocale: ")
                language = st.selectbox("Sélectionnez la langue de la transcription", ['en','fr'])
                if st.button("Générer l'audio à partir du texte extrait"):
                    # Conversion du texte en audio
                    text_to_speech(text_transcription,language)
            # Analyse de sentiment
            sentiment_score, subjectivity_score = analyze_sentiment(text)
            st.write("Analyse de sentiment (score) :", sentiment_score)
            st.write("Subjectivité (score) :", subjectivity_score)

            # Résumé
            if st.button("Résumé"):
                st.session_state.summary = summarize_text(text)
                st.text_area("Résumé :", value=st.session_state.summary, height=200)

            if st.session_state.summary:
                st.header("Choisissez une langue pour la Synthèse vocale: ")
                language = st.selectbox("Sélectionnez la langue de la transcription", ['en','fr'])
                if st.button("Générer l'audio à partir du résumé"):
                    # Conversion du texte en audio
                    text_to_speech(text_resume,language)


            if st.button("Traduire"):
                # Traduction
                target_language_name = st.selectbox("Choisissez la langue de traduction :", list(LANGUAGES.keys()))
                dest_language = LANGUAGES[target_language_name]
                translated_text = translate_transcription(st.session_state.transcription, dest_language)
                st.text_area("Traduction :", value=translated_text, height=200)


            # Synthèse vocale de la traduction
            language = st.selectbox("Sélectionnez la langue pour la synthèse vocale", ['fr', 'en', 'wo', 'dz', 'ru'])
            if st.button("Générer l'audio"):
                text_to_speech(text, language)

            # Recherche dans le texte
            st.header("Recherche dans le texte")
            search_query = st.text_input("Rechercher dans le texte :")
            if search_query and search_query in text:
                st.write(f"Le mot '{search_query}' a été trouvé dans le texte.")
            elif search_query:
                st.write(f"Le mot '{search_query}' n'a pas été trouvé.")

if __name__ == "__main__":
    main()
