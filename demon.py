import random
import time
from rich.console import Console

console = Console()

class Demon:
    def __init__(self, grace, initial_chance, final_chance):
        self.active = False
        self.location = None
        self.turns_passed = 0
        self.warned = False
        self.grace = grace
        self.initial_chance = initial_chance
        self.final_chance = final_chance

    def update(self, turns_left, world):
        self.turns_passed += 1
        if self.turns_passed >= self.grace:
            self.active = True
            
        if turns_left <= 5 and not self.warned:
            self.warned = True
            console.print("[red bold]You feel a chill crawl up your spine...[/red bold]")
            console.print("[red italic]A voice whispers: 'I am coming for you... you cannot escape.'[/red italic]")
            time.sleep(1.5)
            
        if self.active:
            demon_chance = self.final_chance if turns_left <= 5 else self.initial_chance
            if random.random() < demon_chance:
                self.location = random.choice([loc for loc in world.locations if loc != 'bay'])
            else:
                self.location = None # Demon moves into shadows

    def to_dict(self):
        return {
            'active': self.active,
            'location': self.location,
            'turns_passed': self.turns_passed,
            'warned': self.warned,
            'grace': self.grace,
            'initial_chance': self.initial_chance,
            'final_chance': self.final_chance
        }

    @classmethod
    def from_dict(cls, data):
        d = cls(data['grace'], data['initial_chance'], data['final_chance'])
        d.active = data['active']
        d.location = data['location']
        d.turns_passed = data['turns_passed']
        d.warned = data['warned']
        return d

