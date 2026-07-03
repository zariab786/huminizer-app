import random
import re
import string
from nltk.corpus import wordnet
import nltk

class StealthHumanizer:
    def __init__(self):
        print("✅ Advanced Sentence Restructuring Engine Ready")
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "would not": "wouldn't", "should not": "shouldn't", "could not": "couldn't"
        }
        
        # Fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean"
        ]
        
        # Advanced synonyms
        self.synonyms = {
            'good': ['excellent', 'superior', 'positive', 'admirable', 'fine'],
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
            'foundation': ['basis', 'base', 'cornerstone', 'bedrock', 'root'],
            'respect': ['esteem', 'regard', 'admiration', 'appreciation', 'reverence'],
            'kindness': ['compassion', 'gentleness', 'benevolence', 'warmth', 'charity'],
            'consideration': ['thoughtfulness', 'attentiveness', 'courtesy', 'care', 'concern'],
            'habits': ['practices', 'customs', 'routines', 'patterns', 'traditions'],
            'society': ['community', 'civilization', 'culture', 'nation', 'population'],
            'behavior': ['conduct', 'actions', 'demeanor', 'manners', 'etiquette'],
            'character': ['nature', 'personality', 'temperament', 'disposition', 'quality'],
            'values': ['principles', 'ethics', 'morals', 'ideals', 'standards']
        }
    
    def _get_synonym(self, word):
        """Intelligent synonym selection"""
        word_lower = word.lower()
        if word_lower in self.synonyms:
            return random.choice(self.synonyms[word_lower])
        try:
            synsets = wordnet.synsets(word_lower)
            if synsets:
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
    
    def _convert_to_passive(self, sentence):
        """ACTIVE → PASSIVE voice conversion"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
        # Try to find subject-verb-object pattern
        for i in range(len(words) - 2):
            # Common subject indicators
            if words[i].lower() in ['the', 'a', 'an', 'it', 'they', 'we', 'he', 'she']:
                # Check if next word is a verb (ends with s or ed)
                if words[i+1].endswith('s') or words[i+1].endswith('ed'):
                    subject = ' '.join(words[:i+1])
                    verb = words[i+1]
                    obj = ' '.join(words[i+2:])
                    
                    # Create passive voice: "Object is verb-ed by Subject"
                    if verb.endswith('s'):
                        verb = verb[:-1] + 'ed'  # makes -> made
                    elif verb.endswith('ed'):
                        verb = verb
                    else:
                        verb = verb + 'ed'
                    
                    # Clean up the object (remove the from object if present)
                    obj_words = obj.split()
                    if obj_words and obj_words[0].lower() == 'the':
                        obj = ' '.join(obj_words[1:])
                    
                    passive = f"{obj} is {verb} by {subject}"
                    # If the result is reasonable, return it
                    if len(passive.split()) > 3 and len(passive) < len(sentence) * 1.5:
                        return passive
        
        return sentence
    
    def _convert_to_active(self, sentence):
        """PASSIVE → ACTIVE voice conversion"""
        if 'by' in sentence.lower() and (' is ' in sentence or ' are ' in sentence or ' was ' in sentence or ' were ' in sentence):
            parts = sentence.split(' by ')
            if len(parts) == 2:
                subject = parts[1].strip()
                obj_verb = parts[0].strip()
                
                # Remove the 'is/are/was/were'
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
    
    def _split_join_sentences(self, sentences):
        """Intelligently split or combine sentences"""
        if len(sentences) < 2:
            return sentences
        
        new_sentences = []
        i = 0
        while i < len(sentences):
            # If sentence is long (>15 words), split it
            if len(sentences[i].split()) > 15 and random.random() < 0.4:
                words = sentences[i].split()
                mid = len(words) // 2
                # Find a natural split point
                split_at = mid
                for j in range(mid, min(mid + 5, len(words) - 1)):
                    if words[j] in ['and', 'but', 'or', 'however', 'therefore']:
                        split_at = j
                        break
                
                if split_at < len(words) - 1:
                    part1 = ' '.join(words[:split_at])
                    part2 = ' '.join(words[split_at:])
                    new_sentences.append(part1)
                    new_sentences.append(part2)
                    i += 1
                    continue
            
            # If sentence is short (<5 words) and next exists, combine
            elif len(sentences[i].split()) < 5 and i < len(sentences) - 1 and random.random() < 0.3:
                combined = sentences[i] + ' and ' + sentences[i+1].lower()
                new_sentences.append(combined)
                i += 2
                continue
            
            new_sentences.append(sentences[i])
            i += 1
        
        return new_sentences
    
    def _add_voice_variation(self, sentence):
        """Randomly apply active/passive conversion"""
        # 40% chance of voice conversion
        if random.random() < 0.40:
            # Check if sentence is passive -> convert to active
            if 'by' in sentence and ('is' in sentence or 'are' in sentence or 'was' in sentence or 'were' in sentence):
                return self._convert_to_active(sentence)
            # Otherwise convert to passive
            else:
                return self._convert_to_passive(sentence)
        return sentence
    
    def humanize(self, text, style="natural"):
        """Advanced humanization with real restructuring"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            # Step 2: Split/combine sentences
            sentences = self._split_join_sentences(sentences)
            
            # Step 3: Process each sentence
            new_sentences = []
            for sentence in sentences:
                # Apply synonyms
                words = sentence.split()
                new_words = []
                for word in words:
                    clean = word.strip(string.punctuation)
                    if clean and len(clean) > 3:
                        if random.random() < 0.30:
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
                
                # Apply voice conversion
                if len(new_sentence.split()) > 5:
                    new_sentence = self._add_voice_variation(new_sentence)
                
                # Apply contractions
                for formal, casual in self.contractions.items():
                    if random.random() < 0.25:
                        new_sentence = new_sentence.replace(formal, casual)
                
                new_sentences.append(new_sentence)
            
            # Step 4: Add transitions and fillers
            if style != "professional" and len(new_sentences) > 2:
                transitions = [
                    ('However,', 0.3), ('Therefore,', 0.2), 
                    ('Furthermore,', 0.2), ('Moreover,', 0.15), 
                    ('On the other hand,', 0.15)
                ]
                
                for i in range(1, len(new_sentences)):
                    if len(new_sentences[i].split()) > 6:
                        if random.random() < 0.25:
                            transition, _ = random.choice(transitions)
                            new_sentences[i] = transition + ' ' + new_sentences[i][0].lower() + new_sentences[i][1:]
                
                # Add fillers
                for _ in range(random.randint(1, 2)):
                    idx = random.randint(1, len(new_sentences) - 1)
                    if len(new_sentences[idx].split()) > 8:
                        filler = random.choice(self.fillers)
                        words = new_sentences[idx].split()
                        insert_pos = random.randint(2, min(4, len(words) - 2))
                        words.insert(insert_pos, filler + ',')
                        new_sentences[idx] = ' '.join(words)
            
            # Step 5: Final cleanup
            result = '. '.join(new_sentences)
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            result = re.sub(r',\s*,', ',', result)
            
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
