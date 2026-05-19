# formatCLIent.py

import grpc
import jsonFormat_pb2
import jsonFormat_pb2_grpc


def run():
  # Connect to the gRPC server
  channel = grpc.insecure_channel("localhost:50051")

  # Create stub
  stub = jsonFormat_pb2_grpc.jsonFormatServiceStub(channel)

  # Example PGN input
  pgn_data = """
[Event "rated bullet game"]
[Site "https://lichess.org/74k3moQv"]
[Date "2026.01.16"]
[Round "-"]
[White "fish206204"]
[Black "msb2"]
[Result "1-0"]
[GameId "74k3moQv"]
[UTCDate "2026.01.16"]
[UTCTime "13:27:11"]
[WhiteElo "2848"]
[BlackElo "3204"]
[WhiteRatingDiff "+10"]
[BlackRatingDiff "-12"]
[WhiteTitle "CM"]
[BlackTitle "GM"]
[Variant "Standard"]
[TimeControl "60+0"]
[ECO "A07"]
[Opening "King's Indian Attack, with e6"]
[Termination "Normal"]

1. Nf3 d5 2. g3 e6 3. Bg2 Nf6 4. O-O Bd6 5. c4 O-O 6. cxd5 exd5 7. d4 Nc6 8. Nc3 h6 9. Bf4 Bxf4 10. gxf4 Ne7 11. e3 c5 12. Ne5 cxd4 13. exd4 Be6 14. Qf3 Nf5 15. Rad1 Nh4 16. Qg3 Nxg2 17. Kxg2 Nh5 18. Qf3 Qh4 19. Ne2 f6 20. Ng6 Qg4+ 21. Qxg4 Bxg4 22. f3 Rfe8 23. fxg4 Rxe2+ 24. Rf2 Nxf4+ 25. Nxf4 Re4 26. Nxd5 Rxg4+ 27. Kf3 Rh4 28. Nc3 Kf7 29. d5 Rd8 30. d6 Rh5 31. Re2 Re5 32. Rxe5 fxe5 33. Ke4 Ke6 34. Nb5 a6 35. Nc7+ Kd7 36. Nd5 Rf8 37. Nb6+ Kd8 38. Rc1 Rf4+ 39. Kd5 Rd4+ 40. Ke6 Rxd6+ 41. Kxd6 1-0
"""

  # Create request
  request = jsonFormat_pb2.request(
    notationType="PGN",
    boardData=pgn_data,
    isCLI="NoCLI"
  )
  
  print("\nAttempting normal call of PGN notation with NoCLI")
  try:
    response = stub.PGNtoBoard(request)

    print("===== Server Response =====")
    print(f"Error Message  : {response.errorMsg}")
    print(f"Chessboard JSON: \n{response.chessboard}")

  except grpc.RpcError as e:
    print("gRPC Error")
    print(f"Code    : {e.code()}")
    print(f"Details : {e.details()}")

  print("\nAttempting to call with isCLI set to true.")
  request.isCLI="CLI"
  try:
    response = stub.PGNtoBoard(request)

    print("===== Server Response =====")
    print(f"Error Message  : {response.errorMsg}")
    print(f"Chessboard     : \n{response.chessboard}")

  except grpc.RpcError as e:
    print("gRPC Error")
    print(f"Code    : {e.code()}")
    print(f"Details : {e.details()}")
      
  print("\nAttempting to convert EPD format")
  request.notationType="EPD"
  try:
    response = stub.PGNtoBoard(request)

    print("===== Server Response =====")
    print(f"Error Message  : {response.errorMsg}")
    print(f"Chessboard     : \n{response.chessboard}")

  except grpc.RpcError as e:
    print("gRPC Error")
    print(f"Code    : {e.code()}")
    print(f"Details : {e.details()}")


if __name__ == "__main__":
  run()