import random
import re
import string
from nltk.corpus import wordnet
import nltk

class StealthHumanizer:
    def __init__(self):
        print("✅ Humanizer Ready")
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "has not": "hasn't", "had not": "hadn't", "would not": "wouldn't",
            "should not": "shouldn't", "could not": "couldn't", "does not": "doesn't"
        }
        
        # Fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean"
        ]
        
        # Stop words
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'can', 'that', 'which', 'who'
        }
        
        # Synonyms
        self.synonyms = {
            'important': ['crucial', 'vital', 'essential', 'key', 'significant'],
            'large': ['big', 'huge', 'massive', 'substantial'],
            'small': ['tiny', 'little', 'compact', 'minor'],
            'good': ['great', 'excellent', 'fine', 'superior'],
            'help': ['assist', 'support', 'aid', 'facilitate'],
            'use': ['utilize', 'employ', 'apply', 'leverage'],
            'show': ['demonstrate', 'indicate', 'reveal', 'display'],
            'make': ['create', 'produce', 'generate', 'construct'],
            'get': ['obtain', 'acquire', 'secure', 'gather'],
            'think': ['believe', 'consider', 'reckon', 'suppose'],
            'need': ['require', 'demand', 'necessitate'],
            'know': ['understand', 'comprehend', 'grasp', 'realize'],
            'say': ['state', 'mention', 'remark', 'comment'],
            'see': ['observe', 'notice', 'spot', 'witness'],
            'love': ['adore', 'cherish', 'treasure', 'appreciate'],
            'people': ['individuals', 'folks', 'citizens', 'humans'],
            'thing': ['item', 'object', 'element', 'aspect'],
            'way': ['method', 'approach', 'technique', 'manner'],
            'time': ['period', 'duration', 'moment', 'era']
        }
    
    def _get_synonym(self, word):
        word_lower = word.lower()
        if word_lower in self.synonyms:
            return random.choice(self.synonyms[word_lower])
        try:
            synsets = wordnet.synsets(word_lower)
            if synsets:
                for syn in synsets[:3]:
                    lemmas = syn.lemmas()
                    if lemmas:
                        for lemma in lemmas:
                            lemma_name = lemma.name().replace('_', ' ')
                            if (lemma_name != word_lower and 
                                len(lemma_name) > 2 and
                                lemma_name not in self.stop_words and
                                ' ' not in lemma_name):
                                return lemma_name
        except:
            pass
        return word
    
    def humanize(self, text, style="natural"):
        """Main humanization function - SIMPLE AND RELIABLE"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Convert to list of words
            words = text.split()
            result_words = []
            
            # Process each word
            for word in words:
                clean = word.strip(string.punctuation)
                if clean and len(clean) > 3 and clean not in self.stop_words:
                    # 20% chance of synonym replacement
                    if random.random() < 0.20:
                        syn = self._get_synonym(clean)
                        if syn != clean:
                            if word[0].isupper():
                                syn = syn.capitalize()
                            if word[-1] in string.punctuation:
                                syn = syn + word[-1]
                            result_words.append(syn)
                            continue
                result_words.append(word)
            
            result = ' '.join(result_words)
            
            # Add contractions (simple string replace)
            for formal, casual in self.contractions.items():
                if random.random() < 0.30:
                    result = result.replace(formal, casual)
            
            # Add a filler if not professional
            if style != "professional" and len(result.split()) > 10:
                sentences = result.split('. ')
                if len(sentences) > 1:
                    idx = random.randint(1, min(2, len(sentences) - 1))
                    if len(sentences[idx].split()) > 5:
                        filler = random.choice(self.fillers)
                        words = sentences[idx].split()
                        insert_at = min(3, len(words) - 1)
                        words.insert(insert_at, f"{filler},")
                        sentences[idx] = ' '.join(words)
                    result = '. '.join(sentences)
            
            # Clean up
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            if result and result[-1] not in '.!?':
                result += '.'
            
            # IMPORTANT: Make sure we return a string
            if not isinstance(result, str):
                result = str(result)
            
            # If result is exactly "True" or "False", return original
            if result.lower() in ["true", "false"]:
                return text
            
            return result if len(result) > 5 else text
            
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
            if max(lengths) - min(lengths) > 5:
                score += 10
        return min(score, 99)
