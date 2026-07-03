import random
import re
import string
import json
from pathlib import Path

class RewriterEngine:
    """Real sentence rewriter - changes structure, not just words"""
    
    def __init__(self):
        print("🔄 Rewriter Engine Ready")
        self._load_vocabulary()
        self._load_templates()
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't"
        }
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    def _load_vocabulary(self):
        """Load massive vocabulary library"""
        try:
            with open('data/unified_vocabulary.json', 'r') as f:
                data = json.load(f)
                self.thesaurus = data.get('thesaurus', {})
                self.frequent_words = set(data.get('frequent_words', []))
                print(f"✅ Loaded {len(self.thesaurus):,} synonyms")
        except:
            print("⚠️ Using fallback vocabulary")
            self.thesaurus = {
                'important': ['crucial', 'vital', 'essential', 'key', 'critical'],
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
                'good': ['great', 'excellent', 'fine', 'positive', 'superior'],
                'bad': ['poor', 'terrible', 'awful', 'horrible', 'inferior'],
                'big': ['large', 'huge', 'massive', 'substantial', 'considerable'],
                'small': ['tiny', 'little', 'compact', 'miniature', 'minor'],
                'people': ['individuals', 'folks', 'citizens', 'humans', 'persons'],
                'respect': ['esteem', 'regard', 'admiration', 'appreciation'],
                'kindness': ['compassion', 'benevolence', 'warmth', 'charity'],
                'society': ['community', 'civilization', 'culture', 'nation'],
                'foundation': ['basis', 'base', 'cornerstone', 'bedrock', 'root'],
                'behavior': ['conduct', 'actions', 'demeanor', 'manners'],
                'values': ['principles', 'ethics', 'morals', 'ideals', 'standards']
            }
    
    def _load_templates(self):
        """Sentence restructuring templates"""
        self.restructure_templates = [
            # Active ↔ Passive
            self._to_passive,
            self._to_active,
            # Fronting
            self._fronting,
            # Cleft sentences
            self._to_cleft,
            # Inversion
            self._inversion,
            # Relative clause conversion
            self._relative_clause,
            # Adverb fronting
            self._adverb_fronting
        ]
    
    def _get_synonym(self, word):
        """Get synonym from massive library"""
        word_lower = word.lower()
        if word_lower in self.thesaurus and self.thesaurus[word_lower]:
            synonyms = self.thesaurus[word_lower]
            if isinstance(synonyms, list) and synonyms:
                frequent = [s for s in synonyms if s in self.frequent_words]
                if frequent:
                    return random.choice(frequent)
                return random.choice(synonyms)
        return word
    
    def _is_content_word(self, word):
        """Check if word should be replaced"""
        clean = word.strip(string.punctuation).lower()
        return (clean and len(clean) > 3 and clean not in self.stop_words)
    
    # ============ RESTRUCTURING FUNCTIONS ============
    
    def _to_passive(self, sentence):
        """Convert active to passive voice"""
        words = sentence.split()
        if len(words) < 4:
            return sentence
        
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
    
    def _to_active(self, sentence):
        """Convert passive to active voice"""
        if 'by' in sentence:
            for aux in [' is ', ' are ', ' was ', ' were ']:
                if aux in sentence:
                    parts = sentence.split(' by ')
                    if len(parts) == 2:
                        subject = parts[1].strip()
                        obj_verb = parts[0].strip()
                        obj_verb = obj_verb.replace(aux, ' ')
                        verb_parts = obj_verb.split()
                        if len(verb_parts) > 0:
                            verb = verb_parts[0]
                            if verb.endswith('ed'):
                                verb = verb[:-2]
                            obj = ' '.join(verb_parts[1:]) if len(verb_parts) > 1 else ''
                            if obj:
                                active = f"{subject} {verb} {obj}"
                                if len(active.split()) > 3:
                                    return active
        return sentence
    
    def _fronting(self, sentence):
        """Move a phrase to the front"""
        words = sentence.split()
        if len(words) > 6 and random.random() < 0.3:
            # Move the last 2-3 words to the front
            front = words[-3:]
            rest = words[:-3]
            return ' '.join(front + rest)
        return sentence
    
    def _to_cleft(self, sentence):
        """Convert to cleft sentence"""
        words = sentence.split()
        if len(words) > 4:
            subject = ' '.join(words[:2])
            rest = ' '.join(words[2:])
            return f"It is {subject} that {rest}"
        return sentence
    
    def _inversion(self, sentence):
        """Use inversion for emphasis"""
        words = sentence.split()
        if len(words) > 4 and random.random() < 0.3:
            # "never", "rarely", "hardly" inversion
            adverbs = ['never', 'rarely', 'hardly', 'scarcely', 'seldom']
            if words[0].lower() in adverbs:
                return f"{words[0].capitalize()} {' '.join(words[1:])}"
        return sentence
    
    def _relative_clause(self, sentence):
        """Convert to relative clause"""
        words = sentence.split()
        if len(words) > 5 and random.random() < 0.3:
            # Simple relative clause conversion
            if words[0].lower() in ['the', 'a', 'an'] and len(words) > 4:
                # Convert "The X is Y" -> "X, which is Y"
                subject = words[0]
                rest = ' '.join(words[1:])
                return f"{subject}, which {rest}"
        return sentence
    
    def _adverb_fronting(self, sentence):
        """Move adverb to the front"""
        adverbs = ['actually', 'basically', 'honestly', 'clearly', 'obviously']
        if random.random() < 0.3:
            adverb = random.choice(adverbs)
            return f"{adverb}, {sentence.lower()}"
        return sentence
    
    # ============ MAIN REWRITE FUNCTION ============
    
    def rewrite(self, text, style="natural"):
        """Main rewrite function - changes structure significantly"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            new_sentences = []
            
            for sentence in sentences:
                if len(sentence.split()) < 4:
                    new_sentences.append(sentence)
                    continue
                
                # Step 1: Apply synonyms (40% of content words)
                words = sentence.split()
                new_words = []
                for word in words:
                    if self._is_content_word(word):
                        if random.random() < 0.40:
                            syn = self._get_synonym(word)
                            if syn != word.lower():
                                if word[0].isupper():
                                    syn = syn.capitalize()
                                if word[-1] in string.punctuation:
                                    syn = syn + word[-1]
                                new_words.append(syn)
                                continue
                    new_words.append(word)
                rewritten = ' '.join(new_words)
                
                # Step 2: Apply structural changes (70% chance)
                if random.random() < 0.70:
                    # Try multiple restructuring techniques
                    for _ in range(random.randint(1, 3)):
                        template = random.choice(self.restructure_templates)
                        new_version = template(rewritten)
                        if new_version != rewritten and len(new_version) > 3:
                            rewritten = new_version
                
                # Step 3: Apply contractions
                for formal, casual in self.contractions.items():
                    if random.random() < 0.25:
                        rewritten = rewritten.replace(formal, casual)
                
                new_sentences.append(rewritten)
            
            # Combine sentences
            result = '. '.join(new_sentences)
            
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
    
    def get_score(self, text):
        """Calculate rewriting score"""
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


# Alias for backward compatibility
StealthHumanizer = RewriterEngine
