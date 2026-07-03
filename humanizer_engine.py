import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random
import re
import nltk
from nltk.corpus import wordnet
import string

# Download NLTK data if needed
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

class StealthHumanizer:
    def __init__(self):
        print("🔄 Loading models... (2-3 minutes)")
        self.model_name = "t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        print("✅ Models loaded!")
        
        # Fillers and starters
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean"
        ]
        
        self.sentence_starters = [
            "In fact", "Interestingly", "Notably", 
            "It is worth noting that", "Importantly",
            "In particular", "For example"
        ]
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "has not": "hasn't", "had not": "hadn't", "would not": "wouldn't",
            "should not": "shouldn't", "could not": "couldn't", "does not": "doesn't"
        }
        
        # Stop words
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
    
    def _get_synonyms(self, word):
        """Get context-appropriate synonyms"""
        try:
            synonyms = set()
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    lemma_name = lemma.name().replace('_', ' ')
                    if (lemma_name.lower() != word.lower() and 
                        ' ' not in lemma_name and
                        len(lemma_name) <= len(word) + 3 and
                        len(lemma_name) > 2):
                        synonyms.add(lemma_name.lower())
                        if len(synonyms) >= 4:
                            break
                if len(synonyms) >= 4:
                    break
            
            synonyms.discard(word.lower())
            synonyms = [s for s in synonyms if s not in self.stop_words]
            synonyms = [s for s in synonyms if abs(len(s) - len(word)) <= 2]
            return list(synonyms)[:2] if synonyms else []
        except:
            return []
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - V3.3 with fallback"""
        # Safety check
        if not text or len(text) < 5:
            return str(text) if text else ""
        
        try:
            # STEP 1: Try paraphrase with multiple strategies
            result = None
            
            # Strategy 1: Try T5 paraphrase
            try:
                result = self._paraphrase_with_t5(text)
                print(f"🔍 T5 result: '{result[:100] if result else 'None'}'")
                if result and len(result) > 10 and result != "True":
                    result = result
                else:
                    result = None
            except Exception as e:
                print(f"⚠️ T5 failed: {e}")
                result = None
            
            # Strategy 2: Fallback to manual paraphrasing
            if not result or result == "True" or len(result) < 10:
                print("🔄 Using fallback paraphrasing...")
                result = self._manual_paraphrase(text)
            
            # If still no result, return original
            if not result or len(result) < 10 or result == "True":
                print("⚠️ All paraphrasing failed, using original text")
                result = text
            
            # STEP 2: Apply enhancements
            result = self._enhance_text(result, style)
            
            # Final safety check
            if not isinstance(result, str) or len(result) < 5:
                return text
            
            return result
            
        except Exception as e:
            print(f"⚠️ Critical error: {e}")
            return text
    
    def _paraphrase_with_t5(self, text):
        """Paraphrase using T5 with careful handling"""
        try:
            if len(text) > 500:
                text = text[:500]
            
            # Try different prompt formats
            prompts = [
                f"paraphrase: {text}",
                f"rewrite: {text}",
                f"simplify: {text}"
            ]
            
            for prompt in prompts:
                try:
                    inputs = self.tokenizer(
                        prompt,
                        return_tensors="pt",
                        max_length=512,
                        truncation=True,
                        padding=True
                    )
                    
                    with torch.no_grad():
                        outputs = self.model.generate(
                            **inputs,
                            max_length=300,
                            num_beams=5,
                            temperature=0.85,
                            top_p=0.9,
                            do_sample=True,
                            early_stopping=True,
                            repetition_penalty=1.1,
                            no_repeat_ngram_size=3
                        )
                    
                    result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    
                    # Clean up
                    for prefix in ["paraphrase: ", "rewrite: ", "simplify: "]:
                        result = result.replace(prefix, "")
                    
                    if result and len(result) > 10 and result != "True":
                        return result
                except:
                    continue
            
            return None
        except:
            return None
    
    def _manual_paraphrase(self, text):
        """Manual paraphrasing using synonyms and restructuring"""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        paraphrased = []
        
        for sentence in sentences:
            if len(sentence) < 5:
                paraphrased.append(sentence)
                continue
            
            # Get words
            words = sentence.split()
            new_words = []
            
            for i, word in enumerate(words):
                # Clean word
                clean = word.strip(string.punctuation)
                if clean and len(clean) > 3 and clean not in self.stop_words:
                    # 20% chance of replacement
                    if random.random() < 0.2:
                        syns = self._get_synonyms(clean)
                        if syns:
                            # Preserve punctuation
                            if word[-1] in string.punctuation:
                                new_words.append(random.choice(syns) + word[-1])
                            else:
                                new_words.append(random.choice(syns))
                            continue
                new_words.append(word)
            
            # Reconstruct sentence
            new_sentence = ' '.join(new_words)
            
            # Randomly change structure
            if len(new_sentence.split()) > 5 and random.random() < 0.3:
                words = new_sentence.split()
                # Move a phrase to the front
                if len(words) > 6:
                    front = words[-2:]
                    rest = words[:-2]
                    new_sentence = ' '.join(front + rest)
            
            paraphrased.append(new_sentence)
        
        return ' '.join(paraphrased)
    
    def _enhance_text(self, text, style):
        """Apply human touches to text"""
        if not text:
            return text
        
        result = text
        
        # Add contractions (30% chance)
        for formal, casual in self.contractions.items():
            if random.random() < 0.3:
                result = result.replace(formal, casual)
        
        # Add sentence starters (1-2 sentences)
        if style != "professional":
            sentences = result.split('. ')
            if len(sentences) > 2:
                count = min(random.randint(1, 2), len(sentences) - 1)
                indices = random.sample(range(1, len(sentences)), count)
                for idx in indices:
                    if len(sentences[idx].split()) > 5:
                        starter = random.choice(self.sentence_starters)
                        sentences[idx] = f"{starter}, {sentences[idx][0].lower() + sentences[idx][1:]}"
                result = '. '.join(sentences)
        
        # Remove common AI patterns
        patterns = {
            "Firstly": "First",
            "Secondly": "Second", 
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "To summarize",
            "Moreover": "Besides"
        }
        for old, new in patterns.items():
            result = result.replace(old, new)
            result = result.replace(old.lower(), new.lower())
        
        return result
    
    def get_stealth_score(self, text):
        """Estimate how human-like the text is"""
        if not text:
            return 0
        
        score = 75
        words = text.split()
        if len(words) == 0:
            return 50
        
        # Human markers
        human_markers = ["don't", "can't", "i'm", "you're", "it's", "that's", "wasn't", "couldn't"]
        if any(marker in text.lower() for marker in human_markers):
            score += 8
        
        # Vocabulary diversity
        if len(words) > 0 and len(set(words)) / len(words) > 0.5:
            score += 8
        
        # Sentence length variation
        sentences = [s for s in text.split(". ") if s]
        if sentences and len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 8:
                score += 7
        
        # Length bonus
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        
        return min(score, 99)
