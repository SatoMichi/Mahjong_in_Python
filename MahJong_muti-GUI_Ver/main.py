import multiprocessing
from Player import Player
from GameManager import GameManager
from game_client import startClient
import logging

def main():
    host = input("Are you Game Host? 1:yes/0:no\n")
    if host == "1":
        p1 = Player("Gundam Exia",25000)
        p2 = Player("Gundam Dynames",25000) 
        p3 = Player("Gundam Kyrios",25000)
        p4 = Player("Gundam Virtue",25000)
        game = GameManager([p1,p2,p3,p4])
        print("GameManager created.\n")

        server = multiprocessing.Process(target=game.GameFSM)
        server.start()
        print("Game is successfully hosted.\n")
        startClient()
        #server.join()
        #server.close()
    else:
        startClient()

if __name__ == '__main__':
    main()