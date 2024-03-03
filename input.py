import speech_recognition as sr
import nltk

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to continuously capture audio and transcribe it
def continuous_speech_recognition():
    with sr.Microphone() as source:
        print("Speak something...")
        # Continuously listen for speech
        while True:
            try:
                audio = recognizer.listen(source, timeout=60)  # Adjust timeout as needed
                text = recognizer.recognize_google(audio)
                print("You said:", text)

                # Now you can use NLTK for text processing tasks on the transcribed text
                # For example:
                tokens = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(tokens)
                print(tagged)
                # ...
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
            except KeyboardInterrupt:
                print("Stopped listening.")
                break

# Call the function to start continuous speech recognition
continuous_speech_recognition()
