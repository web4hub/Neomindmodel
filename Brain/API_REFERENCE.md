

# API Reference — Brain

## 🧠 Core Module

### class BrainCore
| Method | Description |
|--------|-------------|
| think(prompt: str) | Processes input and returns a cognitive response |
| remember(key: str, value: Any) | Stores a piece of data in memory |
| recall(key: str) -> Any | Retrieves stored information |
| train(data: dict) | Triggers internal retraining or adaptation |

## 🌐 API Layer (FastAPI)
| Route | Method | Description |
|-------|--------|-------------|
| /think | POST | Sends a prompt to BrainCore and receives a response |
| /remember | POST | Saves data to memory |
| /recall | GET | Retrieves stored data from memory |


⸻

