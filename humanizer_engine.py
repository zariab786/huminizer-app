import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random
import re
import nltk
from nltk.corpus import wordnet

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
        
        # Filler words - carefully curated
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean"
        ]
        
        # Only use these fillers at sentence boundaries
        self.sentence_starters = [
            "In fact", "Interestingly", "Notably", 
            "It is worth noting that", "Importantly"
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
        
        # Stop words - don't replace these
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'via', 'per', 'as',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their', 'its',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'can'
        }
    
    def _get_synonyms(self, word, max_synonyms=2):
        """Get context-appropriate synonyms"""
        try:
            synonyms = set()
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    lemma_name = lemma.name().replace('_', ' ')
                    # Filter: keep common words, reject obscure ones
                    if (lemma_name.lower() != word.lower() and 
                        ' ' not in lemma_name and
                        len(lemma_name) <= len(word) + 3 and
                        len(lemma_name) > 2):
                        synonyms.add(lemma_name.lower())
                        if len(synonyms) >= max_synonyms * 2:
                            break
                if len(synonyms) >= max_synonyms * 2:
                    break
            
            # Remove the original word
            synonyms.discard(word.lower())
            
            # Filter out stop words
            synonyms = [s for s in synonyms if s not in self.stop_words]
            
            return list(synonyms)[:max_synonyms] if synonyms else []
        except:
            return []
    
    def _replace_with_synonym(self, word, pos):
        """Replace a word with a synonym - only for content words"""
        # Skip stop words
        if word.lower() in self.stop_words:
            return word
        
        # Skip short words
        if len(word) < 4:
            return word
        
        # Only replace 15-20% of content words
        if random.random() > 0.20:
            return word
        
        synonyms = self._get_synonyms(word, max_synonyms=2)
        if synonyms:
            # Prefer common synonyms
            preferred = ['important', 'vital', 'crucial', 'essential', 'significant',
                        'large', 'big', 'massive', 'substantial',
                        'small', 'tiny', 'little', 'compact']
            
            for pref in preferred:
                if pref in synonyms:
                    return pref
            
            return random.choice(synonyms)
        return word
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - V3.1 Context-Aware"""
        if not text or len(text) < 5:
            return text
        
        try:
            # Step 1: Paraphrase (lighter touch)
            paraphrased = self._paraphrase(text)
            
            # Step 2: Apply synonyms selectively
            synonymized = self._apply_synonyms_selectively(paraphrased)
            
            # Step 3: Add contractions (not fillers)
            contracted = self._add_contractions(synonymized)
            
            # Step 4: Add sentence starters (not random fillers)
            final = self._add_sentence_starters(contracted, style)
            
            # Step 5: Anti-detection
            final = self._stealth_layer(final)
            
            if final is None or final == "":
                return text
            final_str = str(final)
            if final_str.lower() in ["true", "false", "none"]:
                return text
            
            return final_str
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _paraphrase(self, text):
        """Paraphrase with moderate changes"""
        if not text or len(text) < 10:
            return text
        try:
            if len(text) > 500:
                text = text[:500]
            inputs = self.tokenizer(
                f"paraphrase: {text}", 
                return_tensors="pt", 
                max_length=512, 
                truncation=True,
                padding=True
            )
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=300,
                    num_beams=4,
                    temperature=0.85,
                    top_p=0.9,
                    do_sample=True,
                    early_stopping=True,
                    repetition_penalty=1.1,
                    no_repeat_ngram_size=3
                )
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if result:
                result = result.replace("paraphrase: ", "")
                if result and len(result) > 1:
                    result = result[0].upper() + result[1:]
            return result if result and len(result) > 5 else text
        except Exception as e:
            print(f"⚠️ Paraphrase error: {e}")
            return text
    
    def _apply_synonyms_selectively(self, text):
        """Apply synonyms only to content words"""
        if not text:
            return text
        
        words = text.split()
        for i in range(len(words)):
            clean_word = words[i].strip('.,!?;:()')
            if clean_word and len(clean_word) > 3:
                replacement = self._replace_with_synonym(clean_word, i)
                if replacement != clean_word:
                    # Preserve capitalization
                    if clean_word[0].isupper():
                        replacement = replacement.capitalize()
                    words[i] = replacement
        
        return " ".join(words)
    
    def _add_contractions(self, text):
        """Add contractions only where they make sense"""
        result = text
        for formal, casual in self.contractions.items():
            # Only replace 40% of occurrences
            if random.random() > 0.6:
                result = result.replace(formal, casual)
        return result
    
    def _add_sentence_starters(self, text, style):
        """Add sentence starters at sentence boundaries (not random positions)"""
        if not text or style == "professional":
            return text
        
        sentences = text.split('. ')
        if len(sentences) <= 2:
            return text
        
        # Add starters to 2-3 sentences
        starter_count = min(random.randint(1, 3), len(sentences) - 1)
        indices = random.sample(range(1, len(sentences)), starter_count)
        
        for idx in indices:
            # Don't add if sentence is too short
            if len(sentences[idx].split()) < 5:
                continue
                
            starter = random.choice(self.sentence_starters)
            sentences[idx] = f"{starter}, {sentences[idx].lower()}"
        
        return '. '.join(sentences)
    
    def _stealth_layer(self, text):
        """Final anti-detection processing - light touch"""
        if not text:
            return text
        result = text
        
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
        
        # Check for human markers
        human_markers = ["don't", "can't", "i'm", "you're", "it's", "that's", "wasn't", "couldn't"]
        if any(marker in text.lower() for marker in human_markers):
            score += 8
        
        # Vocabulary diversity
        unique_words = len(set(words))
        if unique_words / len(words) > 0.5:
            score += 8
        
        # Sentence length variation
        sentences = [s for s in text.split(". ") if s]
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 8:
                score += 7
        
        # Length bonus
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        
        return min(score, 99)
