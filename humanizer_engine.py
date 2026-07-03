import random
import re
import string
from nltk.corpus import wordnet
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class StealthHumanizer:
    def __init__(self):
        print("✅ Stealth Writer Engine Ready")
        
        # Advanced contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "has not": "hasn't", "had not": "hadn't", "would not": "wouldn't",
            "should not": "shouldn't", "could not": "couldn't", "does not": "doesn't"
        }
        
        # Natural fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean", 
            "the thing is", "you see", "I suppose"
        ]
        
        # Transitional phrases
        self.transitions = {
            'addition': ['furthermore', 'moreover', 'in addition', 'additionally', 'also', 'plus'],
            'contrast': ['however', 'nevertheless', 'on the other hand', 'conversely', 'yet', 'though'],
            'cause': ['therefore', 'thus', 'consequently', 'as a result', 'hence', 'so'],
            'example': ['for example', 'for instance', 'such as', 'including', 'namely'],
            'conclusion': ['in conclusion', 'to summarize', 'ultimately', 'finally', 'overall']
        }
        
        # Stop words - never replace
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'via', 'per', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their', 'its',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'can', 'that', 'which', 'who',
            'whom', 'whose', 'what', 'when', 'where', 'why', 'how'
        }
        
        # Thesaurus for synonym replacement
        self.thesaurus = {
            'good': ['great', 'excellent', 'fine', 'superior', 'quality', 'positive'],
            'bad': ['poor', 'terrible', 'awful', 'horrible', 'inferior', 'negative'],
            'big': ['large', 'huge', 'massive', 'substantial', 'considerable', 'enormous'],
            'small': ['tiny', 'little', 'compact', 'miniature', 'minor', 'modest'],
            'important': ['crucial', 'vital', 'essential', 'key', 'significant', 'critical'],
            'help': ['assist', 'support', 'aid', 'facilitate', 'guide', 'serve'],
            'use': ['utilize', 'employ', 'apply', 'leverage', 'adopt', 'implement'],
            'show': ['demonstrate', 'indicate', 'reveal', 'display', 'exhibit', 'illustrate'],
            'make': ['create', 'produce', 'generate', 'construct', 'form', 'develop'],
            'get': ['obtain', 'acquire', 'secure', 'gather', 'receive', 'obtain'],
            'think': ['believe', 'consider', 'reckon', 'suppose', 'imagine', 'assume'],
            'need': ['require', 'demand', 'necessitate', 'call for', 'need to'],
            'know': ['understand', 'comprehend', 'grasp', 'realize', 'recognize', 'perceive'],
            'say': ['state', 'mention', 'remark', 'comment', 'express', 'declare'],
            'see': ['observe', 'notice', 'spot', 'witness', 'view', 'perceive'],
            'come': ['arrive', 'approach', 'enter', 'advance', 'proceed', 'emerge'],
            'go': ['proceed', 'advance', 'move', 'head', 'travel', 'progress'],
            'love': ['adore', 'cherish', 'treasure', 'appreciate', 'value', 'admire'],
            'hate': ['despise', 'loathe', 'detest', 'dislike', 'abhor', 'reject'],
            'people': ['individuals', 'folks', 'citizens', 'humans', 'persons'],
            'thing': ['item', 'object', 'element', 'factor', 'aspect', 'component'],
            'way': ['method', 'approach', 'technique', 'manner', 'means', 'process'],
            'time': ['period', 'duration', 'moment', 'era', 'phase', 'stage'],
            'life': ['existence', 'being', 'living', 'survival', 'lifespan'],
            'world': ['planet', 'earth', 'globe', 'universe', 'realm']
        }
        
        # Advanced restructuring patterns
        self.restructure_templates = [
            # Active to passive
            lambda s: self._to_passive(s),
            # Passive to active
            lambda s: self._to_active(s),
            # Fronting
            lambda s: self._fronting(s),
            # Cleft sentences
            lambda s: self._to_cleft(s),
            # Split long sentences
            lambda s: self._split_sentence(s),
            # Combine short sentences
            lambda s: self._combine_sentences(s)
        ]
    
    def _get_synonym(self, word):
        """Get a synonym from multiple sources"""
        word_lower = word.lower()
        
        # Check thesaurus first
        if word_lower in self.thesaurus:
            return random.choice(self.thesaurus[word_lower])
        
        # Check WordNet
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
    
    def _to_passive(self, sentence):
        """Convert active to passive voice (simplified)"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
        # Look for common patterns: subject + verb + object
        for i in range(len(words) - 2):
            if words[i] in self.stop_words and words[i+1].endswith('s'):
                # Simple passive: "The cat chases the mouse" -> "The mouse is chased by the cat"
                if i+2 < len(words):
                    subject = ' '.join(words[:i+1])
                    verb = words[i+1]
                    obj = ' '.join(words[i+2:])
                    return f"{obj} is {verb}ed by {subject}"
        
        return sentence
    
    def _to_active(self, sentence):
        """Convert passive to active voice (simplified)"""
        if 'by' in sentence and ' is ' in sentence:
            parts = sentence.split(' by ')
            if len(parts) == 2:
                subject = parts[1]
                obj_verb = parts[0]
                # Remove 'is' from obj_verb
                if ' is ' in obj_verb:
                    obj_verb = obj_verb.replace(' is ', ' ')
                    return f"{subject} {obj_verb}"
        return sentence
    
    def _fronting(self, sentence):
        """Move a phrase to the front"""
        words = sentence.split()
        if len(words) > 6:
            # Move the last 2-3 words to the front
            front = random.sample(words[-4:], min(3, len(words[-4:])))
            rest = words[:-4]
            return ' '.join(front + rest)
        return sentence
    
    def _to_cleft(self, sentence):
        """Convert to cleft sentence"""
        words = sentence.split()
        if len(words) > 4:
            # It is [subject] that [rest]
            subject = ' '.join(words[:2])
            rest = ' '.join(words[2:])
            templates = [
                f"It is {subject} that {rest}",
                f"What is important is that {sentence}",
                f"The thing is that {sentence}"
            ]
            return random.choice(templates)
        return sentence
    
    def _split_sentence(self, sentence):
        """Split long sentence into two"""
        words = sentence.split()
        if len(words) > 10:
            mid = len(words) // 2
            # Split at a natural point (after a stop word)
            split_idx = mid
            for i in range(mid, min(mid + 3, len(words) - 1)):
                if words[i] in self.stop_words:
                    split_idx = i + 1
                    break
            
            part1 = ' '.join(words[:split_idx])
            part2 = ' '.join(words[split_idx:])
            return f"{part1}. {part2}"
        return sentence
    
    def _combine_sentences(self, sentence):
        """Combine sentences (for short sentences)"""
        # This is handled in the main method
        return sentence
    
    def _restructure(self, text):
        """Apply random restructuring to the text"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i in range(len(sentences)):
            if len(sentences[i].split()) > 5:
                # Apply 1-2 restructuring techniques
                for _ in range(random.randint(1, 2)):
                    template = random.choice(self.restructure_templates)
                    try:
                        new_sentence = template(sentences[i])
                        if new_sentence != sentences[i] and len(new_sentence) > 10:
                            sentences[i] = new_sentence
                    except:
                        pass
        
        return ' '.join(sentences)
    
    def _add_fillers(self, text, style):
        """Add natural fillers"""
        if style == "professional":
            return text
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Add 1-2 fillers overall
        filler_count = min(random.randint(1, 2), len(sentences) - 1)
        indices = random.sample(range(1, len(sentences)), filler_count)
        
        for idx in indices:
            if len(sentences[idx].split()) > 5:
                filler = random.choice(self.fillers)
                words = sentences[idx].split()
                # Insert filler after the first few words
                insert_pos = random.randint(2, min(5, len(words) - 2))
                words.insert(insert_pos, f"{filler},")
                sentences[idx] = ' '.join(words)
        
        return '. '.join(sentences)
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - V5.0"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: Restructure sentences (changes structure significantly)
            restructured = self._restructure(text)
            
            # Step 2: Add synonyms (changes vocabulary)
            synonymized = self._apply_synonyms(restructured)
            
            # Step 3: Add contractions (adds natural flow)
            contracted = self._apply_contractions(synonymized)
            
            # Step 4: Add fillers (adds human touches)
            humanized = self._add_fillers(contracted, style)
            
            # Step 5: Final cleanup
            final = self._final_cleanup(humanized)
            
            # Safety checks
            if not isinstance(final, str):
                final = str(final)
            
            if final.lower() in ["true", "false"]:
                return text
            
            return final if len(final) > 10 else text
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _apply_synonyms(self, text):
        """Apply synonyms to content words"""
        words = text.split()
        result = []
        
        for word in words:
            clean = word.strip(string.punctuation)
            if clean and len(clean) > 3 and clean not in self.stop_words:
                # 30% chance of replacement (higher than before)
                if random.random() < 0.30:
                    syn = self._get_synonym(clean)
                    if syn != clean:
                        # Preserve case and punctuation
                        if word[0].isupper():
                            syn = syn.capitalize()
                        if word[-1] in string.punctuation:
                            syn = syn + word[-1]
                        result.append(syn)
                        continue
            result.append(word)
        
        return ' '.join(result)
    
    def _apply_contractions(self, text):
        """Apply contractions"""
        result = text
        for formal, casual in self.contractions.items():
            if random.random() < 0.35:
                result = result.replace(formal, casual)
                result = result.replace(formal.title(), casual.title())
        return result
    
    def _final_cleanup(self, text):
        """Final cleanup"""
        # Remove common AI patterns
        patterns = {
            "Firstly": "First",
            "Secondly": "Second",
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "Ultimately",
            "Moreover": "Besides",
            "Consequently": "As a result",
            "Therefore": "So"
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
        """Calculate human-like score (0-100)"""
        if not text:
            return 0
        
        score = 65
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
            if max(lengths) - min(lengths) > 8:
                score += 10
        
        # Fillers
        if any(f in text.lower() for f in self.fillers):
            score += 5
        
        return min(score, 99)
