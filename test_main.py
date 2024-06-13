import pytest
from main import extract_specific_features, create_features, ensure_model_loaded
import spacy
import json
import os

# Ensure the SpaCy model is loaded before running any tests
ensure_model_loaded()

# Initialize the SpaCy model once for all tests to use.
nlp = spacy.load("en_core_web_sm")

# Simplified setup and teardown environment using pytest fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_environment():
    
    # Setup environment before any tests run
    sentences = ["1,The cat sat on the mat.", "2,She went to the park."]
    prepositions = ["on", "to", "in"]
    with open("test_sentences.csv", "w") as f:
        f.write("\n".join(sentences))
    with open("test_prepositions.txt", "w") as f:
        f.write("\n".join(prepositions))
        
    # Wait for all tests to complete
    yield
    # Teardown environment
    os.remove("test_sentences.csv")
    os.remove("test_prepositions.txt")
    if os.path.exists("test_output.jsonl"):  
        os.remove("test_output.jsonl")

# Test to ensure prepositions are correctly identified within sentences.
def test_prepositions_identification():
    doc = nlp("The cat sat on the mat.")
    prepositions = ["on"]
    identified_preps = [token.text for token in doc if token.text in prepositions]
    assert identified_preps == prepositions, "Prepositions not correctly identified."

# Test if specific features around a preposition are correctly extracted.
def test_feature_extraction_for_preposition():
    doc = nlp("The cat sat on the mat.")
    # Assuming 'on' is the preposition at index 3
    features = extract_specific_features(doc, 3)
    expected_features = ["cat sat on", "on the mat"]
    assert all(feature in features for feature in expected_features), "Features not extracted correctly."

# Test if the output file is created and formatted correctly after the feature extraction process.
def test_output_file_creation_and_format():
    # Load sentences from CSV into a dictionary
    sentences = {}
    with open("test_sentences.csv", "r") as f:
        for line in f:
            sentence_id, sentence_text = line.strip().split(',', 1)
            sentences[int(sentence_id)] = sentence_text  # Convert IDs to int for consistency

    # Load prepositions from txt file into a set
    prepositions = set()
    with open("test_prepositions.txt", "r") as f:
        prepositions = {line.strip() for line in f}

    # Call create_features with correctly loaded data
    create_features(sentences, prepositions, "test_output.jsonl")

    # Assert that the output file was created and verify its format
    assert os.path.exists("test_output.jsonl"), "Output file was not created."
    with open("test_output.jsonl", "r") as file:
        for line in file:
            assert json.loads(line), "Output file is not in JSON lines format."

# Test if the output data contains correct and complete information.
def test_output_data_integrity():
    with open("test_output.jsonl", "r") as file:
        data = [json.loads(line) for line in file]
    assert all("id" in entry and "prep" in entry and "features" in entry for entry in data), "Output data missing required fields."
