import vertexai
from starlette.responses import JSONResponse
import vertexai
import google.generativeai as genai
import json

vertexai.init(project="ENTER YOUR PROJECT ID HERE", location="us-central1")

genai.configure(
    api_key="ENTER API KEY HERE OBTAINED FROM GOOGLE AI STUDIO HERE- https://aistudio.google.com/app/prompts/new_chat"
)


class CreateChatSession:
    def __init__(self):
        self.generationconfig = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_k": 40,
            "top_p": 0.8,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro", generation_config=self.generationconfig
        )
        self.his = [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Your name is Loopa. Act as an investment advisor and always get the latest information whenever available. Answer the user like an Invesment advisor only and elaborate the response as much as possible."
                    }
                ],
            },
            {"role": "model", "parts": [{"text": "Understood."}]},
        ]
        self.session = self.model.start_chat(history=self.his)

    def create_chat_session(self, user_text):
        response = self.session.send_message(user_text)
        return JSONResponse(content={"message": response.text})
