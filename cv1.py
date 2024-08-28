import streamlit as st
import joblib
import numpy as np
import PyPDF2
from docx import Document

# Charger le modèle pré-entraîné
model = joblib.load('optimized_random_forest_model.pkl')

# Fonction pour prétraiter les données du CV
def preprocess_cv(cv_text):
    # Implémentez ici l'extraction de caractéristiques à partir du texte du CV
    # Cela peut être du comptage de mots, du TF-IDF, ou autre extraction pertinente
    features = np.random.rand(15)  # Exemple fictif, à remplacer par votre méthode d'extraction
    return features

# Fonction pour prédire la classification du CV
def classify_cv(cv_text):
    features = preprocess_cv(cv_text)
    prediction = model.predict([features])
    return prediction[0]

# Interface utilisateur Streamlit
st.title('Classification Automatique de CV')

uploaded_file = st.file_uploader("Téléchargez votre CV", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Lire le contenu du fichier
    if uploaded_file.type == "text/plain":
        cv_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        # Extraire le texte du PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        cv_text = ""
        for page in pdf_reader.pages:
            cv_text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        cv_text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Format de fichier non supporté")
        cv_text = ""

    if cv_text:
        # Afficher un aperçu du CV
        st.subheader("Aperçu du CV")
        st.text(cv_text)
        
        if st.button('Classify'):
            # Faire la prédiction
            result = classify_cv(cv_text)
            st.write(f'La classification du CV est: {result}')
