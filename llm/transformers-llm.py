import speech_recognition as sr
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import random
import difflib

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load pre-trained GPT model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Function to generate a random sentence using GPT model
def generate_sentence(context):
    input_ids = tokenizer.encode(context, return_tensors="pt")
    max_length = random.randint(10, 50)  # Adjust the maximum length of generated text
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

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
        prompt = generate_sentence("Tell me something to help me learn English")
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