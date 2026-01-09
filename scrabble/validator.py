"""Word validator for Scrabble game with Dutch word dictionary."""

from typing import Set, Optional
import os


class WordValidator:
    """Validates words against a Dutch dictionary."""

    def __init__(self, dictionary_file: Optional[str] = None):
        """Initialize the word validator.
        
        Args:
            dictionary_file: Path to dictionary file (optional)
        """
        self.valid_words: Set[str] = set()
        if dictionary_file and os.path.exists(dictionary_file):
            self._load_dictionary(dictionary_file)
        else:
            # Initialize with a basic set of common Dutch words
            self._initialize_basic_dictionary()

    def _load_dictionary(self, file_path: str) -> None:
        """Load dictionary from file.
        
        Args:
            file_path: Path to dictionary file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().upper()
                    if word and len(word) >= 2:
                        self.valid_words.add(word)
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            self._initialize_basic_dictionary()

    def _initialize_basic_dictionary(self) -> None:
        """Initialize a basic dictionary with common Dutch words for testing."""
        # Common Dutch words for testing purposes
        basic_words = [
            # Basic words
            "DE", "HET", "EEN", "EN", "VAN", "IN", "OP", "TE", "DAT", "DIE",
            "IS", "VOOR", "MET", "AAN", "ALS", "BIJ", "ZE", "ER", "HIJ", "ZIJN",
            "WE", "JE", "HAD", "DIT", "WAT", "NIET", "WIE", "ZO", "MAAR", "OM",
            
            # Common nouns
            "HUIS", "MAN", "VROUW", "KIND", "DAG", "JAAR", "TIJD", "WERK", "LAND",
            "HAND", "WATER", "BOOT", "AUTO", "FIETS", "BOEK", "TAFEL", "STOEL",
            "DEUR", "RAAM", "BOOM", "BLOEM", "KAT", "HOND", "VOGEL", "VIS",
            
            # Common verbs
            "ZIJN", "HEBBEN", "DOEN", "GAAN", "KOMEN", "ZIEN", "WETEN", "KUNNEN",
            "WORDEN", "MAKEN", "GEVEN", "NEMEN", "WILLEN", "ZEGGEN", "VINDEN",
            "KIJKEN", "LOPEN", "ETEN", "DRINKEN", "SLAPEN", "WERKEN", "SPELEN",
            
            # Common adjectives
            "GOED", "GROOT", "KLEIN", "NIEUW", "OUD", "JONG", "MOOI", "LANG",
            "KORT", "HOOG", "LAAG", "BREED", "SMAL", "WARM", "KOUD", "LICHT",
            "DONKER", "ZWART", "WIT", "ROOD", "BLAUW", "GROEN", "GEEL",
            
            # Numbers and common words
            "EEN", "TWEE", "DRIE", "VIER", "VIJF", "ZES", "ZEVEN", "ACHT", "NEGEN", "TIEN",
            
            # Additional common words
            "WOORDENBOEK", "SPEL", "SCRABBLE", "LETTER", "WOORD", "PUNT", "SCORE",
            "BORD", "VELD", "ROW", "KOLOM", "SPELER", "BEURT", "REGEL", "CONTROLE",
            
            # More words for variety
            "HALLO", "DAG", "AVOND", "NACHT", "WEEK", "MAAND", "WINTER", "ZOMER",
            "LENTE", "HERFST", "ZONDAG", "MAANDAG", "DINSDAG", "WOENSDAG",
            "DONDERDAG", "VRIJDAG", "ZATERDAG", "JANUARI", "FEBRUARI", "MAART",
            "APRIL", "MEI", "JUNI", "JULI", "AUGUSTUS", "SEPTEMBER", "OKTOBER",
            "NOVEMBER", "DECEMBER", "SCHOOL", "KLAS", "LERAAR", "LEERLING",
            "COMPUTER", "TELEFOON", "INTERNET", "EMAIL", "BRIEF", "PAPIER",
            "PEN", "POTLOOD", "MUUR", "VLOER", "PLAFOND", "STRAAT", "WEG",
            "PAD", "BRUG", "STAD", "DORP", "MARKT", "WINKEL", "PRIJS",
            "GELD", "EURO", "BANK", "REIS", "VAKANTIE", "HOTEL", "RESTAURANT",
            "KOFFIE", "THEE", "BROOD", "KAAS", "MELK", "WIJN", "BIER",
            "VLEES", "GROENTE", "FRUIT", "APPEL", "PEER", "BANAAN",
        ]
        
        self.valid_words = set(basic_words)

    def add_word(self, word: str) -> None:
        """Add a word to the dictionary.
        
        Args:
            word: Word to add
        """
        self.valid_words.add(word.upper())

    def is_valid_word(self, word: str) -> bool:
        """Check if a word is valid.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is valid, False otherwise
        """
        if not word or len(word) < 2:
            return False
        return word.upper() in self.valid_words

    def get_word_count(self) -> int:
        """Get the number of words in the dictionary.
        
        Returns:
            Number of words
        """
        return len(self.valid_words)
