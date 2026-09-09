import time
import os
import random
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

from player import Player
from world import World
from demon import Demon

console = Console()

class Game:
    def __init__(self):
        self.player = None
        self.world = World()
        self.demon = None
        self.settings = None
        self.save_file = "savegame.json"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def speak(self, text, delay=0.03, pause=1.0, style="white"):
        # We simulate speaking effect line by line
        console.print(f"[{style}]{text}[/{style}]")
        time.sleep(pause)

    def draw_hud(self):
        # Create a nice HUD panel
        items_found = [item.title() for item, found in self.player.items.items() if found]
        items_text = ", ".join(items_found) if items_found else "None"
        
        status = f"[bold cyan]Hours Remaining:[/bold cyan] {self.player.turns}\n"
        status += f"[bold magenta]Current Location:[/bold magenta] {self.player.current_location.title()}\n"
        status += f"[bold yellow]Items Collected:[/bold yellow] {items_text}\n"
        
        if self.player.brother_found:
            status += "[bold green]Brother Status:[/bold green] Found!\n"
            
        panel = Panel(status, title="[bold white]Player Status[/bold white]", border_style="blue")
        console.print(panel)

    def check_demon_footprints(self):
        if self.demon.active and self.demon.location:
            adj = self.world.get_adjacent(self.player.current_location)
            if self.demon.location in adj:
                console.print("[red bold]⚠️ You hear heavy footsteps echoing from a nearby area... The demon is close![/red bold]")
                time.sleep(1.5)

    def show_menu(self):
        self.clear_screen()
        print("\n")
        title = """[red bold]
        ╔════════════════════════════════════════════╗
        ║                                            ║
        ║           STRANDED: HELL’S MAW             ║
        ║                                            ║
        ╚════════════════════════════════════════════╝
        [/red bold]"""
        console.print(Align.center(title))
        
        menu_text = """
        [cyan]1.[/cyan] START NEW GAME
        [cyan]2.[/cyan] LOAD GAME
        [cyan]3.[/cyan] HELP & RULES
        [cyan]4.[/cyan] EXIT
        """
        console.print(menu_text)

    def show_rules(self):
        self.clear_screen()
        rules = """
        [bold white]🕯️ GAME RULES — STRANDED: HELL'S MAW 🕯️[/bold white]
        You are stranded on a cursed island. Escape before time runs out... or before something finds you.

        [bold cyan]🎯 Objective:[/bold cyan]
        - Collect 5 essential items to build your escape raft.
        - Find your lost brother Edwin.
        - Escape the island before your time (turns) runs out.
        - Avoid the demon that hunts you after a grace period.

        [bold yellow]🕐 Time Limit:[/bold yellow]
        - Each action/location visit = 1 hour (turn).
        - If turns hit 0, you die.

        [bold green]🧭 Required Items to Escape:[/bold green]
        - Map, Compass, Raft, Oars, Torch

        [bold magenta]👤 Brother Rescue Rule:[/bold magenta]
        - You must find the Map and Torch first.
        - Only then will your brother be revealed.
        - He must be rescued to escape.

        [bold red]😈 The Demon:[/bold red]
        - Safe for a grace period.
        - The demon begins hunting locations randomly.
        - If you choose the same location as the demon: instant death.
        - Listen for footprints!

        [bold white]📜 Victory Conditions:[/bold white]
        - All required items found ✅
        - Your brother is rescued ✅
        - You escape before time runs out ✅
        - You avoid the demon ✅
        """
        console.print(Panel(rules, title="[bold]Rules[/bold]", border_style="cyan"))
        Prompt.ask("\n[bold]Press Enter to return to the main menu[/bold]")

    def start_new_game(self):
        self.clear_screen()
        self.speak('...', delay=0.2, pause=1)
        self.speak('Ah...Another soul dares to awaken me')
        self.speak('Tell me how I should treat you mortal...')
        
        diff = Prompt.ask("Choose difficulty", choices=["1", "2", "3"], default="1")
        if diff == '1': # Easy
            self.settings = {'turns': 24, 'grace': 5, 'initial': 0.1, 'final': 0.3, 'level': 'Easy'}
        elif diff == '2': # Novice
            self.settings = {'turns': 18, 'grace': 3, 'initial': 0.2, 'final': 0.4, 'level': 'Novice'}
        else: # Anarchist
            self.settings = {'turns': 12, 'grace': 0, 'initial': 0.3, 'final': 0.5, 'level': 'Anarchist'}
            
        self.speak('So, tell me..')
        self.speak('Who are you?')
        self.speak('Are you [bold cyan]Jonathan[/bold cyan], the brave and courageous (+3 Hours Stamina)?')
        self.speak('Or are you [bold magenta]Daniella[/bold magenta], the cunning yet alluring damsel (Higher chance to find items)?')
        
        char_choice = Prompt.ask("Choose who you are", choices=["1", "2"], default="1")
        
        self.player = Player(char_choice, self.settings['turns'])
        self.demon = Demon(self.settings['grace'], self.settings['initial'], self.settings['final'])
        
        if char_choice == '1':
            self.speak('Ah, Jonathan.')
            self.speak("I hope your pride won't cost your life.")
        else:
            self.speak('Daniella.')
            self.speak("I hope your wits won't be the death of you.")
            
        self.speak('\nYou have been stranded in my domain called "Hells maw" after your plane crashed...')
        self.speak('You wake up in the bay area of the island.')
        self.speak(f'You have {self.player.turns} hours before dawn breaks.', style="yellow bold")
        self.speak('Your goal is to find your brother Edwin and escape this wretched place.')
        time.sleep(1)
        self.game_loop()

    def save_game(self):
        state = {
            'player': self.player.to_dict(),
            'demon': self.demon.to_dict(),
            'settings': self.settings
        }
        try:
            with open(self.save_file, 'w') as f:
                json.dump(state, f)
            console.print("[bold green]Your soul is tethered to this moment... (Progress Saved)[/bold green]")
            time.sleep(1)
        except Exception as e:
            console.print(f"[bold red]Failed to save game: {e}[/bold red]")
            time.sleep(1)

    def load_game(self):
        if not os.path.exists(self.save_file):
            console.print("[bold red]No saved memory remains in this realm...[/bold red]")
            time.sleep(2)
            return False
            
        try:
            with open(self.save_file, 'r') as f:
                state = json.load(f)
            self.player = Player.from_dict(state['player'])
            self.demon = Demon.from_dict(state['demon'])
            self.settings = state['settings']
            console.print("[bold green]Memories restored. Returning to the nightmare...[/bold green]")
            time.sleep(2)
            self.game_loop()
            return True
        except Exception as e:
            console.print(f"[bold red]Save file corrupted... ({e})[/bold red]")
            time.sleep(2)
            return False

    def game_loop(self):
        while self.player.turns > 0:
            self.clear_screen()
            self.draw_hud()
            
            # Print location description
            desc = self.world.descriptions.get(self.player.current_location, "")
            console.print(f"[italic dim]{desc}[/italic dim]\n")
            
            self.check_demon_footprints()

            console.print("[bold]Where do you wish to go to search?[/bold]")
            for loc in self.world.locations:
                if loc != 'bay':
                    console.print(f"- [cyan]{loc.title()}[/cyan]")
            
            if self.player.has_all_items() and self.player.brother_found and self.player.current_location != 'bay':
                console.print("- [green]BAY[/green] (Return to escape)")
            if self.player.current_location == 'bay' and self.player.has_all_items() and self.player.brother_found:
                console.print("- [green bold]SET SAIL[/green bold] (Escape!)")
                
            console.print("- [yellow]SAVE[/yellow] (Save your progress and exit to menu)")
            
            choice = Prompt.ask("Enter choice").strip().lower()

            if choice == "save":
                self.save_game()
                return # Exit to main menu

            if choice == "bay":
                if self.player.has_all_items() and self.player.brother_found:
                    self.speak("You head back to the bay with everything you need...", style="green")
                    self.player.current_location = "bay"
                    self.player.turns -= 1
                    continue
                else:
                    self.speak("You cannot return to the bay yet. Something is still missing.", style="red")
                    time.sleep(1.5)
                    continue

            if choice == "set sail":
                if self.player.current_location == "bay" and self.player.has_all_items() and self.player.brother_found:
                    self.clear_screen()
                    self.speak("You and your brother start assembling the raft...", style="green bold")
                    self.speak("You build a raft with your brother and prepare to leave...")
                    self.speak("The night is dark, but you are ready.")
                    self.speak("You set sail...")
                    self.speak("Congratulations! You survived. For now...", style="bold green")
                    self.speak("Next time you won't get away...", style="red bold")
                    self.speak("THE END", style="bold white on red", pause=3)
                    # Delete save file if won
                    if os.path.exists(self.save_file):
                        os.remove(self.save_file)
                    return
                else:
                    self.speak("You can't set sail now. Either you're not at the bay or you're missing something.", style="red")
                    time.sleep(1.5)
                    continue

            if choice not in self.world.locations:
                self.speak('That place... does not exist here.', style="red")
                time.sleep(1.5)
                continue

            # Move and deduct turn
            self.player.turns -= 1
            self.player.current_location = choice
            
            # Demon logic
            self.demon.update(self.player.turns, self.world)
            if self.demon.active and self.demon.location == choice:
                self.clear_screen()
                self.speak("The shadows shift... I FOUND YOU!!", style="red bold", pause=1)
                self.speak("*Your screams are lost in the void*", style="red italic")
                self.speak("GAME OVER.", style="bold white on red", pause=3)
                # Delete save file if lost
                if os.path.exists(self.save_file):
                    os.remove(self.save_file)
                return

            # Searching logic
            found_item = False
            missing_items = [item for item, found in self.player.items.items() if not found]
            
            self.speak(f"Searching the {choice}...")
            time.sleep(0.5)

            if missing_items:
                # Random chance to find one of the missing items
                for item in missing_items:
                    if random.random() < self.player.base_find_chance:
                        self.player.items[item] = True
                        console.print(f"[bold green]✨ You found the {item.title()}! Well done...[/bold green]")
                        found_item = True
                        time.sleep(1.5)
                        break

            if not found_item:
                # Random event instead of finding nothing
                event_text = self.world.random_event(self.player)
                console.print(event_text)
                time.sleep(1.5)
                
            # Hints
            missing_items = [item for item, found in self.player.items.items() if not found]
            if missing_items and self.player.turns in [15, 10, 5]:
                hint_item = random.choice(missing_items)
                console.print(f"[yellow italic]A whisper in the dark: 'Seek the {hint_item}...'[/yellow italic]")
                time.sleep(1.5)

            # Brother logic
            if self.player.items['map'] and self.player.items['torch']:
                self.player.brother_revealed = True
                
            if self.player.brother_revealed and not self.player.brother_found:
                self.speak('The mist fades.... A familiar figure appears at the shore...', style="cyan")
                self.speak('It is your brother Edwin! You rush to him.', style="bold green")
                self.player.brother_found = True
                time.sleep(2)

        # Out of turns
        if self.player.turns <= 0:
            self.clear_screen()
            self.speak("The final hour tolls...", style="red bold")
            self.speak("Time is up.", style="red")
            self.speak("You have failed.", style="red")
            self.speak("Goodbye Mortal.", style="red italic")
            self.speak("GAME OVER.", style="bold white on red", pause=3)
            if os.path.exists(self.save_file):
                os.remove(self.save_file)

    def run(self):
        while True:
            self.show_menu()
            choice = Prompt.ask("CHOOSE YOUR DESTINY", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                self.start_new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.show_rules()
            elif choice == "4":
                self.clear_screen()
                self.speak("Leaving so soon? Farewell...for now :)", style="magenta", delay=0.05)
                time.sleep(1)
                break

