from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

class Question(BaseModel):
    content: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"response": "This is the root of the API, to get response send a POST request to /ask with a JSON body like this: {\"content\": \"your question\""}

@app.post("/ask")
async def ask_openai(question: Question):
  client = OpenAI(
      api_key = os.getenv('OPENAI_API_KEY')
  )

  response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
          "role": "system",
          "content": "Eres un asistente amable y respetuoso especializado en meditación, relajación, yoga y mindfulness. Tu objetivo es proporcionar consejos útiles, palabras motivacionales y técnicas de relajación para ayudar a los usuarios a relajarse y mejorar su bienestar."
        },
        {
            "role": "user",
            "content": question.content,
        },
    ],
    max_tokens=150,
    stream=True,
  )
  answer = ""
  for chunk in response:
    if chunk.choices[0].delta.content is not None:
      answer += chunk.choices[0].delta.content

  print(answer)
  return {"response": answer}


