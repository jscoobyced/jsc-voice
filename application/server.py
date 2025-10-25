import asyncio
import os
import websockets
import signal
import ssl
from dotenv import load_dotenv
from storyteller.story_client import StoryClient, StoryClients
from storyteller.processor import StoryProcessor
import util.logger as log

load_dotenv()

logger = log.Logger()
clients = StoryClients()
server_url = os.environ["SERVER_URL"]
server_port = int(os.environ["SERVER_PORT"])

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="origin.pem", keyfile="origin.key")
story_processor = StoryProcessor()


async def audio_handler(websocket):
    logger.info("Client connected")
    async for message in websocket:
        socket: websockets.ServerConnection = websocket
        client_id = socket.id
        logger.info(f"Received audio data from {client_id}")
        if not clients.client_exists(client_id):
            client = StoryClient(id=client_id, socket=websocket)
            clients.add_client(client_id=client_id, client_object=client)
        client = clients.get_client(client_id)
        await story_processor.process(message=message, client=client)


async def disconnect_all_clients():
    nb_clients = len(clients)
    logger.info(f"Disconnecting {nb_clients} connected clients...")
    if nb_clients == 0:
        return
    # Iterate over a copy of the set to avoid issues if clients disconnect during iteration
    connected_clients = clients.get_all_clients()
    for client in connected_clients.values():
        try:
            await client.socket.close(code=1001, reason="Server shutting down")
            logger.info(f"Client {client.socket.remote_address} disconnected.")
        except Exception as e:
            logger.info(
                f"Error disconnecting client {client.socket.remote_address}: {e}"
            )


async def main():
    async def signal_handler():
        logger.info("SIGINT (Ctrl+C) received. Performing cleanup...")
        cleanup_task = asyncio.create_task(disconnect_all_clients())
        try:
            await asyncio.wait_for(cleanup_task, timeout=5)
        except asyncio.TimeoutError:
            logger.info("Cleanup timed out.")
        finally:
            start_server.close()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(
        signal.SIGINT, lambda: asyncio.create_task(signal_handler())
    )

    async with websockets.serve(
        audio_handler, server_url, server_port, ssl=ssl_context
    ) as start_server:
        logger.info(f"WebSocket server started on ws://{server_url}:{server_port}")
        await start_server.wait_closed()


if __name__ == "__main__":
    tmp_folder = os.environ["TMP_FOLDER"]
    # Empty tmp folder
    if os.path.exists(tmp_folder):
        for f in os.listdir(tmp_folder):
            os.remove(os.path.join(tmp_folder, f))
    # If tmp folder doesn't exist, create it
    else:
        os.makedirs(tmp_folder)

    try:
        asyncio.run(main())
    except Exception as e:
        logger.info(f"Error: {e}")
