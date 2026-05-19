# import time

import io
import grpc
import json
import time
# import logging
import chess
import chess.pgn
from concurrent import futures

import jsonFormat_pb2
import jsonFormat_pb2_grpc

def pgn_to_fen(pgn_text):
  # Use StringIO for string parsing and read game
  game = chess.pgn.read_game(io.StringIO(pgn_text))
  if not game: return "No valid game found."
  
  board = game.board()
  for move in game.mainline_moves():
    board.push(move)
  return board.fen()
  # Returns a string in FEN
  
def fen_to_board_array(fen):
  # FEN consists of 6 parts; the first part is the board layout
  board_part = fen.split(' ')[0]
  
  # Ranks are separated by '/'
  ranks = board_part.split('/')
  
  board_array = []
  for rank in ranks:
    row = ""
    for char in rank:
      if char.isdigit():
        # Replace digit with that many empty squares (dots)
        row += "." * int(char)
      else:
        row += char
    board_array.append(row)
      
  return board_array

def board_array_to_json(board_array):
  temp_data = {"board": board_array}
  return json.dumps(temp_data)

class jsonFormatService(jsonFormat_pb2_grpc.jsonFormatServiceServicer):
  def PGNtoBoard(self, request, context):
    if not request.notationType or not request.boardData or not request.isCLI:
      return jsonFormat_pb2.response(errorMsg="All fields required", chessboard="")
    
    if(request.notationType=="PGN"):
      fen = pgn_to_fen(request.boardData)
      board = fen_to_board_array(fen)
      if(request.isCLI=="CLI"):
        return jsonFormat_pb2.response(errorMsg="",chessboard="\n".join(board))
      else:
        return jsonFormat_pb2.response(errorMsg="",chessboard=board_array_to_json(board))
    else:
      return jsonFormat_pb2.response(errorMsg=f"Format {request.notationType} not yet supported", chessboard="")
    
    
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  jsonFormat_pb2_grpc.add_jsonFormatServiceServicer_to_server(jsonFormatService(), server)
  server.add_insecure_port("[::]:50051")
  server.start()
  print("gRPC server running on port 50051")
  server.wait_for_termination()
  
if __name__ == "__main__":
  serve()