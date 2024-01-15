# Import necessary libraries and modules
import os  # Operating system functions
import speech_recognition as sr  # Library for speech recognition
import win32com.client  # Module for text-to-speech functionality
import webbrowser  # Module for opening web browsers
import openai  # OpenAI GPT-3 API wrapper
from config import apikey  # Importing API key from a configuration file
import datetime  # Module for working with dates and times

# Function to interact with the OpenAI GPT-3 model
def ai(prompt):
    openai.api_key = apikey  # Set the API key for OpenAI
    text = f"OpenAI response for Prompt: {prompt} \n*********************\n\n"

    # Requesting completion from the GPT-3 model
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Appending GPT-3 response to the text
    text += response["choices"][0]["text"]

    # Saving the response to a file
    if not os.path.exists("OpenAi"):
        os.mkdir("OpenAi")

    with open(f"OpenAi/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)

# Initializing text-to-speech engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")
print("Enter the word you want to speak it out by computer")

chatStr = ""  # Variable to store chat history

# Function for chat interactions using GPT-3
def chat(query):
    global chatStr
    print(query)

    # Appending user input to the chat history
    chatStr += f"Armaan: {query}\n J.A.R.V.I.S : "

    # Requesting completion from the GPT-3 model
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Speaking the GPT-3 response and updating chat history
    speaker.Speak(response["choices"][0]["text"])
    print(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"

    return response["choices"][0]["text"]

# Function to recognize and return user's voice command
def takeCommand():
    r = sr.Recognizer()

    # Listening to the user's voice through the microphone
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")

        # Using Google's speech recognition to convert audio to text
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Error in accessing the Google Speech Recognition API. Check your internet connection.")
        return ""

# Main program execution
if __name__ == '__main__':
    # Greeting from the text-to-speech engine
    speaker.Speak('Hello, My name is Jarvis and I am your personal assistant')

    while True:
        # Getting user's voice command
        query = takeCommand()
        boolean = True
        sites = [["youtube", "https://www.youtube.com"], ["wikipeida", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]

        # Checking if the user wants to open a specific website
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                boolean = False
                speaker.Speak(f"Opening {site[0]} sir...")

                # Opening the specified website in a web browser
                webbrowser.open(site[1])
                break

        if boolean:
            # Checking for specific commands
            if "the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")

                # Speaking the current time
                speaker.speak(f"Sir the time is {strfTime}")
            elif "using artificial intelligence".lower() in query.lower():
                # Calling the function to interact with GPT-3 based on the user's query
                ai(prompt=query)
            elif "Bye jarvis".lower() in query.lower():
                # Exiting the program if the user says "Bye jarvis"
                exit()
            elif "forget everything".lower() in query.lower():
                # Clearing the chat history if the user says "forget everything"
                chatStr = ""
            else:
                print("Talking...")

                # Having a chat based on the user's query
                chat(query)
