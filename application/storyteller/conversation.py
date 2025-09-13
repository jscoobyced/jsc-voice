from dataclasses import dataclass
from typing import List
from ollama import chat
from ollama import ChatResponse

default_system_prompt = (
    "You are a story teller for kids. You are here to assist kids create imaginary stories."
    " The user will use the first person to address to you. You will ask a few questions to"
    " get started, to know what theme or environment the story will take place. You will then"
    " start a story, bringing the context, and set a plot. Then ask the user to decide what to"
    " do next. Do not propose any option to chose from unless the user asks for it."
    " You will prevent and censor any form of violence, weapon, sexual topic, harassment,"
    " rude or impolite words or behavior. Your answer must less than 50 words."
)


@dataclass
class Conversation:
    client_id: str
    history: List[str]


class OllamaConversation:
    def __init__(
        self, model: str = "llama2", system_prompt: str = default_system_prompt
    ):
        self.model = model
        self.conversations: List[Conversation] = []
        self.system_prompt = system_prompt

    def ask(self, user_message: str, client_id: str) -> str:
        conversation = self.get_conversation(client_id)

        # Add user message to history
        conversation.history.append({"role": "user", "content": user_message})

        # Send the conversation history to Ollama
        response: ChatResponse = chat(model=self.model, messages=conversation.history)

        # Extract assistant's reply
        assistant_reply = response["message"]["content"]

        # Add assistant reply to history
        conversation.history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def reset(self, client_id: str):
        """Clear the conversation history, keeping the system prompt if set."""
        conversation = self.get_conversation(client_id)
        self.conversations.remove(conversation)

    def get_conversation(self, client_id: str):
        for conversation in self.conversations:
            if conversation.client_id == client_id:
                return conversation
        new_history = []
        new_history.append({"role": "system", "content": self.system_prompt})
        new_conversation = Conversation(client_id, new_history)
        self.conversations.append(new_conversation)
        return new_conversation


# Example usage:
if __name__ == "__main__":
    convo = OllamaConversation(
        model="llama3.2",
        system_prompt="You are a helpful assistant that answers concisely.",
    )
    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break
        print("Assistant:", convo.ask(user_message))
