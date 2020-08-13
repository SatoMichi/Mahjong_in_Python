import multiprocessing
from GameManager import GamaManager
from game_client import startClient

def main():
    p1 = Player("Gundam Exia",25000)
    p2 = Player("Gundam Dynames",25000) 
    p3 = Player("Gundam Kyrios",25000)
    p4 = Player("Gundam Virtue",25000)
    game = GameManager([p1,p2,p3,p4])

    server = multiprocessing.Process(target=game.GameFSM)
    server.start()
    print("Game is succsessfully hosted.")
    startClient()
    server.join()

if __name__ == '__main__':
    main()