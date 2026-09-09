import random

class World:
    def __init__(self):
        self.locations = ['cave', 'beach', 'forest', 'mountain', 'river', 'ruins', 'bay']
        self.adjacency = {
            'bay': ['beach', 'forest'],
            'beach': ['bay', 'cave', 'river'],
            'forest': ['bay', 'mountain', 'ruins'],
            'cave': ['beach', 'mountain'],
            'mountain': ['forest', 'cave', 'river'],
            'river': ['beach', 'mountain', 'ruins'],
            'ruins': ['forest', 'river']
        }
        self.descriptions = {
            'bay': "The sandy bay where you crashed. It feels relatively safe here.",
            'beach': "A long stretch of grey sand. The waves crash violently against the shore.",
            'forest': "Twisted, dead trees loom over you. Shadows dance in your peripheral vision.",
            'cave': "A dark, damp cavern. The air is thick with the smell of decay.",
            'mountain': "Jagged rocks and strong winds. It's easy to lose your footing here.",
            'river': "A rushing river of dark water. Something moves beneath the surface.",
            'ruins': "Crumbling stone pillars of an ancient structure. A sense of dread hangs heavy."
        }

    def get_adjacent(self, loc):
        return self.adjacency.get(loc, [])

    def random_event(self, player):
        roll = random.random()
        if roll < 0.2:
            player.turns -= 1
            return "[red]⚠️ You triggered a hidden trap! You twisted your ankle and lost 1 hour.[/red]"
        elif roll < 0.35:
            player.turns += 1
            return "[green]✨ You found a moment of peace and rested. You gained 1 hour![/green]"
        elif roll < 0.6:
            return "[dim]You find old bones scattered on the ground... you are not the first one here.[/dim]"
        return "[dim]You searched the area... yet found nothing of use.[/dim]"

