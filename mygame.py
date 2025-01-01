import _pygame

def main():
    game = _pygame.Game() 
    game.FirstCreation()
    game.cyclegame() 
    game.cleanup()

if __name__ == "__main__":
    main()
