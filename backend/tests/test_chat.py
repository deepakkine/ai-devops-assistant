from app.services.chat_service import ChatService

chat = ChatService()

question = "How is the VPC created?"

answer = chat.chat(question)

print()
print(answer)