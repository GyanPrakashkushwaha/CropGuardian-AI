from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


if not load_dotenv():
    raise Exception("API KEY NOT LOADED")


def get_gemini_model(model_name = "gemini-2.0-flash", temperature = 0):
    model = ChatGoogleGenerativeAI(
        model = f"models/{model_name}",
        temperature = temperature,
        api_key = os.getenv("GEMINI_API_KEY")
    )
    return model