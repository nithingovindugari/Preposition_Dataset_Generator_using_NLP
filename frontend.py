import streamlit as st
from main import extract_specific_features, create_features, ensure_model_loaded
import spacy

# Load the SpaCy model
ensure_model_loaded()
nlp = spacy.load("en_core_web_sm")

# Streamlit app title
st.title('Preposition Feature Extractor')

# User input: sentence
user_input = st.text_area("Enter a sentence to extract features from:", "The quick brown fox jumps over the lazy dog.")

# Process the sentence
doc = nlp(user_input)

# Identify prepositions and their indices
prepositions = ["on", "to", "in", "for", "with", "by", "at"]  # Example list
identified_preps = [(i, token.text) for i, token in enumerate(doc) if token.text in prepositions]

# Display identified prepositions to the user
if identified_preps:
    st.write("Identified prepositions and their positions:")
    for pos, prep in identified_preps:
        st.write(f"{prep} (Position: {pos})")

        # Optionally, show extracted features for each preposition
        features = extract_specific_features(doc, pos)
        st.write("Extracted Features:")
        st.write(features)
else:
    st.write("No prepositions identified in the sentence.")
