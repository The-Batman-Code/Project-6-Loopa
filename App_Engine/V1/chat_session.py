from vertexai.language_models import ChatModel, InputOutputTextPair, ChatSession
import vertexai
from starlette.responses import JSONResponse
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("loopa_key.json")

vertexai.init(project="", location="us-central1", credentials=credentials)


class CreateChatSession:
    def __init__(self):
        self.context = ""
        self.session = ChatSession(
            model=ChatModel.from_pretrained("chat-bison"),
            context=self.context,
            max_output_tokens=1024,
            temperature=0.2,
            top_k=40,
            top_p=0.8,
        )

    def create_chat_session(self, user_text):
        response = self.session.send_message(user_text)
        return JSONResponse(content={"message": response.text})
