# This file contains the utility functions 
# Create File and write the prepositions in the file
def save_initial_prepositions_to_file(file_path):
    """
    Saves the given initial list of prepositions to a text file. This is a setup function
    that is intended to be run once to create the initial file of prepositions.

    :param prepositions: A list of prepositions to initialize the file with.
    :param file_path: The path to the file where the prepositions will be saved.
    """

        
    valid_prepositions = ["on","for","of","to","at","in","with","by"]

    # # Path to save the prepositions text file
    # file_path = '/Users/Checkout/Desktop/tech-screener-nithin/prepositions.txt'

    # Save the valid prepositions to a text file
    with open(file_path, 'w') as file:
        for prep in valid_prepositions:
            file.write(prep + '\n')


# Load the prepositions from the file and return a set of prepositions
def load_prepositions_from_file(file_path):
    """
    Loads prepositions from a text file into a set. This set is used to check if a token is
    a valid preposition during the feature extraction process.

    :param file_path: The path to the file to read prepositions from.
    :return: A set of prepositions.
    """
    with open(file_path, 'r') as file:
        return {line.strip() for line in file}


'''Below function is not intended for the requirements of the task but is included
   for completeness to modify the prepositions in the file'''
   
# Update the prepositions file with new prepositions if needed in future
def update_prepositions_file(file_path, new_prepositions):
    """
    Adds new prepositions to the existing file of prepositions. This function allows for 
    the list of prepositions to be updated as needed.
    
    :param file_path: The path to the file where the prepositions are saved.
    :param new_prepositions: A list of new prepositions to add to the file.
    """
    current_prepositions = load_prepositions_from_file(file_path)
    with open(file_path, 'a') as file:
        for prep in new_prepositions:
            if prep not in current_prepositions:
                file.write(prep + '\n')
                



