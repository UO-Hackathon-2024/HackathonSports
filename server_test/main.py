URI = "ws://10.108.22.125:3000"  # Replace with your server's IP and port

import asyncio
import websockets

# Function to send messages from a player (either player 1 or player 2)
async def send_player_swing(player_id: str, delay: float, websocket):
    await asyncio.sleep(delay)  # Delay before sending the next swing
    # Send the swing message
    message = f"player{player_id}_swing"
    await websocket.send(message)
    print(f"Sent: {message}")
    
    # Wait for server acknowledgment (optional)
   

# Main function to connect both players
async def main():

    socket = await websockets.connect(URI)  # Connection for player 1 async for message in websocket: 
    
    await send_player_swing('2', 6, socket)
    


# Run the WebSocket client for both players
asyncio.run(main())

