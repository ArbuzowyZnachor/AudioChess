from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import random
from time import sleep
import sys
import logging

logging.basicConfig(filename='server_errors.log', level=logging.ERROR)

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.gameNumber = 0
        self.gameColour = 0
        Channel.__init__(self, *args, **kwargs)

    # Set game info
    def set_game(self, gameNumber, gameColour):
        self.gameNumber = gameNumber
        self.gameColour = gameColour

#======================== Server communication functions =====================

    # Send move to server
    def Network_move(self, data):
        try:
            self._server.send_move({
                "move":data["move"], 
                "game":self.gameNumber,
                "colour":int( not self.gameColour)})
        except Exception:
            logging.exception(
                "Unable to send move from client to server.\
                     Client: {0}".format(self))

    # Send resign to server
    def Network_resign(self, data):
        try:
            self._server.send_resign({
                "game":self.gameNumber, 
                "colour":int( not self.gameColour)})
        except Exception:
            logging.exception("Unable to send move from \
                client to server. Client: {0}".format(self))

    # Send disconnect to server
    def Network_disconnect(self, data):
        try:
            self._server.remove_client(self)
        except Exception:
            logging.exception("Unable to send dissconnect from \
                client to server. Client: {0}".format(self))

class ChessServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        self.players = []
        self.gameCounter = 0
        Server.__init__(self, *args, **kwargs)

        print("Server launched")
        print("Ctrl-C to exit")
        self.q = []
    
#======================== Clients managing functions =====================

    # Try pair client after connection to server
    def Connected(self, channel, addr):
        self.q.append(channel)
        if len(self.q)>1:
            self._pair_players()

    # Pair clients and set their games
    def _pair_players(self):
        try:
            self.piecesColour = random.getrandbits(1)
            self.players.append([
                self.q[self.piecesColour], 
                self.q[int(not self.piecesColour)]])
        except Exception as ex:
            logging.exception("_pair_players function error. \
                Allocating colors failed")
            self.send_disconnection(self.q[self.piecesColour], ex)
            self.send_disconnection(self.q[int(not self.piecesColour)], ex)
            del self.q[0:2]
        else:
            try:
                self.players[-1][0].Send({
                    "action": "setGame", 
                    "gameNumber": self.gameCounter, 
                    "colour": "white"})
                self.players[-1][1].Send({
                    "action": "setGame", 
                    "gameNumber": self.gameCounter, 
                    "colour": "black"})
                self.players[-1][0].set_game(self.gameCounter, 0)
                self.players[-1][1].set_game(self.gameCounter, 1)
                self.gameCounter += 1
            except Exception as ex:
                logging.exception("_pair_players function error.\
                     Pairing players failed")
                self.send_disconnection(self.players[-1][0], ex)
                self.send_disconnection(self.players[-1][1], ex)
                del self.players[-1]
            else:
                del self.q[0:2]

    # Remove client from queue
    def remove_client(self, channel):
        try:
            self.q.remove(channel)
        except Exception:
            logging.exception("Unable to remove channel from server list")
        else:
            print("channel removed")

#======================== Client communication functions =====================

    # Send move to client
    def send_move(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({
                "action":"moveFromServer", 
                "move":data["move"]})
        except Exception:
            logging.exception("Unable to send move from server to client")

    # Send resign info to client
    def send_resign(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({
                "action":"resignFromServer"})
        except Exception:
            logging.exception("Unable to send resign from server to client")

    # Send disconnecton info to client
    def send_disconnection(self, channel, error):
        try:
            channel.Send({"action":"disconnectedFromServer", "error": error})
        except Exception:
            logging.exception("Unable to send move from server to client")

    # Send data to clients while server is launched
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:5554")
    else:
        host, port = sys.argv[1].split(":")
        s = ChessServer(localaddr=(host, int(port)))
        s.Launch()        