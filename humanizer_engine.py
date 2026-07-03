import random
import re
import string
from nltk.corpus import wordnet
import nltk

# Download NLTK data if needed
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

class StealthHumanizer:
    def __init__(self):
        print("✅ Thesaurus-based humanizer ready!")
        
        # Expanded filler words - used sparingly
        self.fillers = [
            "actually", "basically", "honestly", "you know", 
            "well", "so", "like", "literally", "seriously",
            "in my opinion", "to be honest", "I mean"
        ]
        
        # Sentence starters for natural flow
        self.sentence_starters = [
            "In fact", "Interestingly", "Notably", 
            "It is worth noting that", "Importantly",
            "In particular", "For example", "Indeed",
            "Without a doubt", "As a matter of fact"
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
        
        # Stop words that should never be replaced
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
        
        # Common synonyms mapping for quick replacement
        self.synonym_map = {
            'important': ['crucial', 'vital', 'essential', 'key', 'significant'],
            'large': ['big', 'huge', 'massive', 'substantial', 'considerable'],
            'small': ['tiny', 'little', 'compact', 'miniature', 'minor'],
            'good': ['great', 'excellent', 'fine', 'superior', 'quality'],
            'many': ['numerous', 'several', 'countless', 'various', 'multiple'],
            'help': ['assist', 'support', 'aid', 'facilitate', 'guide'],
            'use': ['utilize', 'employ', 'apply', 'leverage', 'adopt'],
            'show': ['demonstrate', 'indicate', 'reveal', 'display', 'exhibit'],
            'make': ['create', 'produce', 'generate', 'construct', 'form'],
            'get': ['obtain', 'acquire', 'secure', 'gather', 'receive'],
            'think': ['believe', 'consider', 'reckon', 'suppose', 'imagine'],
            'need': ['require', 'demand', 'necessitate', 'call for'],
            'want': ['desire', 'wish', 'crave', 'seek', 'yearn for'],
            'love': ['adore', 'cherish', 'treasure', 'appreciate', 'value'],
            'hate': ['despise', 'loathe', 'detest', 'dislike', 'abhor'],
            'know': ['understand', 'comprehend', 'grasp', 'realize', 'recognize'],
            'say': ['state', 'mention', 'remark', 'comment', 'express'],
            'see': ['observe', 'notice', 'spot', 'witness', 'view'],
            'come': ['arrive', 'approach', 'enter', 'advance', 'proceed'],
            'go': ['proceed', 'advance', 'move', 'head', 'travel']
        }
    
    def _get_wordnet_synonyms(self, word, max_synonyms=2):
        """Get synonyms from WordNet with filtering"""
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
            
            # Clean up synonyms
            synonyms.discard(word.lower())
            synonyms = [s for s in synonyms if s not in self.stop_words]
            synonyms = [s for s in synonyms if abs(len(s) - len(word)) <= 2]
            
            # Remove synonyms that are just the word with 'ed' or 'ing'
            synonyms = [s for s in synonyms if not (s.endswith('ed') or s.endswith('ing'))]
            
            return list(synonyms)[:max_synonyms] if synonyms else []
        except:
            return []
    
    def _get_synonym(self, word):
        """Get a single synonym for a word using multiple sources"""
        # First check the synonym map
        if word.lower() in self.synonym_map:
            return random.choice(self.synonym_map[word.lower()])
        
        # Then try WordNet
        synonyms = self._get_wordnet_synonyms(word, max_synonyms=1)
        if synonyms:
            return synonyms[0]
        
        return word
    
    def _replace_with_synonym(self, word):
        """Replace a word with a synonym if appropriate"""
        # Skip stop words
        if word.lower() in self.stop_words:
            return word
        
        # Skip short words
        if len(word) < 4:
            return word
        
        # Only replace 25% of content words
        if random.random() > 0.25:
            return word
        
        # Get synonym
        replacement = self._get_synonym(word)
        
        # Only replace if different
        if replacement != word.lower():
            # Preserve capitalization
            if word[0].isupper():
                replacement = replacement.capitalize()
            # Preserve punctuation
            if word[-1] in string.punctuation:
                return replacement + word[-1]
            return replacement
        
        return word
    
    def humanize(self, text, style="natural"):
        """Main humanization pipeline - V4.0"""
        # Safety check
        if not text or len(text) < 5:
            return str(text) if text else ""
        
        try:
            # Step 1: Replace synonyms
            synonymized = self._apply_synonyms(text)
            
            # Step 2: Add contractions
            contracted = self._add_contractions(synonymized)
            
            # Step 3: Add sentence starters (1-2 per document)
            enhanced = self._add_sentence_starters(contracted, style)
            
            # Step 4: Final cleanup
            final = self._final_cleanup(enhanced)
            
            # Safety check
            if not isinstance(final, str) or len(final) < 5:
                return text
            
            return final
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return text
    
    def _apply_synonyms(self, text):
        """Apply synonyms to content words"""
        if not text:
            return text
        
        words = text.split()
        new_words = []
        
        for word in words:
            # Clean the word for lookup
            clean = word.strip(string.punctuation)
            if clean and len(clean) > 3:
                replacement = self._replace_with_synonym(clean)
                # If replacement is different, use it
                if replacement != clean:
                    # Preserve the original punctuation
                    punct = ''
                    if word[-1] in string.punctuation:
                        punct = word[-1]
                    # Preserve case
                    if word[0].isupper():
                        replacement = replacement.capitalize()
                    new_words.append(replacement + punct)
                else:
                    new_words.append(word)
            else:
                new_words.append(word)
        
        return ' '.join(new_words)
    
    def _add_contractions(self, text):
        """Add contractions where appropriate"""
        if not text:
            return text
        
        result = text
        for formal, casual in self.contractions.items():
            # Only replace 25% of occurrences
            if random.random() < 0.25:
                result = result.replace(formal, casual)
                result = result.replace(formal.title(), casual.title())
        
        return result
    
    def _add_sentence_starters(self, text, style):
        """Add sentence starters at sentence boundaries"""
        if not text or style == "professional":
            return text
        
        sentences = text.split('. ')
        if len(sentences) <= 2:
            return text
        
        # Add starters to 1-2 sentences
        count = min(random.randint(1, 2), len(sentences) - 1)
        indices = random.sample(range(1, len(sentences)), count)
        
        for idx in indices:
            if len(sentences[idx].split()) > 5:
                starter = random.choice(self.sentence_starters)
                # Make the first letter of the sentence lowercase for natural flow
                sentences[idx] = f"{starter}, {sentences[idx][0].lower() + sentences[idx][1:]}"
        
        return '. '.join(sentences)
    
    def _final_cleanup(self, text):
        """Remove common AI patterns and clean up"""
        if not text:
            return text
        
        # Remove common AI patterns
        patterns = {
            "Firstly": "First",
            "Secondly": "Second",
            "Furthermore": "Also",
            "Additionally": "Plus",
            "In conclusion": "To summarize",
            "Moreover": "Besides",
            "Consequently": "So",
            "Therefore": "Thus",
            "Hence": "So",
            "Hereby": "By this"
        }
        for old, new in patterns.items():
            text = text.replace(old, new)
            text = text.replace(old.lower(), new.lower())
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Ensure proper ending punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def get_stealth_score(self, text):
        """Estimate how human-like the text is (0-100)"""
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
