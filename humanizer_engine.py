import random
import re
import string
import json
import os

class StealthHumanizer:
    def __init__(self):
        print("✅ V10.0 - Massive Database Engine")
        
        # Load massive synonym database
        try:
            with open('data/app_synonyms.json', 'r') as f:
                self.synonyms = json.load(f)
            print(f"   📚 Loaded {len(self.synonyms):,} synonym entries")
        except:
            print("   ⚠️ No synonym database found")
            self.synonyms = {}
        
        # Load frequent words
        try:
            with open('data/word_frequency.txt', 'r') as f:
                self.frequent_words = set([w.strip() for w in f.read().split('\n') if w.strip()])
            print(f"   📊 Loaded {len(self.frequent_words):,} frequent words")
        except:
            self.frequent_words = set()
        
        # Load slang
        try:
            with open('data/slang_words.json', 'r') as f:
                self.slang_words = set(json.load(f))
            print(f"   💬 Loaded {len(self.slang_words)} slang words")
        except:
            self.slang_words = set()
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "would not": "wouldn't", "should not": "shouldn't", "could not": "couldn't",
            "does not": "doesn't", "has not": "hasn't", "had not": "hadn't"
        }
        
        # Fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean",
            "the thing is", "you see", "I suppose"
        ]
        
        # Stop words
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
        """Get synonym from massive database with intelligence"""
        word_lower = word.lower()
        
        # Check if we have synonyms for this word
        if word_lower in self.synonyms:
            synonyms = self.synonyms[word_lower]
            if isinstance(synonyms, list) and len(synonyms) > 0:
                # Prefer synonyms that are frequent words (more natural)
                frequent_synonyms = [s for s in synonyms if s in self.frequent_words]
                if frequent_synonyms:
                    return random.choice(frequent_synonyms)
                return random.choice(synonyms)
        
        return word
    
    def _convert_to_passive(self, sentence):
        """Convert active to passive voice"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
        # Look for subject-verb-object pattern
        for i in range(len(words) - 2):
            if words[i].lower() in ['the', 'a', 'an', 'it', 'they', 'we', 'he', 'she']:
                if words[i+1].endswith('s') or words[i+1].endswith('ed'):
                    subject = ' '.join(words[:i+1])
                    verb = words[i+1]
                    obj = ' '.join(words[i+2:])
                    
                    if verb.endswith('s'):
                        verb = verb[:-1] + 'ed'
                    elif verb.endswith('ed'):
                        verb = verb
                    else:
                        verb = verb + 'ed'
                    
                    obj_words = obj.split()
                    if obj_words and obj_words[0].lower() == 'the':
                        obj = ' '.join(obj_words[1:])
                    
                    passive = f"{obj} is {verb} by {subject}"
                    if len(passive.split()) > 3 and len(passive) < len(sentence) * 1.5:
                        return passive
        
        return sentence
    
    def _apply_advanced_restructuring(self, sentence):
        """Apply multiple restructuring techniques"""
        # 35% chance of voice conversion
        if random.random() < 0.35:
            if 'by' in sentence and any(aux in sentence for aux in [' is ', ' are ', ' was ', ' were ']):
                # Passive to active
                parts = sentence.split(' by ')
                if len(parts) == 2:
                    subject = parts[1].strip()
                    obj_verb = parts[0].strip()
                    for aux in [' is ', ' are ', ' was ', ' were ']:
                        if aux in obj_verb:
                            obj_verb = obj_verb.replace(aux, ' ')
                            verb_parts = obj_verb.split()
                            if len(verb_parts) > 0:
                                verb = verb_parts[0].strip()
                                if verb.endswith('ed'):
                                    verb = verb[:-2]
                                obj = ' '.join(verb_parts[1:]) if len(verb_parts) > 1 else ''
                                if obj:
                                    return f"{subject} {verb} {obj}"
            else:
                # Active to passive
                return self._convert_to_passive(sentence)
        return sentence
    
    def humanize(self, text, style="natural"):
        """Advanced humanization with massive database"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            new_sentences = []
            
            for sentence in sentences:
                words = sentence.split()
                new_words = []
                
                # Apply synonyms with intelligence
                for word in words:
                    clean = word.strip(string.punctuation)
                    if clean and len(clean) > 3 and clean not in self.stop_words:
                        # 35% chance of replacement
                        if random.random() < 0.35:
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
                
                # Apply advanced restructuring
                if len(new_sentence.split()) > 5:
                    new_sentence = self._apply_advanced_restructuring(new_sentence)
                
                # Apply contractions
                for formal, casual in self.contractions.items():
                    if random.random() < 0.20:
                        new_sentence = new_sentence.replace(formal, casual)
                
                new_sentences.append(new_sentence)
            
            # Add transitions and fillers
            if style != "professional" and len(new_sentences) > 2:
                transitions = ['However,', 'Therefore,', 'Furthermore,', 'Moreover,', 'On the other hand,']
                for i in range(1, len(new_sentences)):
                    if len(new_sentences[i].split()) > 6 and random.random() < 0.2:
                        transition = random.choice(transitions)
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
            
            # Final cleanup
            result = '. '.join(new_sentences)
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            result = re.sub(r',\s*,', ',', result)
            
            if result and result[-1] not in '.!?':
                result += '.'
            
            # Safety checks
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
