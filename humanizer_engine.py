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
        
        self.fillers = ["actually", "basically", "honestly", "you know", "well", "so", "like"]
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's"
        }
    
    def humanize(self, text, style="natural"):
        paraphrased = self._paraphrase(text)
        humanized = self._add_human_touches(paraphrased, style)
        return self._stealth_layer(humanized)
    
    def _paraphrase(self, text):
        inputs = self.tokenizer(f"paraphrase: {text}", return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=200, num_beams=5, temperature=0.9, top_p=0.85, do_sample=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def _add_human_touches(self, text, style):
        for formal, casual in self.contractions.items():
            if random.random() > 0.5:
                text = text.replace(formal, casual)
        
        filler_count = {"casual": 3, "natural": 2, "creative": 2, "professional": 1}.get(style, 2)
        words = text.split()
        if len(words) > 10:
            for _ in range(filler_count):
                idx = random.randint(3, len(words) - 3)
                words.insert(idx, random.choice(self.fillers))
            text = " ".join(words)
        return text
    
    def _stealth_layer(self, text):
        patterns = {r'Firstly': 'First', r'Furthermore': 'Also', r'Additionally': 'Plus'}
        for pattern, replacement in patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
    
    def get_stealth_score(self, text):
        score = 75
        if any(word in text.lower() for word in ["don't", "can't", "i'm"]): score += 5
        if len(set(text.split())) / len(text.split()) > 0.6: score += 5
        if any(filler in text.lower() for filler in self.fillers): score += 5
        return min(score, 99)