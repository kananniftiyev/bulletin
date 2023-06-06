import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models
import re
import string

# Download stopwords and wordnet if not already downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')  # Download the 'punkt' tokenizer

class TopicModel:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = set(string.punctuation)
        
    def preprocess_text(self, text):
        if text is None:
            return []
        
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and punctuation
        tokens = [token for token in tokens if token not in self.stop_words and token not in self.punctuation]
        
        # Lemmatize the tokens
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def getTopic(self, text, num_topics=5):
        # Preprocess the text
        tokens = self.preprocess_text(text)
        
        if not tokens:
            return None
        
        # Create a dictionary from the tokens
        dictionary = corpora.Dictionary([tokens])
        
        # Create a bag-of-words representation of the text
        corpus = [dictionary.doc2bow(tokens)]
        
        # Build the LDA model
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
        
        # Get the topics
        topics = lda_model.print_topics(num_topics=num_topics)
        
        top_topic = topics[0]  # Get the first topic
        
        # Extract the topic keywords using regular expressions and exclude punctuation marks
        topic_keywords = re.findall(r'"([^"]*)"', top_topic[1])
        topic_keywords = [keyword for keyword in topic_keywords if keyword not in self.punctuation]
        
        if topic_keywords:
            first_keyword = topic_keywords[0]
            return first_keyword.capitalize()  # Capitalize the first keyword
        else:
            return None
