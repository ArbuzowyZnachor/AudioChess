from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import random
from time import sleep
import sys
import queue

DEBUG = 0

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.gameNumber = 0
        self.gameColour = 0
        Channel.__init__(self, *args, **kwargs)

    def set_game(self, gameNumber, gameColour):
        self.gameNumber = gameNumber
        self.gameColour = gameColour

    def Network_move(self, data):
        try:
            self._server.send_move({"move":data["move"], "game":self.gameNumber, "colour":int( not self.gameColour)})
        except Exception as ex:
            print("Unable to send move from client to server. Error: {0}".format(ex))

    def Network_draw(self):
        try:
            self._server.send_draw()
        except Exception as ex:
            print("Unable to send draw from client to server. Error: {0}".format(ex))

    def Network_drawOffer(self):
        try:
            self._server.send_drawOffer()
        except Exception as ex:
            print("Unable to send draw offer from client to server. Error: {0}".format(ex))

     def Network_drawAccept(self):
        try:
            self._server.send_drawAccept()
        except Exception as ex:
            print("Unable to send draw accept from client to server. Error: {0}".format(ex))
    
    # def Close(self): #TODO
    #     self._server.del_player(self)

class ChessServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        self.players = []
        self.gameCounter = 0
        Server.__init__(self, *args, **kwargs)

        print("Server launched")
        print("Ctrl-C to exit")
        self.q = []

    def _try_make_pair(self):
        if len(self.q)>1:
            try:
                self.piecesColour = random.getrandbits(1)
                self.players.append([self.q[self.piecesColour], self.q[int(not self.piecesColour)]])
                print(self.players)
                del self.q[0:2]

            except Exception as e:
                print("_try_make_pair function error! Reason:{0}".format(e))
                pass

            else:
                try:
                    if(DEBUG):
                        print("Stworzono parę {0} oraz {1}".format(self.players[-1][0].addr, self.players[-1][1].addr))
                        self.players[-1][0].Send({"action": "setGame", "gameNumber": self.gameCounter, "colour": "białe"})
                        self.players[-1][1].Send({"action": "setGame", "gameNumber": self.gameCounter, "colour": "czarne"})

                    self.players[-1][0].set_game(self.gameCounter, 0)
                    self.players[-1][1].set_game(self.gameCounter, 1)
                    self.gameCounter += 1

                except Exception as e:
                    print("_try_make_pair printing function error! Reason:{0}".format(e))
                    pass    

    # def del_player(self, player): #TODO
    #     print("Deleting Player" + str(player.addr))
    #     del self.players[player]

    def send_move(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({"action":"moveFromServer", "move":data["move"]})
        except Exception as ex:
            print("Unable to send move from server to client. Error: ", ex)
    
    def send_draw(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({"action":"drawFromServer"})
        except Exception as ex:
            print("Unable to send draw from server to client. Error: ", ex)

    def send_drawOffer(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({"action":"drawOfferFromServer"})
        except Exception as ex:
            print("Unable to send draw from server to client. Error: ", ex)

    def send_resign(self, data):
        try:
            self.players[data["game"]][data["colour"]].Send({"action":"resignFromServer"})
        except Exception as ex:
            print("Unable to send resign from server to client. Error: ", ex)


    def Connected(self, channel, addr):
        print ('new connection:', channel, addr)
        self.q.append(channel)
        self._try_make_pair()

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        s = ChessServer(localaddr=(host, int(port)))
        s.Launch()
        