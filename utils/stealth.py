import random
import re

class StealthProcessor:
    def __init__(self):
        self.fillers = [
            "actually", "basically", "honestly", "you know",
            "well", "so", "like", "literally", "seriously"
        ]
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't"
        }
    
    def add_fillers(self, text):
        words = text.split()
        if len(words) > 8:
            for _ in range(random.randint(1, 3)):
                idx = random.randint(3, len(words)-3)
                words.insert(idx, random.choice(self.fillers))
        return " ".join(words)
    
    def add_contractions(self, text):
        for formal, casual in self.contractions.items():
            if random.random() > 0.4:
                text = text.replace(formal, casual)
        return text
    
    def vary_sentences(self, text):
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > 2:
            for i in range(len(sentences)):
                words = sentences[i].split()
                if i % 2 == 0 and len(words) > 8:
                    sentences[i] = " ".join(words[:len(words)//2]) + "..."
                elif i % 3 == 0 and len(words) < 5:
                    sentences[i] += " and stuff like that"
        return ". ".join(sentences)
    
    def process(self, text):
        text = self.add_contractions(text)
        text = self.add_fillers(text)
        text = self.vary_sentences(text)
        return text