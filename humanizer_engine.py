import random
import re
import json
from pathlib import Path

class Vocabulary:
    """Clean vocabulary manager - loads from external files"""
    def __init__(self):
        self.thesaurus = {}
        self.frequent_words = set()
        self.slang_words = set()
        self.stop_words = self._get_stop_words()
        self._load_vocabulary()
    
    def _get_stop_words(self):
        """Common words that should never be replaced"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    def _load_vocabulary(self):
        """Load vocabulary from external JSON files"""
        try:
            with open('data/unified_vocabulary.json', 'r') as f:
                data = json.load(f)
                self.thesaurus = data.get('thesaurus', {})
                self.frequent_words = set(data.get('frequent_words', []))
                self.slang_words = set(data.get('slang_words', []))
                print(f"✅ Loaded {len(self.thesaurus)} synonyms, {len(self.frequent_words)} frequent words")
        except FileNotFoundError:
            print("⚠️ Vocabulary file not found, using fallback")
            self._load_fallback()
    
    def _load_fallback(self):
        """Fallback vocabulary"""
        self.thesaurus = {
            'good': ['great', 'excellent', 'fine', 'positive'],
            'important': ['crucial', 'vital', 'essential', 'key'],
            'help': ['assist', 'support', 'aid', 'facilitate'],
            'use': ['utilize', 'employ', 'apply', 'implement'],
            'show': ['demonstrate', 'indicate', 'reveal', 'display'],
            'make': ['create', 'produce', 'generate', 'construct'],
            'get': ['obtain', 'acquire', 'secure', 'gather'],
            'think': ['believe', 'consider', 'reckon', 'suppose'],
            'need': ['require', 'demand', 'necessitate'],
            'know': ['understand', 'comprehend', 'grasp', 'realize']
        }
    
    def get_synonym(self, word):
        """Get a clean synonym for a word"""
        word_lower = word.lower()
        if word_lower in self.thesaurus and self.thesaurus[word_lower]:
            synonyms = self.thesaurus[word_lower]
            if isinstance(synonyms, list) and synonyms:
                return random.choice(synonyms)
        return word


class StealthHumanizer:
    """Clean, modular humanization engine"""
    def __init__(self):
        self.vocab = Vocabulary()
        self.contractions = self._get_contractions()
        print("✅ Humanizer Engine Ready")
    
    def _get_contractions(self):
        """Clean contractions"""
        return {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't"
        }
    
    def _is_content_word(self, word):
        """Check if a word should be replaced"""
        clean = word.strip(string.punctuation).lower()
        return (clean and 
                len(clean) > 3 and 
                clean not in self.vocab.stop_words)
    
    def _apply_synonyms(self, text, rate=0.30):
        """Apply synonyms with controlled rate"""
        words = text.split()
        new_words = []
        
        for word in words:
            if self._is_content_word(word):
                if random.random() < rate:
                    syn = self.vocab.get_synonym(word)
                    if syn != word.lower():
                        # Preserve case and punctuation
                        if word[0].isupper():
                            syn = syn.capitalize()
                        if word[-1] in string.punctuation:
                            syn = syn + word[-1]
                        new_words.append(syn)
                        continue
            new_words.append(word)
        
        return ' '.join(new_words)
    
    def _apply_contractions(self, text, rate=0.25):
        """Apply contractions naturally"""
        result = text
        for formal, casual in self.contractions.items():
            if random.random() < rate:
                result = result.replace(formal, casual)
        return result
    
    def _clean_text(self, text):
        """Clean up the text"""
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r',\s*,', ',', text)
        if text and text[-1] not in '.!?':
            text += '.'
        return text
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Apply transformations
            result = self._apply_synonyms(text, rate=0.30)
            result = self._apply_contractions(result, rate=0.25)
            result = self._clean_text(result)
            
            # Safety check
            if not isinstance(result, str) or len(result) < 10:
                return text
            
            if result.lower() in ["true", "false"]:
                return text
            
            return result
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def get_stealth_score(self, text):
        """Calculate human-like score"""
        if not text:
            return 0
        
        score = 70
        words = text.split()
        if len(words) == 0:
            return 50
        
        if any("'t" in word or "'m" in word for word in words):
            score += 10
        if len(set(words)) / len(words) > 0.5:
            score += 10
        
        sentences = [s for s in text.split(". ") if s]
        if len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 8:
                score += 10
        
        return min(score, 99)
