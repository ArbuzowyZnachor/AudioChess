from PodSixNet.Connection import connection, ConnectionListener
from time import sleep
import sys

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))

    def Loop(self):
        connection.Pump()
        self.Pump()


    # Sends move to server
    def send_move(self, move):
        connection.Send({"action":"move", "move":move})

    def send_draw(self):
        connection.Send({"action":"draw"})

    def send_drawOffer(self):
        connection.Send({"action":"drawOffer"})

    def send_drawAccept(self):
        connection.Send({"action":"drawAccept"})

    def send_resign(self):
        connection.Send({"action":"resign"}) 


    def Network_moveFromServer(self,data):
        print("Ruch przeciwnika: ", data["move"])

    def Network_drawFromServer(self):
        print("Partia zakończona remisem")

    def Network_drawOfferFromServer(self):
        print("Przeciwnik proponuje remis")

    def Network_drawAcceptFromServer(self)
        print("Przeciwnik zaakceptował remis")

    def Network_resignFromServer(self):
        print("Przeciwnik zrezygnował")


    def Network_setGame(self, data):
        print("Numer twojej gry: {0} Twój kolor: {1}".format(data["gameNumber"], data["colour"]))

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        c = Client(host, int(port))
        while 1:
            c.Loop()
            sleep(0.001)