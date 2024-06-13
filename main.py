# Importing Pandas Library to read the data from the CSV file
import pandas as pd
import utils
import spacy
import json

# File path of the prepositions file, input file and output file
pre_file_path = 'prepositions.txt'
input_file_path = 'sentences.csv'
output_file_path = 'output.jsonl'


''' Reading the data from the CSV file as a dataframe is standard practice 
    to visualize the data and understand the structure of the data 
    later we can convert it to dictionary'''
    
data = pd.read_csv(input_file_path)

# Convert DataFrame to a dictionary for easier processing
sentences_dict = pd.Series(data.Sentence.values, index=data.Id).to_dict()

'''Storing the prepositions in a File and reading the file (prepositions.txt) 
   to get the list of prepositions as it is not suggested to hard code the prepositions in the code
   File can be created manually or can use write() function to write the prepositions in the file'''

# Prepositions are loaded from the file and stored in a set
prepositions =  utils.load_prepositions_from_file(pre_file_path)
   
# Load the SpaCy model required
def ensure_model_loaded(model_name="en_core_web_sm"):
    try:
        spacy.load(model_name)
    except OSError:
        print(f"Downloading the SpaCy model {model_name}...")
        spacy.cli.download(model_name)
        print(f"Model {model_name} downloaded.")

ensure_model_loaded()

nlp = spacy.load('en_core_web_sm')

def extract_specific_features(doc, preposition_index):
    """
    This function extracts a predefined set of features centered around a specific preposition
    within a sentence. The features include sequences of words (tokens) and their corresponding
    part-of-speech (POS) tags, considering both the immediate and broader context of the preposition.

    Parameters:
    - doc (spacy.tokens.doc.Doc): A processed sentence as a SpaCy Doc object, which contains
      tokens and their linguistic annotations.
    - preposition_index (int): The index of the target preposition within the Doc object,
      around which features will be extracted.

    Returns:
    - List[str]: A comprehensive list of extracted features, comprising both token sequences
      and POS tag sequences, formulated based on specified patterns that capture varying
      contextual spans around the preposition.
    """
    features = []

    # Prepare lists of tokens and their POS tags surrounding the target preposition,
    # ensuring to handle sentence boundaries by providing empty strings for out-of-range indices.
    tokens = [doc[i].text if 0 <= i < len(doc) else '' for i in range(preposition_index - 2, preposition_index + 3)]
    pos_tags = [doc[i].tag_ if 0 <= i < len(doc) else '' for i in range(preposition_index - 2, preposition_index + 3)]

    # Define specific patterns for extracting features. These patterns are tuples indicating
    # relative positions of tokens to include in each feature, relative to the preposition.
    token_patterns = [
        (1, 2),    
        (2, 3),    
        (1, 2, 3), 
        (0, 1, 2),
        (2, 3, 4),
        (0, 1, 2, 3, 4)
    ]

    # Apply the same patterns for generating POS tag sequences as for token sequences.
    pos_patterns = token_patterns

    # Extract token-based features based on the defined patterns.
    for pattern in token_patterns:
        feature = ' '.join(tokens[i] for i in pattern if tokens[i]).strip()
        if feature:  # Add the feature to the list if it's not an empty string.
            features.append(feature)

    # extract POS tag-based features.
    for pattern in pos_patterns:
        feature = ' '.join(pos_tags[i] for i in pattern if pos_tags[i]).strip()
        if feature:  # Again, only add non-empty feature strings to the list.
            features.append(feature)

    return features


def create_features(sentences, prepositions, output_path):
    """
    Extracts features around specified prepositions in given sentences and saves them to a JSONL file.

    Parameters:
    - sentences (dict): A dictionary where each key is a sentence ID and each value is the corresponding sentence text.
    - prepositions (set): A set of prepositions to look for in the sentences. The preposition 'to' is treated specially to exclude cases 
      where it functions as part of an infinitive verb.
    - output_path (str): Path to the output JSONL file where extracted features will be saved.
    
    This function processes each sentence to identify occurrences of the specified prepositions, extracts a set of features for each occurrence,
    and writes these features to the specified output file in JSONL format.Each line in the output file represents a set of features related to 
    a single preposition occurrence, including the sentence ID, the preposition itself, and the extracted features.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        # Iterate through each sentence provided in the input dictionary.
        for sentence_id, sentence_text in sentences.items():
            # Process the sentence text with spaCy to obtain a Doc object.
            doc = nlp(sentence_text)
            
            # Iterate through each token in the Doc to find specified prepositions.
            for token in doc:
                # Check if the token is a preposition of interest.
                # Special case for 'to': exclude it when it precedes a verb
                if token.lower_ in prepositions and not (token.lower_ == "to" and token.i < len(doc) - 1 and doc[token.i + 1].pos_ == "VERB"):
                    # Construct the feature ID from the sentence ID and token index.
                    feature_id = f"{sentence_id}_{token.i}"
                    
                    # Extract features around the current token using a helper function.
                    features = extract_specific_features(doc, token.i)
                    
                    # Compile the feature data into a dictionary.
                    feature_data = {
                        "id": feature_id,
                        "prep": token.text,
                        "features": features
                    }
                    
                    # Write the feature data to the output file as a JSON object.
                    file.write(json.dumps(feature_data) + '\n')


# Process sentences and save features to JSONL
create_features(sentences_dict, prepositions, output_path=output_file_path)

print(f"Features have been successfully extracted and saved to {output_file_path}.")
