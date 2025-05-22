class Character:
    """Class representing a D&D character with all its attributes and methods."""
    
    def __init__(self, name="", race="Human", character_class="Fighter", background="Soldier", 
                 ability_scores=None, level=1, **kwargs):
        """
        Initialize a new character with default or provided values.
        
        Args:
            name (str): Character name
            race (str): Character race
            character_class (str): Character class
            background (str): Character background
            ability_scores (dict): Dictionary of ability scores
            level (int): Character level
            **kwargs: Additional character attributes
        """
        self.name = name
        self.race = race
        self.character_class = character_class
        self.background = background
        self.ability_scores = ability_scores or {}
        self.level = level
        
        # Add any additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convert character object to dictionary for serialization."""
        return {
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "background": self.background,
            "ability_scores": self.ability_scores,
            "level": self.level
        }
    
    def get_ability_modifier(self, ability):
        """Calculate and return ability modifier based on ability score."""
        if ability not in self.ability_scores:
            return 0
        
        score = self.ability_scores[ability]
        return (score - 10) // 2
    
    def __str__(self):
        """String representation of character."""
        return f"{self.name} - Level {self.level} {self.race} {self.character_class}"
