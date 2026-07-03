import random
import re
import string
import json
from pathlib import Path

class Vocabulary:
    """Clean vocabulary manager - loads from external JSON"""
    def __init__(self):
        self.thesaurus = {}
        self.frequent_words = set()
        self.stop_words = self._get_stop_words()
        self._load_vocabulary()
    
    def _get_stop_words(self):
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    def _load_vocabulary(self):
        try:
            with open('data/unified_vocabulary.json', 'r') as f:
                data = json.load(f)
                self.thesaurus = data.get('thesaurus', {})
                self.frequent_words = set(data.get('frequent_words', []))
                print(f"✅ Loaded {len(self.thesaurus):,} synonyms from library")
        except FileNotFoundError:
            print("⚠️ Vocabulary file not found, using fallback")
            self._load_fallback()
    
    def _load_fallback(self):
        self.thesaurus = {
            'good': ['great', 'excellent', 'fine', 'positive', 'superior'],
            'important': ['crucial', 'vital', 'essential', 'key', 'significant'],
            'help': ['assist', 'support', 'aid', 'facilitate', 'guide'],
            'use': ['utilize', 'employ', 'apply', 'implement', 'leverage'],
            'show': ['demonstrate', 'indicate', 'reveal', 'display', 'exhibit'],
            'make': ['create', 'produce', 'generate', 'construct', 'develop'],
            'get': ['obtain', 'acquire', 'secure', 'gather', 'receive'],
            'think': ['believe', 'consider', 'reckon', 'suppose', 'assume'],
            'need': ['require', 'demand', 'necessitate', 'call for'],
            'know': ['understand', 'comprehend', 'grasp', 'realize', 'perceive'],
            'say': ['state', 'mention', 'remark', 'comment', 'declare'],
            'see': ['observe', 'notice', 'spot', 'witness', 'perceive'],
            'people': ['individuals', 'folks', 'citizens', 'humans', 'persons'],
            'respect': ['esteem', 'regard', 'admiration', 'appreciation'],
            'kindness': ['compassion', 'benevolence', 'warmth', 'charity'],
            'society': ['community', 'civilization', 'culture', 'nation'],
            'foundation': ['basis', 'base', 'cornerstone', 'bedrock', 'root'],
            'behavior': ['conduct', 'actions', 'demeanor', 'manners'],
            'values': ['principles', 'ethics', 'morals', 'ideals', 'standards']
        }
    
    def get_synonym(self, word):
        word_lower = word.lower()
        if word_lower in self.thesaurus and self.thesaurus[word_lower]:
            synonyms = self.thesaurus[word_lower]
            if isinstance(synonyms, list) and synonyms:
                # Prefer frequent words
                frequent_synonyms = [s for s in synonyms if s in self.frequent_words]
                if frequent_synonyms:
                    return random.choice(frequent_synonyms)
                return random.choice(synonyms)
        return word


class StealthHumanizer:
    """Clean humanization engine - NO TORCH NEEDED"""
    def __init__(self):
        print("✅ Humanizer Engine Ready (No AI models needed)")
        self.vocab = Vocabulary()
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't"
        }
        print(f"✅ Loaded {len(self.vocab.thesaurus):,} synonym entries")
    
    def _is_content_word(self, word):
        clean = word.strip(string.punctuation).lower()
        return (clean and 
                len(clean) > 3 and 
                clean not in self.vocab.stop_words)
    
    def _apply_synonyms(self, text, rate=0.35):
        """Apply synonyms from the massive library"""
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
        result = text
        for formal, casual in self.contractions.items():
            if random.random() < rate:
                result = result.replace(formal, casual)
        return result
    
    def _restructure_sentences(self, text):
        """Change sentence structure"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        new_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 12 and random.random() < 0.3:
                # Split long sentences
                mid = len(words) // 2
                for j in range(mid, min(mid + 5, len(words) - 1)):
                    if words[j] in ['and', 'but', 'or', 'however', 'therefore']:
                        part1 = ' '.join(words[:j])
                        part2 = ' '.join(words[j:])
                        new_sentences.append(part1)
                        new_sentences.append(part2)
                        break
                else:
                    new_sentences.append(sentence)
            else:
                new_sentences.append(sentence)
        
        return '. '.join(new_sentences)
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Apply transformations
            result = self._apply_synonyms(text, rate=0.35)
            result = self._apply_contractions(result, rate=0.25)
            result = self._restructure_sentences(result)
            
            # Clean up
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            result = re.sub(r',\s*,', ',', result)
            
            if result and result[-1] not in '.!?':
                result += '.'
            
            if not isinstance(result, str) or len(result) < 10:
                return text
            
            if result.lower() in ["true", "false"]:
                return text
            
            return result
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def get_stealth_score(self, text):
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
