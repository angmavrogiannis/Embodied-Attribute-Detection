import speech_recognition as sr
import robomaster

"""
    Listens to a verbal command and returns a textual version of it
    Reference: https://towardsdatascience.com/easy-speech-to-text-with-python-3df0d973b426
"""
def hear() -> str:
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Microphone as source
    # Listen to the speech and store in audio_text variable
    with sr.Microphone() as source:
        if input():
            print("Talk")
            audio_text = r.listen(source, phrase_time_limit=3)
            print("Time over")

    # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition
        instruction = r.recognize_google(audio_text)
    except:
        instruction = "Sorry, I did not get that"
    print("Text: " + instruction)
    return instruction