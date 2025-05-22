import os
import json
from character import Character

class DataManager:
    """Class for managing character data storage and retrieval."""
    
    def __init__(self, data_dir="character_data"):
        """
        Initialize the data manager with a data directory.
        
        Args:
            data_dir (str): Directory where character data will be stored
        """
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_character(self, character):
        """
        Save a character to a JSON file.
        
        Args:
            character (Character): Character object to save
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Convert character to dictionary
            character_dict = character.to_dict()
            
            # Create a safe filename from character name
            safe_name = "".join(x for x in character.name if x.isalnum() or x in " _-")
            safe_name = safe_name.replace(" ", "_")
            
            # If name is empty, use a default name
            if not safe_name:
                safe_name = f"{character.race}_{character.character_class}"
            
            file_path = os.path.join(self.data_dir, f"{safe_name}.json")
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(character_dict, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving character: {e}")
            return False
    
    def load_character(self, filename):
        """
        Load a character from a JSON file.
        
        Args:
            filename (str): Name of the file to load
            
        Returns:
            Character: Loaded character object or None if loading failed
        """
        try:
            file_path = os.path.join(self.data_dir, filename)
            
            with open(file_path, 'r') as f:
                character_dict = json.load(f)
            
            # Create a Character object from the dictionary
            return Character(**character_dict)
        except Exception as e:
            print(f"Error loading character: {e}")
            return None
    
    def get_saved_characters(self):
        """
        Get a list of all saved characters.
        
        Returns:
            list: List of dictionaries containing character data
        """
        characters = []
        
        try:
            # Get all JSON files in the data directory
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.data_dir, filename)
                    
                    with open(file_path, 'r') as f:
                        character_dict = json.load(f)
                        characters.append(character_dict)
        except Exception as e:
            print(f"Error getting saved characters: {e}")
        
        return characters
    
    def delete_character(self, character_name):
        """
        Delete a character file.
        
        Args:
            character_name (str): Name of the character to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            # Create a safe filename from character name
            safe_name = "".join(x for x in character_name if x.isalnum() or x in " _-")
            safe_name = safe_name.replace(" ", "_")
            
            file_path = os.path.join(self.data_dir, f"{safe_name}.json")
            
            # Check if file exists before deleting
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting character: {e}")
            return False
