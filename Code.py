from game import Game
from rich.console import Console

console = Console()

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        console.print("\n[red]Game terminated.[/red]")
