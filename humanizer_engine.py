import random
import re
import string
from nltk.corpus import wordnet
import nltk
from nltk.tokenize import sent_tokenize

class StealthHumanizer:
    def __init__(self):
        print("✅ Advanced Humanizer Ready")
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "would not": "wouldn't", "should not": "shouldn't", "could not": "couldn't"
        }
        
        # Rich fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean",
            "the thing is", "you see", "I suppose"
        ]
        
        # Advanced synonyms
        self.advanced_synonyms = {
            'good': ['excellent', 'superior', 'quality', 'positive', 'admirable'],
            'great': ['exceptional', 'remarkable', 'outstanding', 'impressive'],
            'important': ['crucial', 'vital', 'essential', 'critical', 'significant'],
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
            'thing': ['item', 'object', 'element', 'aspect', 'factor'],
            'way': ['method', 'approach', 'technique', 'manner', 'process'],
            'time': ['period', 'duration', 'moment', 'era', 'phase'],
            'life': ['existence', 'being', 'living', 'survival', 'lifespan'],
            'world': ['planet', 'earth', 'globe', 'universe', 'realm'],
            'foundation': ['basis', 'base', 'cornerstone', 'bedrock', 'root'],
            'respect': ['esteem', 'regard', 'admiration', 'appreciation', 'reverence'],
            'kindness': ['compassion', 'gentleness', 'benevolence', 'warmth', 'charity'],
            'consideration': ['thoughtfulness', 'attentiveness', 'courtesy', 'care', 'concern'],
            'habits': ['practices', 'customs', 'routines', 'patterns', 'traditions']
        }
    
    def _get_synonym(self, word):
        """Intelligent synonym selection"""
        word_lower = word.lower()
        
        # Check advanced synonyms
        if word_lower in self.advanced_synonyms:
            return random.choice(self.advanced_synonyms[word_lower])
        
        # Try WordNet
        try:
            synsets = wordnet.synsets(word_lower)
            if synsets:
                # Get the most common synonym
                for syn in synsets[:3]:
                    lemmas = syn.lemmas()
                    if lemmas:
                        for lemma in lemmas[:3]:
                            lemma_name = lemma.name().replace('_', ' ')
                            if (lemma_name != word_lower and 
                                len(lemma_name) > 2 and
                                ' ' not in lemma_name):
                                return lemma_name
        except:
            pass
        
        return word
    
    def _to_passive(self, sentence):
        """Convert active to passive voice"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
        # Find verb patterns
        for i in range(len(words) - 2):
            # Pattern: subject + verb + object
            if words[i] in ['the', 'a', 'an', 'it', 'they', 'we'] and words[i+1] in ['is', 'are', 'was', 'were', 'have', 'has', 'had']:
                continue
            
            # Simple passive conversion
            if i+2 < len(words):
                subject = ' '.join(words[:i+1])
                verb = words[i+1]
                obj = ' '.join(words[i+2:])
                
                # Remove 's' from verb if present
                if verb.endswith('s'):
                    verb = verb[:-1]
                
                # Create passive voice
                passive = f"{obj} is {verb}ed by {subject}"
                if len(passive.split()) > 3:
                    return passive
        
        return sentence
    
    def _to_active(self, sentence):
        """Convert passive to active voice"""
        if 'by' in sentence and (' is ' in sentence or ' are ' in sentence or ' was ' in sentence or ' were ' in sentence):
            parts = sentence.split(' by ')
            if len(parts) == 2:
                subject = parts[1]
                obj_verb = parts[0]
                # Remove auxiliary verb
                for aux in [' is ', ' are ', ' was ', ' were ']:
                    if aux in obj_verb:
                        obj_verb = obj_verb.replace(aux, ' ')
                        verb_parts = obj_verb.split()
                        if verb_parts:
                            verb = verb_parts[0]
                            obj = ' '.join(verb_parts[1:])
                            active = f"{subject} {verb} {obj}"
                            if len(active.split()) > 3:
                                return active
        return sentence
    
    def _add_transition(self, sentence, pos):
        """Add transitional phrases naturally"""
        transitions = {
            'addition': ['Furthermore,', 'Moreover,', 'In addition,', 'Additionally,'],
            'contrast': ['However,', 'Nevertheless,', 'On the other hand,', 'Conversely,'],
            'cause': ['Therefore,', 'Thus,', 'Consequently,', 'As a result,'],
            'example': ['For example,', 'For instance,', 'Such as,', 'Namely,']
        }
        
        if pos == 'addition':
            return random.choice(transitions['addition']) + ' ' + sentence[0].lower() + sentence[1:]
        elif pos == 'contrast':
            return random.choice(transitions['contrast']) + ' ' + sentence[0].lower() + sentence[1:]
        elif pos == 'cause':
            return random.choice(transitions['cause']) + ' ' + sentence[0].lower() + sentence[1:]
        else:
            return sentence
    
    def _restructure_sentence(self, sentence):
        """Apply multiple restructuring techniques"""
        techniques = [
            self._to_passive,
            self._to_active,
            lambda s: self._add_transition(s, 'addition') if len(s.split()) > 5 else s,
            lambda s: self._add_transition(s, 'contrast') if len(s.split()) > 5 else s,
            lambda s: self._add_transition(s, 'cause') if len(s.split()) > 5 else s
        ]
        
        # Apply 1-2 techniques
        for _ in range(random.randint(1, 2)):
            technique = random.choice(techniques)
            new_sentence = technique(sentence)
            if new_sentence != sentence and len(new_sentence) > 5:
                sentence = new_sentence
        
        return sentence
    
    def humanize(self, text, style="natural"):
        """Advanced humanization pipeline"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            new_sentences = []
            
            for i, sentence in enumerate(sentences):
                # Step 2: Apply synonyms to content words
                words = sentence.split()
                new_words = []
                
                for word in words:
                    clean = word.strip(string.punctuation)
                    if clean and len(clean) > 3:
                        # 35% chance of synonym replacement
                        if random.random() < 0.35:
                            syn = self._get_synonym(clean)
                            if syn != clean:
                                if word[0].isupper():
                                    syn = syn.capitalize()
                                if word[-1] in string.punctuation:
                                    syn = syn + word[-1]
                                new_words.append(syn)
                                continue
                    new_words.append(word)
                
                new_sentence = ' '.join(new_words)
                
                # Step 3: Restructure sentence (active/passive, transitions)
                if len(new_sentence.split()) > 5:
                    new_sentence = self._restructure_sentence(new_sentence)
                
                # Step 4: Add contractions
                for formal, casual in self.contractions.items():
                    if random.random() < 0.20:
                        new_sentence = new_sentence.replace(formal, casual)
                
                new_sentences.append(new_sentence)
            
            # Step 5: Add fillers to 1-2 sentences
            if style != "professional" and len(new_sentences) > 2:
                for _ in range(random.randint(1, 2)):
                    idx = random.randint(1, len(new_sentences) - 1)
                    if len(new_sentences[idx].split()) > 8:
                        filler = random.choice(self.fillers)
                        words = new_sentences[idx].split()
                        insert_pos = random.randint(2, min(4, len(words) - 2))
                        words.insert(insert_pos, f"{filler},")
                        new_sentences[idx] = ' '.join(words)
            
            # Step 6: Final cleanup
            result = '. '.join(new_sentences)
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            
            if result and result[-1] not in '.!?':
                result += '.'
            
            # Step 7: Safety check - return original if something went wrong
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
        
        # Transitions
        transitions = ['furthermore', 'moreover', 'however', 'therefore', 'consequently']
        if any(t in text.lower() for t in transitions):
            score += 5
        
        return min(score, 99)
