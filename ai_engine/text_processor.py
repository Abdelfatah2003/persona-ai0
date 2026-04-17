import re
import string

try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

class TextProcessor:
    STOP_WORDS = {
        'en': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
               'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
               'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
               'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
               'used', 'it', 'its', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
               'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'they',
               'them', 'their', 'this', 'that', 'these', 'those', 'am', 'about', 'which',
               'who', 'whom', 'what', 'where', 'when', 'why', 'how', 'all', 'each',
               'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
               'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
               'also', 'now', 'here', 'there', 'then', 'once', 'if', 'because', 'until',
               'while', 'although', 'though', 'after', 'before', 'above', 'below', 'between',
               'into', 'through', 'during', 'under', 'again', 'further', 'out', 'up', 'down',
               'off', 'over', 'under', 'again', 'back', 'being', 'having', 'doing', 'going',
               'like', 'get', 'got', 'make', 'made', 'know', 'knew', 'think', 'thought',
               'see', 'saw', 'want', 'seem', 'look', 'try', 'keep', 'give', 'gave', 'take',
               'took', 'come', 'came', 'say', 'said', 'tell', 'told', 'ask', 'asked'},
        'ar': {'في', 'من', 'على', 'إلى', 'عن', 'مع', 'أن', 'هذا', 'هذه', 'التي', 'الذي',
               'التى', 'اللذين', 'اللتين', 'اللواتي', 'الآن', 'بعد', 'قبل', 'بين', 'عند',
               'ثم', 'أو', 'و', 'لا', 'ما', 'هو', 'هي', 'هم', 'هن', 'أنا', 'نحن', 'أنت',
               'أنتن', 'إنه', 'إنها', 'لقد', 'كان', 'كانت', 'كانوا', 'أصبح', 'ليس', 'غير'}
    }
    
    def __init__(self, lang='en'):
        self.lang = lang
        self.stop_words = self.STOP_WORDS.get(lang, self.STOP_WORDS['en'])
    
    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'http\S+|www.\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        if NLTK_AVAILABLE:
            try:
                tokens = word_tokenize(text)
                tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]
                return ' '.join(tokens)
            except:
                pass
        
        words = text.split()
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        return ' '.join(words)
    
    def extract_keywords(self, text, top_n=10):
        words = text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
    
    def tokenize(self, text):
        return text.split()
    
    def to_vector(self, text, vocabulary):
        tokens = self.tokenize(text)
        vector = [1 if word in tokens else 0 for word in vocabulary]
        return vector
