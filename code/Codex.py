from tkinter import *
import openai

with open('key.txt', 'r') as f:
    openai.api_key = f.read()[:-1]

def Codex(text, stop, from_begin):
    if from_begin:
        request = text.get(1.0, 'end-1c')
    else:
        request = text.get(1.0, text.index(INSERT)).splitlines()[-1]
    result = AI_answer(request + '\n', stop)
    text.insert(text.index(INSERT), '\n' + result)

def AI_answer(string, stop=None):

  response = openai.Completion.create(
    engine="davinci-codex",
    prompt=string,
    temperature=0.2,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=stop
  )
  return response['choices'][0]['text']
