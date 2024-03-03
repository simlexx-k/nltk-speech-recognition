import speech_recognition as sr
import datetime
import sys

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define predefined commands and their corresponding actions
commands = {
    "hello": "Hello! How can I help you?",
    "time": "Current time is ",  # Replace XX:XX with actual time
    "weather": "The weather is sunny today.",  # Replace with actual weather data
    "exit": "Stoping program..."
}

# Function to recognize and execute commands
def execute_command(text):
    for command, action in commands.items():
        if command in text.lower():
            return action
    return "Command not recognized."

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


if __name__ == "__main__":
    while True:
        text = capture_and_transcribe()
        action = execute_command(text)
        print(action)
        if "exit" in text.lower():
            print("Exiting application. Goodbye!")
            sys.exit()