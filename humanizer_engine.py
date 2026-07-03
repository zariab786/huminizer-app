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
        
        # Expanded fillers
        self.fillers = [
            "actually", "basically", "honestly", "you know", "well", 
            "so", "like", "literally", "seriously", "just saying",
            "in my opinion", "to be honest", "I mean", "you see",
            "the thing is", "in other words", "as a matter of fact",
            "believe it or not", "interestingly", "for the most part",
            "at the end of the day", "without a doubt", "it seems that"
        ]
        
        # More contractions
        self.contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "i am": "i'm", "you are": "you're", "it is": "it's",
            "that is": "that's", "are not": "aren't", "is not": "isn't",
            "was not": "wasn't", "were not": "weren't", "have not": "haven't",
            "has not": "hasn't", "had not": "hadn't", "would not": "wouldn't",
            "should not": "shouldn't", "could not": "couldn't", "does not": "doesn't",
            "cannot": "can't", "will not": "won't"
        }
        
        # WordNet is loaded but we'll access it through NLTK
        self.wordnet_loaded = True
        
    def _get_synonyms(self, word, max_synonyms=3):
        """Get synonyms from WordNet for a word"""
        try:
            synonyms = set()
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    # Only keep single-word synonyms that are different from the original
                    lemma_name = lemma.name().replace('_', ' ')
                    if lemma_name.lower() != word.lower() and ' ' not in lemma_name:
                        synonyms.add(lemma_name.lower())
                        if len(synonyms) >= max_synonyms * 2:
                            break
                if len(synonyms) >= max_synonyms * 2:
                    break
            
            # Remove the original word if it appears in synonyms
            synonyms.discard(word.lower())
            
            # Return a random subset
            return list(synonyms)[:max_synonyms] if synonyms else []
        except:
            return []
    
    def _replace_with_synonym(self, word):
        """Replace a word with a synonym (or not)"""
        # Skip short or common words
        if len(word) < 4 or word.lower() in ['the', 'and', 'for', 'you', 'are', 'was', 'were', 'have']:
            return word
        
        # 40% chance of replacement
        if random.random() > 0.4:
            return word
            
        # Get synonyms
        synonyms = self._get_synonyms(word, max_synonyms=2)
        if synonyms:
            # Sometimes use 2-word synonyms if available
            if len(synonyms) >= 2 and random.random() > 0.7:
                return random.choice(synonyms)
            return random.choice(synonyms)
        return word
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - V3.0 with massive vocabulary"""
        if not text or len(text) < 5:
            return text
        try:
            # Step 1: Paraphrase (longer output)
            paraphrased = self._paraphrase(text)
            
            # Step 2: Apply synonyms (massive vocabulary expansion)
            synonymized = self._apply_synonyms(paraphrased)
            
            # Step 3: Add human touches (fillers, contractions)
            humanized = self._add_human_touches(synonymized, style)
            
            # Step 4: Restructure sentences
            restructured = self._restructure_sentences(humanized)
            
            # Step 5: Anti-detection layer
            final = self._stealth_layer(restructured)
            
            # Step 6: Ensure we return string
            if final is None or final == "":
                return text
            final_str = str(final)
            if final_str.lower() in ["true", "false", "none"]:
                return text
            
            # Step 7: Try to expand or compress if needed
            final_str = self._adjust_length(final_str, len(text.split()))
            
            return final_str
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _paraphrase(self, text):
        """Paraphrase using T5 - with longer output"""
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
                    max_length=400,  # Increased from 200 to 400
                    num_beams=5,      # More beams = better quality
                    temperature=0.9,
                    top_p=0.92,
                    do_sample=True,
                    early_stopping=True,
                    repetition_penalty=1.2,  # Avoid repetitive phrases
                    num_return_sequences=1,
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
    
    def _apply_synonyms(self, text):
        """Apply synonyms to increase vocabulary diversity"""
        if not text:
            return text
            
        words = text.split()
        # Replace 30-40% of the words with synonyms
        for i in range(len(words)):
            # Clean the word (remove punctuation)
            clean_word = words[i].strip('.,!?;:()')
            if clean_word and len(clean_word) > 3:
                replacement = self._replace_with_synonym(clean_word)
                if replacement != clean_word:
                    # Preserve capitalization
                    if clean_word[0].isupper():
                        replacement = replacement.capitalize()
                    words[i] = replacement
        
        return " ".join(words)
    
    def _restructure_sentences(self, text):
        """Change sentence structure - active/passive, fronting, cleft sentences"""
        if not text:
            return text
            
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if len(sentences) <= 1:
            return text
            
        # Randomly apply different restructuring
        for i in range(len(sentences)):
            if len(sentences[i].split()) < 5:
                continue
                
            chance = random.random()
            
            # Active -> Passive (15% chance)
            if chance < 0.15:
                words = sentences[i].split()
                # Very simple pattern: "subject verb object" -> "object by subject verb"
                # This is simplified - in production you'd use a proper parser
                if len(words) >= 4:
                    # Simple transformation for demo
                    if words[0] not in ['the', 'a', 'an']:
                        words = [words[-1], 'by'] + words[:-1]
                        sentences[i] = " ".join(words)
            
            # Fronting (10% chance)
            elif chance < 0.25:
                words = sentences[i].split()
                if len(words) >= 4:
                    # Move the last phrase to the front
                    front = words[-2:]
                    rest = words[:-2]
                    sentences[i] = " ".join(front + rest)
        
        return ". ".join(sentences)
    
    def _adjust_length(self, text, target_word_count):
        """Adjust length to be +/- 20% of original"""
        if not text:
            return text
        
        words = text.split()
        current_count = len(words)
        target_count = int(target_word_count * random.uniform(0.85, 1.15))  # +/- 15%
        
        if current_count == 0:
            return text
            
        # If too short, add filler phrases
        if current_count < target_count:
            expansion_phrases = [
                " and that's really important",
                " in many ways",
                " to be precise",
                " as you might expect",
                " no doubt about it",
                " in the grand scheme of things"
            ]
            while len(words) < target_count:
                idx = random.randint(1, max(1, len(words)-1))
                phrase = random.choice(expansion_phrases)
                if len(words) + len(phrase.split()) <= target_count + 5:
                    words.insert(idx, phrase)
                else:
                    break
            return " ".join(words)
        
        # If too long, shorten
        elif current_count > target_count:
            # Remove filler phrases or shorten long sentences
            remove_phrases = [
                " and all that stuff",
                " and things like that",
                " you know what I mean",
                " basically",
                " actually"
            ]
            for phrase in remove_phrases:
                if phrase in text:
                    text = text.replace(phrase, "")
                    current_count = len(text.split())
                    if current_count <= target_count:
                        break
            
            # If still too long, truncate from the middle
            if current_count > target_count:
                words = text.split()
                remove_count = current_count - target_count
                # Remove from the middle
                start_idx = len(words)//2 - remove_count//2
                end_idx = len(words)//2 + remove_count//2
                if start_idx > 0 and end_idx < len(words):
                    words = words[:start_idx] + ["..."] + words[end_idx:]
                return " ".join(words)
        
        return text
    
    def _add_human_touches(self, text, style):
        """Add human-like imperfections"""
        if not text:
            return text
        result = text
        
        # Apply contractions
        for formal, casual in self.contractions.items():
            if random.random() > 0.5:
                result = result.replace(formal, casual)
        
        # Add filler words
        filler_count = {
            "casual": random.randint(3, 6),
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
        
        return result
    
    def _stealth_layer(self, text):
        """Final anti-detection processing"""
        if not text:
            return text
        result = text
        
        # Remove common AI patterns
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
        
        return result
    
    def get_stealth_score(self, text):
        """Estimate how human-like the text is (0-100)"""
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
        
        # Vocabulary diversity (using WordNet synonyms)
        unique_words = len(set(words))
        if unique_words / len(words) > 0.5:
            score += 8
        
        # Sentence length variation
        sentences = [s for s in text.split(". ") if s]
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            if max(lengths) - min(lengths) > 10:
                score += 7
        
        # Filler words
        if any(filler in text.lower() for filler in self.fillers):
            score += 7
        
        # Length bonus
        if len(words) > 100:
            score += 5
        elif len(words) > 50:
            score += 3
        
        return min(score, 99)
