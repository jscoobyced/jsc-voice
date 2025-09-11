import requests
import json

url = "http://localhost:11434/api/chat"


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_access_token",
}


class Ollama:

    def ask(self, question: str):
        # Define the data payload with system and user prompts
        data = {
            "model": "gemma3:12b",
            "messages": [
                {
                    "role": "system",
                    "content": "Answer this question in 100 words maximum",
                    "role": "user",
                    "content": question,
                }
            ],
            "format": "json",
            "stream": False,
        }

        # Send a POST request to the Ollama server
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()
            message = response_data.get(
                "message",
                {
                    "content": '{ "No answer returned": { "type": "text", "category": "Information", }}'
                },
            )
            answer_data = message.get(
                "content",
                '{ "No answer returned": { "type": "text", "category": "Information", }}',
            )
            answer_json = json.loads(answer_data)
            answer = answer_json["answer"]
            return answer
