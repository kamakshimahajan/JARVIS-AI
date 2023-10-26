import os
import speech_recognition as sr
import win32com.client
import webbrowser
import openai
from config import apikey
import datetime

def ai(prompt):
    openai.api_key=apikey
    text=f"OpenAI response for Prompt: {prompt} \n*********************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text+=response["choices"][0]["text"]
    # print(response["choices"][0]["text"])
    if not os.path.exists("OpenAi"):
        os.mkdir("OpenAi")

    with open(f"OpenAi/{''.join(prompt.split('intelligence')[1:])}.txt","w")as f:
        f.write(text)

speaker=win32com.client.Dispatch("SAPI.SpVoice")
print("Enter the word you want to speak it out by computer");

chatStr=""
def chat(query):
    global chatStr
    print(query)
    # print(chatStr)
    openai.api_key = apikey
    chatStr += f"Armaan: {query}\n J.A.R.V.I.S : "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speaker.Speak(response["choices"][0]["text"])
    print(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    # print(chatStr)
    return response["choices"][0]["text"]


def takeCommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=1;
        audio=r.listen(source)
    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Error in accessing the Google Speech Recognition API. Check your internet connection.")
        return ""

if __name__=='__main__':
    # print('Pycharm');
    speaker.Speak('Hello, My name is Jarvis and I am your personal assistant')
    while True:
        query=takeCommand();
        boolean=True
        sites=[["youtube","https://www.youtube.com"],["wikipeida","https://www.wikipedia.com"],["google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                boolean=False
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break
        if boolean:
            if "the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                speaker.speak(f"Sir the time is {strfTime}")
            elif "using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
            elif "Bye jarvis".lower() in query.lower():
                exit()
            elif "forget everything".lower() in query.lower():
                chatStr = ""
            else:
                print("Talking...")
                chat(query)

