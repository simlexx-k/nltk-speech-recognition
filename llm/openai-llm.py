import speech_recognition as sr
import openai
import random
import difflib

# Initialize the recognizer
recognizer = sr.Recognizer()

# Set your OpenAI API key
openai.api_key = 'API-KEY'

# Function to generate a random sentence using OpenAI GPT model
def generate_sentence(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-1106",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

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
        prompt = "Tell me something to help me learn English"
        generated_prompt = generate_sentence(prompt)
        print("Prompt:", generated_prompt)
        text = capture_and_transcribe()
        if "exit" in text.lower():
            break
        else:
            print("Original Prompt:", generated_prompt)
            print("Your Response:", text)
            similarity_score = evaluate_pronunciation(generated_prompt.lower(), text.lower())
            print("Pronunciation Similarity: {:.2f}%".format(similarity_score))
            if similarity_score >= 70:
                print("Your pronunciation is good!")
            else:
                print("You may need to practice your pronunciation.")
