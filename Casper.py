# Brian Kasper 2018

import time
import wolframalpha
import wikipedia
import requests
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

# Unique App ID from Wolfram Alpha
client = wolframalpha.Client('4KXRH3-YK694P27XJ')

# Search Wikipedia
def search_wiki(keyword=''):
  # Use keyword to make initial search
  searchResults = wikipedia.search(keyword)
  
  # If search returns nothing print error message
  if not searchResults:
    print("No results found from Wikipedia")
    return None

  # Return best result if disambiguation arries 
  try:
    page = wikipedia.page(searchResults[0])
  except wikipedia.DisambiguationError as err:
    page = wikipedia.page(err.options[0])
  
  # Return results
  return [str(page.title.encode('utf-8')), str(page.summary.encode('utf-8'))]
    
# Use Wolfram Alpha to interpret input and attempt to answer question
def search_wolfram(text=''):
  
  # Result from input
  res = client.query(text)
  
  # If Wolfram cant interpret the input print an error message
  if res['@success'] == 'false':
    print("Wolfram Alpha cannot interpret the input.")
    return None
  
  # If Wolfram can interpret the input
  else:
    result = ''
    
    # Question
    pod0 = res['pod'][0]
    question = resolveListOrDict(pod0['subpod']).split('(')[0]
    
    # Answer
    pod1 = res['pod'][1]
    
    # If Wolfram has the answer
    if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
      
      # Return Results
      return [question, resolveListOrDict(pod1['subpod'])]
    
    # If wolfram does not have the answer try searching wikipedia
    else:
      return search_wiki(question)

# Return string from list or dictionary input
def resolveListOrDict(variable):
  # If input is a list
  if isinstance(variable, list):
    return variable[0]['plaintext']
  # If input is a dictionary
  else:
    return variable['plaintext']

# Convert string to audio
def speak(audioString):
  print(audioString)
  tts = gTTS(text=audioString, lang='en')
  tts.save("audio.mp3")
  mixer.init()
  mixer.music.load('audio.mp3')
  mixer.music.play()
 
def recordAudio():
  # Record Audio
  r = sr.Recognizer()
  with sr.Microphone() as source:
    speak("Ask me a question!")
    time.sleep(2)
    audio = r.listen(source)
 
  # Speech recognition using Google Speech Recognition
  try:
    data = r.recognize_google(audio)
    print("You said: " + data)
    return data
  except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    return None
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

# Greeting 
speak("Hi my name is Casper.")
time.sleep(2)
question = recordAudio()

# Loop until user says "I am done"
while True:
  # If google can recognize audio
  if question != None:
    if "I am done" in question:
      break

    # First try wolfram to find answer
    answer = search_wolfram(question)
    
    # If wolfram or wikipedia found answer
    if answer != None:
      speak(answer[1])
      time.sleep(len(answer[1]) // 5)
    else:
      speak("Sorry, I could not find an answer to your question")
      time.sleep(5)

  # Continue to get user input
  question = recordAudio()

