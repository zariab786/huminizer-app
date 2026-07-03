import random
import re
import string
from nltk.corpus import wordnet
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class StealthHumanizer:
    def __init__(self):
        print("✅ Stealth Writer Engine Ready (No AI models)")
        
        # Simple contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "would not": "wouldn't", "should not": "shouldn't", "could not": "couldn't"
        }
        
        # Natural fillers
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
            'time': ['period', 'duration', 'moment', 'era'],
            'life': ['existence', 'being', 'living', 'survival']
        }
    
    def _get_synonym(self, word):
        """Get synonym from thesaurus or WordNet"""
        word_lower = word.lower()
        
        # Check thesaurus
        if word_lower in self.synonyms:
            return random.choice(self.synonyms[word_lower])
        
        # Try WordNet
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
    
    def _replace_synonyms(self, text):
        """Replace words with synonyms"""
        words = text.split()
        result = []
        
        for word in words:
            clean = word.strip(string.punctuation)
            if clean and len(clean) > 3 and clean not in self.stop_words:
                # 25% chance of replacement
                if random.random() < 0.25:
                    syn = self._get_synonym(clean)
                    if syn != clean:
                        if word[0].isupper():
                            syn = syn.capitalize()
                        if word[-1] in string.punctuation:
                            syn = syn + word[-1]
                        result.append(syn)
                        continue
            result.append(word)
        
        return ' '.join(result)
    
    def _apply_contractions(self, text):
        """Apply contractions naturally"""
        result = text
        for formal, casual in self.contractions.items():
            if random.random() < 0.30:
                result = result.replace(formal, casual)
                result = result.replace(formal.title(), casual.title())
        return result
    
    def _add_fillers(self, text, style):
        """Add natural fillers"""
        if style == "professional":
            return text
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) <= 1:
            return text
        
        count = min(random.randint(1, 2), len(sentences) - 1)
        indices = random.sample(range(1, len(sentences)), count)
        
        for idx in indices:
            if len(sentences[idx].split()) > 5:
                filler = random.choice(self.fillers)
                words = sentences[idx].split()
                insert_pos = random.randint(2, min(4, len(words) - 1))
                words.insert(insert_pos, f"{filler},")
                sentences[idx] = ' '.join(words)
        
        return ' '.join(sentences)
    
    def _add_sentence_starters(self, text):
        """Add sentence starters"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) <= 2:
            return text
        
        starters = [
            "In fact,", "Interestingly,", "Notably,", 
            "Importantly,", "In particular,", "Indeed,"
        ]
        
        count = min(random.randint(1, 2), len(sentences) - 1)
        indices = random.sample(range(1, len(sentences)), count)
        
        for idx in indices:
            if len(sentences[idx].split()) > 5:
                starter = random.choice(starters)
                sentences[idx] = f"{starter} {sentences[idx][0].lower() + sentences[idx][1:]}"
        
        return ' '.join(sentences)
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: Replace synonyms
            result = self._replace_synonyms(text)
            
            # Step 2: Add contractions
            result = self._apply_contractions(result)
            
            # Step 3: Add sentence starters
            if style != "professional":
                result = self._add_sentence_starters(result)
            
            # Step 4: Add fillers
            result = self._add_fillers(result, style)
            
            # Step 5: Clean up
            result = self._cleanup(result)
            
            # Safety check
            if not isinstance(result, str):
                result = str(result)
            
            if result.lower() in ["true", "false"]:
                return text
            
            return result if len(result) > 5 else text
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _cleanup(self, text):
        """Clean up the text"""
        # Remove common AI patterns
        patterns = {
            "Firstly": "First",
            "Secondly": "Second",
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "Ultimately",
            "Moreover": "Besides"
        }
        for old, new in patterns.items():
            text = text.replace(old, new)
            text = text.replace(old.lower(), new.lower())
        
        # Fix spacing
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix multiple periods
        text = re.sub(r'\.{2,}', '.', text)
        
        # Ensure proper ending
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def get_stealth_score(self, text):
        """Calculate human-like score"""
        if not text:
            return 0
        
        score = 70
        words = text.split()
        if len(words) == 0:
            return 50
        
        # Contractions
        if any("'t" in word or "'m" in word for word in words):
            score += 10
        
        # Vocabulary diversity
        if len(set(words)) / len(words) > 0.5:
            score += 10
        
        # Sentence variation
        sentences = [s for s in text.split(". ") if s]
        if len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 5:
                score += 10
        
        return min(score, 99)
