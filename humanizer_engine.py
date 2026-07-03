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
            "in my opinion", "to be honest", "I mean", "you see",
            "the thing is", "in other words", "as a matter of fact"
        ]
        
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "has not": "hasn't", "had not": "hadn't", "would not": "wouldn't",
            "should not": "shouldn't", "could not": "couldn't", "does not": "doesn't"
        }
        
        self.synonyms = {
            "important": ["crucial", "vital", "essential", "key", "significant"],
            "large": ["big", "huge", "massive", "substantial"],
            "small": ["tiny", "little", "compact", "miniature"],
            "good": ["great", "excellent", "fine", "superior"],
            "help": ["assist", "support", "aid", "facilitate"],
            "use": ["utilize", "employ", "apply", "leverage"],
            "show": ["demonstrate", "indicate", "reveal", "display"],
            "make": ["create", "produce", "generate", "construct"],
            "get": ["obtain", "acquire", "secure", "gather"]
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
            if final_str.lower() in ["true", "false", "none"]:
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
                    max_length=250,
                    num_beams=4,
                    temperature=0.9,
                    top_p=0.92,
                    do_sample=True,
                    early_stopping=True,
                    repetition_penalty=1.1
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
            if random.random() > 0.5:
                result = result.replace(formal, casual)
        
        filler_count = {
            "casual": random.randint(3, 5),
            "natural": random.randint(2, 4),
            "creative": random.randint(2, 3),
            "professional": random.randint(1, 2)
        }.get(style, 2)
        
        words = result.split()
        if len(words) > 10:
            for _ in range(filler_count):
                if len(words) > 5:
                    idx = random.randint(3, len(words) - 3)
                    words.insert(idx, random.choice(self.fillers))
            result = " ".join(words)
        
        sentences = [s.strip() for s in result.split(". ") if s.strip()]
        if len(sentences) > 2:
            for i in range(len(sentences)):
                if i % 2 == 0 and len(sentences[i].split()) > 10:
                    words = sentences[i].split()
                    sentences[i] = " ".join(words[:max(4, len(words)//2)]) + "..."
                elif i % 3 == 0 and len(sentences[i].split()) < 5:
                    sentences[i] += " and all that stuff"
            result = ". ".join(sentences)
        
        words = result.split()
        for i in range(len(words)):
            if random.random() > 0.85:
                for common, synonyms in self.synonyms.items():
                    if words[i].lower() == common:
                        words[i] = random.choice(synonyms)
                        break
        result = " ".join(words)
        
        return result
    
    def _stealth_layer(self, text):
        if not text:
            return text
        result = text
        
        patterns = {
            "Firstly": "First of all",
            "Secondly": "Next",
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "To wrap it up",
            "Moreover": "Besides that",
            "Consequently": "As a result",
            "Therefore": "So",
            "Thus": "In other words"
        }
        for old, new in patterns.items():
            result = result.replace(old, new)
            result = result.replace(old.lower(), new.lower())
        
        if random.random() > 0.7:
            result = result.replace(" their ", " there ", 1)
        if random.random() > 0.8:
            result = result.replace(" you're ", " your ", 1)
        
        return result
    
    def get_stealth_score(self, text):
        if not text:
            return 0
        score = 75
        words = text.split()
        if len(words) == 0:
            return 50
        
        human_markers = ["don't", "can't", "i'm", "you're", "it's", "that's", "wasn't", "couldn't"]
        if any(marker in text.lower() for marker in human_markers):
            score += 8
        
        if len(set(words)) / len(words) > 0.55:
            score += 8
        
        sentences = [s for s in text.split(". ") if s]
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 8:
                score += 7
        
        if any(filler in text.lower() for filler in self.fillers):
            score += 7
        
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        
        contraction_count = sum(1 for word in words if "'" in word)
        if contraction_count / len(words) > 0.05:
            score += 5
        
        return min(score, 99)
