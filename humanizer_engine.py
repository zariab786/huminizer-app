import random
import re
import string
import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class StealthHumanizer:
    def __init__(self):
        print("🔄 Loading T5 model...")
        self.model_name = "t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        print("✅ Model loaded!")
        
        # ==================== LOAD MASSIVE LIBRARY ====================
        print("📚 Loading massive vocabulary library...")
        try:
            with open('data/unified_vocabulary.json', 'r') as f:
                self.vocab_data = json.load(f)
                self.thesaurus = self.vocab_data.get('thesaurus', {})
                self.frequent_words = set(self.vocab_data.get('frequent_words', []))
                print(f"✅ Loaded {len(self.thesaurus):,} synonym entries")
                print(f"📊 Sample synonyms: {list(self.thesaurus.items())[:3]}")
        except Exception as e:
            print(f"⚠️ Error loading library: {e}")
            self.thesaurus = {}
            self.frequent_words = set()
        # =============================================================
        
        # Contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't"
        }
        
        # Stop words
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    def _get_synonym_from_library(self, word):
        """Get synonym from the massive library"""
        word_lower = word.lower()
        
        # Check if word exists in thesaurus
        if word_lower in self.thesaurus:
            synonyms = self.thesaurus[word_lower]
            if isinstance(synonyms, list) and synonyms:
                # Prefer synonyms that are frequent words (more natural)
                frequent_synonyms = [s for s in synonyms if s in self.frequent_words]
                if frequent_synonyms:
                    return random.choice(frequent_synonyms)
                return random.choice(synonyms)
        
        return word
    
    def _apply_synonyms_from_library(self, text, rate=0.35):
        """Apply synonyms from the massive library"""
        words = text.split()
        new_words = []
        
        for word in words:
            # Check if this is a content word
            clean = word.strip(string.punctuation)
            if clean and len(clean) > 3 and clean not in self.stop_words:
                # Apply synonym with given rate
                if random.random() < rate:
                    syn = self._get_synonym_from_library(clean)
                    if syn != clean.lower():
                        # Preserve case and punctuation
                        if word[0].isupper():
                            syn = syn.capitalize()
                        if word[-1] in string.punctuation:
                            syn = syn + word[-1]
                        new_words.append(syn)
                        continue
            new_words.append(word)
        
        return ' '.join(new_words)
    
    def _paraphrase_with_t5(self, text):
        """Paraphrase using T5"""
        try:
            if len(text) > 500:
                text = text[:500]
            
            # Try different prompts
            prompts = [f"paraphrase: {text}", f"rewrite: {text}"]
            
            for prompt in prompts:
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
                        max_length=400,
                        min_length=100,
                        num_beams=6,
                        temperature=0.8,
                        top_p=0.95,
                        do_sample=True,
                        early_stopping=True,
                        repetition_penalty=1.1,
                        no_repeat_ngram_size=3
                    )
                
                result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                result = result.replace("paraphrase: ", "").replace("rewrite: ", "")
                
                if len(result) > 50 and result != text:
                    return result
            
            return text
        except Exception as e:
            print(f"⚠️ T5 error: {e}")
            return text
    
    def _apply_contractions(self, text, rate=0.25):
        """Apply contractions"""
        result = text
        for formal, casual in self.contractions.items():
            if random.random() < rate:
                result = result.replace(formal, casual)
        return result
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - USING MASSIVE LIBRARY"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: T5 Paraphrase
            result = self._paraphrase_with_t5(text)
            
            # Step 2: Apply synonyms from the MASSIVE LIBRARY
            result = self._apply_synonyms_from_library(result, rate=0.35)
            
            # Step 3: Apply contractions
            result = self._apply_contractions(result, rate=0.25)
            
            # Step 4: Clean up
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\.{2,}', '.', result)
            result = re.sub(r',\s*,', ',', result)
            
            if result and result[-1] not in '.!?':
                result += '.'
            
            # If T5 didn't change anything, use more synonyms
            if result == text or len(result) < 20:
                result = self._apply_synonyms_from_library(text, rate=0.50)
                result = self._apply_contractions(result, rate=0.30)
            
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
