# ChessboardFormatMicroservice

### Disclaimers:
- This microservice, but especially the install.sh script has only been tested in a Linux environment. Compatibility with other operating systems is not guaranteed.
- Only PGN is supported as an input notation at the moment
- The microservice is not yet able to detect incorrectly formatted inputs

## Setup

### **Prerequisites**
- Git
- Python3
- Pip
- Recommended: python3-venv


### **Installation**
Bash:
```bash
./install.sh
```


### **Running**
Bash:
```bash
# Create a new terminal and navigate to it
python3 src/formatServer.py
# Go back to the original terminal for example
python3 src/formatClient.py
```

### **Requesting data from the microservice**

```python
  # example_client.py

  # Connect to the gRPC server
  channel = grpc.insecure_channel("localhost:50051")

  # Create stub
  stub = jsonFormat_pb2_grpc.jsonFormatServiceStub(channel)
  pgn_data = """
[Event "Test Game"]
[Site "Local"]
[Date "2026.05.18"]
[Round "1"]
[White "WhitePlayer"]
[Black "BlackPlayer"]
[Result "*"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 *
"""
  request = jsonFormat_pb2.request(
    notationType="PGN",
    boardData=pgn_data,
    isCLI="NoCLI"
  )

  response = stub.PGNtoBoard(request)
```
### Request Fields
| Field | Type | Description |
|---|---|---|
| `notationType` | string | Represents the form of notation. Currently only PGN is supported |
| `boardData`    | string | String representing the board in the specified notation|
| `isCLI`        | string | `CLI` if the caller wants an array of strings. `NoCLI` for JSON return |

### **Receiving data from the microservice**
```python
  # Continuing from the request
  response = stub.PGNtoBoard(request)

  print("===== Server Response =====")
  print(f"Error Message  : {response.errorMsg}")
  print(f"Chessboard Response: \n{response.chessboard}")
```
### Response fields

| Field | Type | Description |
|---|---|---|
| `errorMsg` | string | Empty if no error is encountered, otherwise provides a descriptive error message |
| `chessboard` | json or string[] | If the value for isCLI is "CLI", returns a string[], otherwise JSON representing the board state |
