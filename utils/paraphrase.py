from transformers import pipeline

class Paraphraser:
    def __init__(self):
        self.paraphraser = pipeline(
            "text2text-generation",
            model="t5-base",
            device=-1
        )
    
    def paraphrase(self, text, num_return=1):
        result = self.paraphraser(
            f"paraphrase: {text}",
            max_length=512,
            num_return_sequences=num_return,
            temperature=0.9
        )
        return [r['generated_text'] for r in result]