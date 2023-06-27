import speech_recognition as sr
import multiprocessing
from vk import startVirtualKeyboard
from VirtualMouse import startVirtualMouse

def listen_microphone(timeout=2):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Adjust microphone for ambient noise

        try:
            audio = r.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("Microphone inactive for {} seconds. Stopping...".format(timeout))
            return ""

    try:
        print("Recognizing...")
        text = r.recognize_google(audio)  # Uses Google Speech Recognition API
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service: {0}".format(e))

    return ""

def keyboardProcessFunction():
    startVirtualKeyboard()

def mouseProcessFunction():
    startVirtualMouse()

if __name__ == '__main__':
    command = ""
    keyboardProcess = None
    mouseProcess = None

    while True:
        text = listen_microphone()
        text = text.lower()
        text = text.strip()
        if text:
            print("You said:", text)
            if "start keyboard" in text and keyboardProcess is None:
                print("Starting keyboard process...")
                keyboardProcess = multiprocessing.Process(target=keyboardProcessFunction)
                keyboardProcess.start()
            elif "stop keyboard" in text and keyboardProcess is not None:
                print("Stopping the keyboard process...")
                keyboardProcess.terminate()
                keyboardProcess.join()
                keyboardProcess = None
            elif "start mouse" in text and mouseProcess is None:
                print("Starting mouse process...")
                mouseProcess = multiprocessing.Process(target=mouseProcessFunction)
                mouseProcess.start()
            elif "stop mouse" in text and mouseProcess is not None:
                print("Stopping the mouse process...")
                mouseProcess.terminate()
                mouseProcess.join()
                mouseProcess = None
