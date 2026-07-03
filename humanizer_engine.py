import random
import re
import string
import json

class StealthHumanizer:
    def __init__(self):
        print("✅ V12.0 - 50% Active/Passive Conversion")
        
        # Load synonym database
        try:
            with open('data/app_synonyms.json', 'r') as f:
                self.synonyms = json.load(f)
            print(f"   Loaded {len(self.synonyms):,} synonym entries")
        except:
            # Fallback synonyms - clean and natural
            self.synonyms = {
                'good': ['excellent', 'superior', 'fine', 'positive'],
                'great': ['exceptional', 'remarkable', 'outstanding'],
                'important': ['crucial', 'vital', 'essential', 'key'],
                'help': ['assist', 'support', 'aid', 'facilitate'],
                'use': ['utilize', 'employ', 'apply', 'implement'],
                'show': ['demonstrate', 'indicate', 'reveal', 'display'],
                'make': ['create', 'produce', 'generate', 'construct'],
                'get': ['obtain', 'acquire', 'secure', 'gather'],
                'think': ['believe', 'consider', 'reckon', 'suppose'],
                'need': ['require', 'demand', 'necessitate'],
                'know': ['understand', 'comprehend', 'grasp', 'realize'],
                'say': ['state', 'mention', 'remark', 'comment'],
                'see': ['observe', 'notice', 'spot', 'witness'],
                'people': ['individuals', 'folks', 'citizens'],
                'foundation': ['basis', 'cornerstone', 'bedrock'],
                'respect': ['esteem', 'regard', 'admiration'],
                'kindness': ['compassion', 'benevolence', 'warmth'],
                'consideration': ['thoughtfulness', 'courtesy', 'care'],
                'society': ['community', 'civilization', 'culture'],
                'behavior': ['conduct', 'actions', 'demeanor'],
                'character': ['nature', 'personality', 'temperament'],
                'values': ['principles', 'ethics', 'morals'],
                'simple': ['basic', 'elementary', 'straightforward'],
                'habit': ['practice', 'routine', 'custom'],
                'positive': ['favorable', 'good', 'constructive'],
                'strong': ['powerful', 'solid', 'robust']
            }
            print("   Using fallback synonyms")
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "would not": "wouldn't", "should not": "shouldn't", "could not": "couldn't",
            "does not": "doesn't", "has not": "hasn't", "had not": "hadn't"
        }
        
        # Stop words - NEVER replace these
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'can', 'that', 'which', 'who',
            'whom', 'whose', 'what', 'when', 'where', 'why', 'how'
        }
    
    def _get_synonym(self, word):
        """Get a sensible synonym for a word"""
        word_lower = word.lower()
        if word_lower in self.synonyms and self.synonyms[word_lower]:
            synonyms = self.synonyms[word_lower]
            if isinstance(synonyms, list) and len(synonyms) > 0:
                # Pick a synonym that's not too long
                good_synonyms = [s for s in synonyms if len(s) <= len(word) + 3 and len(s) > 2]
                if good_synonyms:
                    return random.choice(good_synonyms)
                return random.choice(synonyms)
        return word
    
    def _apply_active_to_passive(self, sentence):
        """Convert active voice to passive voice"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
        # Find subject + verb + object pattern
        for i in range(len(words) - 2):
            # Check if this looks like a subject
            if words[i].lower() in ['the', 'a', 'an', 'it', 'they', 'we', 'he', 'she', 'this', 'that']:
                # Check if next word is a verb
                verb = words[i+1]
                if verb.endswith('s') or verb.endswith('ed') or verb in ['is', 'are', 'was', 'were', 'have', 'has', 'had']:
                    subject = ' '.join(words[:i+1])
                    obj = ' '.join(words[i+2:])
                    
                    # Clean up object
                    obj_words = obj.split()
                    if obj_words and obj_words[0].lower() in ['the', 'a', 'an']:
                        obj = ' '.join(obj_words[1:])
                    
                    # Create passive voice
                    if verb.endswith('s'):
                        base_verb = verb[:-1]
                        passive_verb = base_verb + 'ed'
                    elif verb.endswith('ed'):
                        passive_verb = verb
                    elif verb in ['is', 'are', 'was', 'were']:
                        passive_verb = verb + ' done'
                    else:
                        passive_verb = verb + 'ed'
                    
                    passive = f"{obj} is {passive_verb} by {subject}"
                    if len(passive.split()) > 3 and len(passive) < len(sentence) * 1.5:
                        return passive
        
        return sentence
    
    def _apply_passive_to_active(self, sentence):
        """Convert passive voice to active voice"""
        if 'by' in sentence:
            parts = sentence.split(' by ')
            if len(parts) == 2:
                subject = parts[1].strip()
                obj_verb = parts[0].strip()
                
                # Remove auxiliary verbs
                for aux in [' is ', ' are ', ' was ', ' were ']:
                    if aux in obj_verb:
                        obj_verb = obj_verb.replace(aux, ' ')
                        verb_parts = obj_verb.split()
                        if len(verb_parts) > 0:
                            verb = verb_parts[0].strip()
                            # Remove 'ed' from verb if present
                            if verb.endswith('ed'):
                                verb = verb[:-2]
                            obj = ' '.join(verb_parts[1:]) if len(verb_parts) > 1 else ''
                            if obj:
                                active = f"{subject} {verb} {obj}"
                                if len(active.split()) > 3:
                                    return active
        
        return sentence
    
    def _is_passive(self, sentence):
        """Check if a sentence is in passive voice"""
        return 'by' in sentence and any(aux in sentence for aux in [' is ', ' are ', ' was ', ' were '])
    
    def humanize(self, text, style="natural"):
        """Intelligent humanization with 50% active/passive conversion"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            result_sentences = []
            voice_changes = 0
            total_sentences = len(sentences)
            
            # We'll convert 50% of sentences to the opposite voice
            target_changes = max(1, int(total_sentences * 0.5))
            
            # Get indices of sentences that can be converted
            convertible_indices = []
            for i, sentence in enumerate(sentences):
                words = sentence.split()
                if len(words) >= 4:
                    convertible_indices.append(i)
            
            # Randomly select which sentences to convert
            if convertible_indices:
                to_convert = random.sample(convertible_indices, min(target_changes, len(convertible_indices)))
            else:
                to_convert = []
            
            for i, sentence in enumerate(sentences):
                # Apply synonyms (30% of content words)
                words = sentence.split()
                new_words = []
                for word in words:
                    clean = word.strip(string.punctuation)
                    if clean and len(clean) > 3 and clean not in self.stop_words:
                        if random.random() < 0.30:
                            syn = self._get_synonym(clean)
                            if syn != clean and syn:
                                if word[0].isupper():
                                    syn = syn.capitalize()
                                if word[-1] in string.punctuation:
                                    syn = syn + word[-1]
                                new_words.append(syn)
                                continue
                    new_words.append(word)
                
                new_sentence = ' '.join(new_words)
                
                # Apply voice conversion if this sentence is selected
                if i in to_convert and len(new_sentence.split()) >= 4:
                    if self._is_passive(new_sentence):
                        new_sentence = self._apply_passive_to_active(new_sentence)
                    else:
                        new_sentence = self._apply_active_to_passive(new_sentence)
                    voice_changes += 1
                
                # Apply contractions
                for formal, casual in self.contractions.items():
                    if random.random() < 0.20:
                        new_sentence = new_sentence.replace(formal, casual)
                
                result_sentences.append(new_sentence)
            
            result = '. '.join(result_sentences)
            
            # Clean up
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            result = re.sub(r',\s*,', ',', result)
            result = re.sub(r'\s+\.', '.', result)
            
            if result and result[-1] not in '.!?':
                result += '.'
            
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
        
        return min(score, 99)
