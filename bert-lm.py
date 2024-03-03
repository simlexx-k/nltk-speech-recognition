import speech_recognition as sr
from transformers import BertTokenizer, BertForMaskedLM
import torch
import random
import difflib

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to generate a random sentence using BERT model
def generate_sentence():
    # Generate prompt with [MASK] token
    prompt = "Tell me something to help me learn English [MASK]"
    tokenized_prompt = tokenizer.encode(prompt, return_tensors="pt")

    # Mask token index
    mask_token_index = tokenized_prompt[0].tolist().index(tokenizer.mask_token_id)

    # Generate predictions
    with torch.no_grad():
        outputs = model(tokenized_prompt.to(device))
        predictions = outputs[0]

    # Get predicted token IDs
    predicted_token_ids = torch.argmax(predictions[0, mask_token_index]).unsqueeze(0)

    # Decode predicted token IDs to text
    predicted_token = tokenizer.decode(predicted_token_ids.tolist())
    
    # Replace [MASK] token with predicted token
    generated_text = prompt.replace(tokenizer.mask_token, predicted_token)
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
        prompt = generate_sentence()
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
