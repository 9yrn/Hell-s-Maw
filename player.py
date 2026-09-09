class Player:
    def __init__(self, character_type, turns):
        self.character_type = character_type
        self.turns = turns
        self.items = {'map': False, 'compass': False, 'raft': False, 'oars': False, 'torch': False}
        self.current_location = 'bay'
        self.brother_revealed = False
        self.brother_found = False
        
        # Meaningful Character Choices
        if self.character_type == '1': # Jonathan
            self.name = "Jonathan"
            self.turns += 3  # Bonus stamina
            self.base_find_chance = 0.3
        elif self.character_type == '2': # Daniella
            self.name = "Daniella"
            self.base_find_chance = 0.45 # Higher find chance
        else:
            self.name = "Unknown"
            self.base_find_chance = 0.3

    def has_all_items(self):
        return all(self.items.values())

    def to_dict(self):
        return {
            'character_type': self.character_type,
            'name': self.name,
            'turns': self.turns,
            'items': self.items,
            'current_location': self.current_location,
            'brother_revealed': self.brother_revealed,
            'brother_found': self.brother_found,
            'base_find_chance': self.base_find_chance
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data['character_type'], data['turns'])
        p.name = data['name']
        p.items = data['items']
        p.current_location = data['current_location']
        p.brother_revealed = data['brother_revealed']
        p.brother_found = data['brother_found']
        p.base_find_chance = data['base_find_chance']
        return p

