from game import LCSGame
from db_connect import connect_to_mongo

if __name__ == "__main__":
    game = LCSGame()
    connect_to_mongo()
    game.run()
