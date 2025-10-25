import os
from typing import Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import websockets
from storyteller.conversation import OllamaConversation

load_dotenv()

ollama_model = os.environ["OLLAMA_MODEL"]


@dataclass
class StoryClient:
    id: str
    conversation: OllamaConversation
    socket: websockets.ServerConnection

    def __init__(self, id: str, socket: websockets.ServerConnection):
        self.id = id
        self.socket = socket
        self.conversation = OllamaConversation(model=ollama_model)


class StoryClients:

    def __init__(self):
        self._clients: Dict[str, StoryClient] = {}

    def add_client(self, client_id: str, client_object: StoryClient) -> None:
        """Add a client with their associated object"""
        self._clients[client_id] = client_object

    def get_client(self, client_id: str) -> Optional[StoryClient]:
        """Retrieve a client object by UUID - O(1) lookup"""
        return self._clients.get(client_id)

    def remove_client(self, client_id: str) -> bool:
        """Remove a client and return True if successful"""
        if client_id in self._clients:
            del self._clients[client_id]
            return True
        return False

    def client_exists(self, client_id: str) -> bool:
        """Check if a client exists"""
        return client_id in self._clients

    def get_all_clients(self) -> Dict[str, StoryClient]:
        """Return all clients"""
        return self._clients.copy()

    def __len__(self) -> int:
        return len(self._clients)

    def __contains__(self, client_id: str) -> bool:
        return client_id in self._clients
