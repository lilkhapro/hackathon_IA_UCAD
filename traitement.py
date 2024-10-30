from textblob import TextBlob
from googletrans import Translator, LANGUAGES
import PyPDF2
import docx

def extract_text_from_word(word_file):
    doc = docx.Document(word_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Fonction d'analyse des sentiments
def analyze_sentiment(text):
    try:
        if not text.strip():
            return 0.0, 0.0  # Pas de sentiment si le texte est vide
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except Exception as e:
        return f"Erreur lors de l'analyse de sentiment : {e}", 0.0


# Fonction de traduction avec gestion des erreurs
def translate_transcription(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        return f"Erreur lors de la traduction : {e}" 

# Vérifier si la langue est supportée
def is_language_supported(language_code):
    return language_code in LANGUAGES.values()
