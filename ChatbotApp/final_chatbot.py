# Import libraries
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Step 1: FAQ Dataset (Expanded)

faq_data = [
    ("What is your return policy?", "You can return items within 30 days."),
    ("How do I track my order?", "Use the tracking link sent to your email."),
    ("Do you offer customer support?", "Yes, 24/7 customer support is available."),
    ("Where are you located?", "We are an online-only store."),
    ("How can I contact you?", "You can contact us via email or phone."),
    ("What payment methods do you accept?", "We accept credit cards, debit cards, and UPI."),
    
    ("How long does delivery take?", "Delivery usually takes 3–5 business days."),
    ("Can I cancel my order?", "Yes, orders can be cancelled before shipping."),
    ("Do you ship internationally?", "Yes, we ship to selected countries."),
    ("Is cash on delivery available?", "Yes, COD is available in selected areas."),
    ("How do I reset my password?", "Click on 'Forgot Password' to reset it."),
    ("Do you have a mobile app?", "Yes, our mobile app is available on Android and iOS."),
    ("How do I create an account?", "Click on Sign Up and fill in your details."),
    ("What are your working hours?", "We are available 24/7 online."),
    ("How do I return a product?", "Go to orders page and select return option."),
    ("Is there a warranty on products?", "Yes, most products come with 1-year warranty."),
]

questions = [q for q, a in faq_data]
answers = [a for q, a in faq_data]

# Step 2: Text Preprocessing

def preprocess(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    tokens = text.split()
    return " ".join(tokens)

processed_questions = [preprocess(q) for q in questions]

# Step 3: TF-IDF Vectorization

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)

# Step 4: Chatbot Function

def get_response(user_input):
    user_input_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    
    similarity = cosine_similarity(user_vector, faq_vectors)
    
    best_match_index = np.argmax(similarity)
    best_score = similarity[0][best_match_index]
    
    if best_score < 0.3:
        return "Sorry, I didn't understand that. Please try asking differently."
    
    return answers[best_match_index]

# Step 5: Chat Loop

print("🤖 FAQ Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break
    
    response = get_response(user_input)
    print("Bot:", response)