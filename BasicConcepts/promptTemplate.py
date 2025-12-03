from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory

llm = ChatOllama(model="llama3-chatqa")

# Create memory object (useful for AUTO history)
history = InMemoryChatMessageHistory()

# Create prompt with placeholder for memory
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder("chat_history"),
    ("human", "{user_input}")
])

while True:
    user_input = input("\nYou: ")

    # Format prompt with current history + new user input
    final_prompt = prompt.format(
        chat_history=history.messages,
        user_input=user_input
    )


    response = llm.invoke(final_prompt)

    print("AI:", response.content)

    # --- AUTO SAVE HISTORY ---
    history.add_user_message(user_input)
    history.add_ai_message(response.content)
