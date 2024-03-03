import speech_recognition as sr
import nltk
import random
import difflib

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define predefined prompts for language learning
prompts = [
    "Hello, how are you?",
    "What's your name?",
    "Where are you from?",
    "Can you tell me about your hobbies?",
    "Describe your favorite place to visit.",
    "Talk about your daily routine.",
]

# Function to select a random prompt for the user
def get_prompt():
    return random.choice(prompts)

# Function to capture audio and transcribe it
def capture_and_transcribe():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)

# Function to evaluate pronunciation based on similarity score
def evaluate_pronunciation(original, spoken):
    similarity = difflib.SequenceMatcher(None, original, spoken).ratio()
    return similarity * 100

if __name__ == "__main__":
    print("Welcome to English Language Learning Assistant!")
    print("You can practice speaking English by repeating after me.")
    print("You can also say 'exit' to quit.")

    while True:
        prompt = get_prompt()
        print("Prompt:", prompt)
        text = capture_and_transcribe()
        if "exit" in text.lower():
            break
        else:
            print("Original Prompt:", prompt)
            print("Your Response:", text)
            similarity_score = evaluate_pronunciation(prompt.lower(), text.lower())
            print("Pronunciation Similarity: {:.2f}%".format(similarity_score))
            if similarity_score >= 70:
                print("Your pronunciation is good!")
            else:
                print("You may need to practice your pronunciation.")
