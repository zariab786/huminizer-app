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
        if not text or len(text) < 5:
            return text
        try:
            paraphrased = self._paraphrase(text)
            humanized = self._add_human_touches(paraphrased, style)
            final = self._stealth_layer(humanized)
            if final is None or final == "":
                return text
            final_str = str(final)
            if final_str.lower() in ["true", "false"]:
                return text
            return final_str
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _paraphrase(self, text):
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
                    max_length=200,
                    num_beams=4,
                    temperature=0.85,
                    top_p=0.9,
                    do_sample=True,
                    early_stopping=True
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
    
    def _add_human_touches(self, text, style):
        if not text:
            return text
        result = text
        for formal, casual in self.contractions.items():
            if random.random() > 0.6:
                result = result.replace(formal, casual)
        filler_count = {
            "casual": 3,
            "natural": 2,
            "creative": 2,
            "professional": 1
        }.get(style, 2)
        words = result.split()
        if len(words) > 10:
            for _ in range(filler_count):
                if len(words) > 5:
                    idx = random.randint(3, len(words) - 3)
                    words.insert(idx, random.choice(self.fillers))
            result = " ".join(words)
        if ". " in result:
            sentences = result.split(". ")
            for i in range(len(sentences)):
                if i % 2 == 0 and len(sentences[i].split()) > 8:
                    words = sentences[i].split()
                    sentences[i] = " ".join(words[:max(3, len(words)//2)]) + "..."
            result = ". ".join(sentences)
        return result
    
    def _stealth_layer(self, text):
        if not text:
            return text
        result = text
        patterns = {
            "Firstly": "First",
            "Secondly": "Second",
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "To sum up",
            "Moreover": "Besides",
            "Consequently": "So",
            "Therefore": "Thus"
        }
        for old, new in patterns.items():
            result = result.replace(old, new)
            result = result.replace(old.lower(), new.lower())
        return result
    
    def get_stealth_score(self, text):
        if not text:
            return 0
        score = 75
        words = text.split()
        if len(words) == 0:
            return 50
        human_markers = ["don't", "can't", "i'm", "you're", "it's", "that's"]
        if any(marker in text.lower() for marker in human_markers):
            score += 5
        if len(set(words)) / len(words) > 0.6:
            score += 5
        sentences = [s for s in text.split(". ") if s]
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 10:
                score += 5
        if any(filler in text.lower() for filler in self.fillers):
            score += 5
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        return min(score, 99)
