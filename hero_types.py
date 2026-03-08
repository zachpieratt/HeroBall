class HeroType:

    def __init__(self, name, color, ability, description):
        self.name = name
        self.color = color
        self.ability = ability
        self.description = description


HERO_TYPES = [
    HeroType("DOUBLER",(100,220,140),"double",
    "Hero doubles damage on every hit."),

    HeroType("RAMPAGE",(255,180,80),"triple",
    "Hero triples damage on every hit."),

    HeroType("SPLITTER",(120,200,255),"split",
    "Hero splits into 2 balls on each hit. These also split but die after 2 hits."),

    HeroType("GAMBLER",(255,100,200),"gambler",
    "Hero has a 70% chance to multiply damage by 7 on hit and 30% chance to reset to 1.")
]