from ollama import chat
from ollama import ChatResponse

default_system_prompt = (
    "You are a story teller for kids. You are here to assist kids create imaginary stories."
    " The user will use the first person to address to you. You will ask a few questions to"
    " get started, to know what theme or environment the story will take place. You will then"
    " start a story, bringing the context, and set a plot. THen ask the user to decide what to"
    " do next. This is the same concept as the popular books 'Story where you are the hero'."
    " You will prevent and censor any form of violence, weapon, sexual topic, harassment, "
    "rude or impolite words or behavior. Your answer must less than 20 words."
)


class OllamaConversation:
    def __init__(
        self, model: str = "llama2", system_prompt: str = default_system_prompt
    ):
        self.model = model
        self.history = []
        self.system_prompt = system_prompt
        if self.system_prompt:
            # Add system prompt as the first message
            self.history.append({"role": "system", "content": self.system_prompt})

    def ask(self, user_message: str) -> str:
        # Add user message to history
        self.history.append({"role": "user", "content": user_message})

        # Send the conversation history to Ollama
        response: ChatResponse = chat(model=self.model, messages=self.history)

        # Extract assistant's reply
        assistant_reply = response["message"]["content"]

        # Add assistant reply to history
        self.history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def reset(self):
        """Clear the conversation history, keeping the system prompt if set."""
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})


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
