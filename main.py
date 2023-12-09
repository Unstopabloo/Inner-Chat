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

# app = FastAPI()

# client = OpenAI(
#   api_key = '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'
# )

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/chao")
# def read_root():
#     return {"response": "chao world"}

# response = client.chat.completions.create(
#   model='gpt-3.5-turbo',
#   messages=[
#     {
#       "role": "user",
#       "content": "Dime para que sirve el Mindfulness y como me puede ayudar"
#     }
#   ],
#   max_tokens=40,
#   stream=True,
# )
# for chunk in response:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")