import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random
import re

class StealthHumanizer:
    def __init__(self):
        print("🔄 Loading models... (2-3 minutes)")
        self.model_name = "t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        print("✅ Models loaded!")
        
        self.fillers = [
            "actually", "basically", "honestly", "you know", "well", 
            "so", "like", "literally", "seriously", "just saying",
            "in my opinion", "to be honest"
        ]
        
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't"
        }
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - RETURNS THE TEXT"""
        try:
            # Step 1: Paraphrase
            paraphrased = self._paraphrase(text)
            
            # Step 2: Add human touches
            humanized = self._add_human_touches(paraphrased, style)
            
            # Step 3: Anti-detection layer
            final = self._stealth_layer(humanized)
            
            # Step 4: Make sure we return a string, not a bool!
            if isinstance(final, bool):
                return text  # Return original if something went wrong
            
            return final if final and len(final) > 5 else text
            
        except Exception as e:
            print(f"⚠️ Error in humanize: {e}")
            return text  # Return original text on error
    
    def _paraphrase(self, text):
        """Paraphrase using T5"""
        if not text or len(text) < 10:
            return text
            
        try:
            input_text = f"paraphrase: {text}"
            inputs = self.tokenizer(
                input_text, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True,
                padding=True
            )
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=200,
                    num_beams=5,
                    temperature=0.9,
                    top_p=0.85,
                    do_sample=True,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return result if result and len(result) > 5 else text
            
        except Exception as e:
            print(f"⚠️ Paraphrase error: {e}")
            return text
    
    def _add_human_touches(self, text, style):
        """Add human-like imperfections based on style"""
        if not text:
            return text
            
        # Apply contractions
        for formal, casual in self.contractions.items():
            if random.random() > 0.5:
                text = text.replace(formal, casual)
        
        # Add filler words based on style
        filler_map = {
            "casual": random.randint(2, 4),
            "natural": random.randint(1, 3),
            "creative": random.randint(1, 2),
            "professional": random.randint(0, 1)
        }
        filler_count = filler_map.get(style, 2)
        
        words = text.split()
        if len(words) > 10:
            for _ in range(filler_count):
                if len(words) > 5:
                    idx = random.randint(3, len(words) - 3)
                    words.insert(idx, random.choice(self.fillers))
            text = " ".join(words)
        
        # Vary sentence length (burstiness)
        sentences = text.split('. ')
        if len(sentences) > 2:
            for i in range(len(sentences)):
                if i % 2 == 0 and len(sentences[i].split()) > 8:
                    words = sentences[i].split()
                    sentences[i] = " ".join(words[:len(words)//2]) + "..."
                elif i % 3 == 0 and len(sentences[i].split()) < 5:
                    sentences[i] += " and all that stuff"
            text = ". ".join(sentences)
        
        return text
    
    def _stealth_layer(self, text):
        """Final anti-detection processing"""
        if not text:
            return text
            
        # Remove common AI patterns
        patterns = {
            r'Firstly': 'First',
            r'Secondly': 'Second',
            r'Furthermore': 'Also',
            r'Additionally': 'Plus',
            r'In conclusion': 'To sum up',
            r'Moreover': 'Besides',
            r'Consequently': 'So',
            r'Therefore': 'Thus'
        }
        
        for pattern, replacement in patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Mix active/passive voice randomly
        if random.random() > 0.5:
            text = text.replace("is being", "is")
            text = text.replace("are being", "are")
        
        return text
    
    def get_stealth_score(self, text):
        """Estimate how human-like the text is (0-100)"""
        if not text:
            return 0
            
        score = 75  # Base score
        
        words = text.split()
        if len(words) == 0:
            return 50
        
        # Check for human markers
        if any(word in text.lower() for word in ["don't", "can't", "i'm", "you're"]):
            score += 5
        
        # Vocabulary diversity
        unique_words = len(set(words))
        if unique_words / len(words) > 0.6:
            score += 5
        
        # Sentence length variation
        sentences = text.split('. ')
        lengths = [len(s.split()) for s in sentences if s]
        if lengths and max(lengths) - min(lengths) > 10:
            score += 5
        
        # Filler words
        if any(filler in text.lower() for filler in self.fillers):
            score += 5
        
        # Longer text usually scores higher
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        
        return min(score, 99)
