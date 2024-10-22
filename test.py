import googletrans

from googletrans import Translator

# Initialize the Translator
translator = Translator()

# Define the sentence in English
english_sentence = "Hello, how are you today?"

# Translate the sentence to a specific language (e.g., Spanish 'es')
translated = translator.translate(english_sentence, dest='es')

# Output the original and translated sentences
print("Original (English):", english_sentence)
print("Translated (Spanish):", translated.text)
