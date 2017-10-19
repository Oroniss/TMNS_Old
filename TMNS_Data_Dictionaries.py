##################################################################################################################
#                                       Material Dictionary.
##################################################################################################################

material_properties = {  # AC,  DR, HA, SR,     AR, CR, ER, FR, NR,     HP/V,   Adjective,  fgcolor, Traits
    "Cloth":        (0,     False,  0,  0,     -25, 5,  -15, -30, -30,  5,      "Cloth",    "Putrid Green",
                     {"Cloth", "Organic"}),
    "Glass":        (0,     False,  0,  0,      5,  15, -30, 20, -20,   5,      "Glass",    "Magic Purple",
                     {"Glass", "Inorganic"}),
    "Ice":          (10,    False,  2,  0,      10, 0,  20, -30, -20,   5,      "Icy",      "Ice",
                     {"Icy", "Inorganic", "Immune to Cold"}),
    "Iron":         (25,    False,  5,  0,      -5, 20, -10, 10, -20,   12,     "Iron",     "Steel Gray",
                     {"Metal", "Inorganic"}),
    "Magic":        (0,     False,  5,  25,     15, 15, 15, 15, 15,     15,     "Magic",    "Magic Purple",
                     {"Magic", "Inorganic"}),
    "Steel":        (30,    False,  8,  0,      0,  30, -5,  0, -20,    20,     "Steel",    "Steel Gray",
                     {"Metal", "Inorganic"}),
    "Stone":        (25,    False,  5,  0,     -5,  20, 30, 20, -20,    10,     "Stone",    "Stone Wall",
                     {"Stone", "Inorganic"}),
    "Wood":         (10,    False,  2,  0,     -10, 10, -10, -20, -30,  5,      "Wooden",   "Wood Brown",
                     {"Wood", "Organic"})
}

##################################################################################################################
#                                       Furnishing Dictionary.
##################################################################################################################

furnishing_details = {  # Sym,  BLos, BMov, SMov, Vol bgc,          fogcolor            material    Setup Function
    "Altar":            ("#",   False,    2,  2,  5,  None,         None,               None),
    "Barricade":        ("|",   False,    2,  2,  3,  None,         None,               None),
    "Cage":             ("#",   False,    2,  2,  3,  None,         None,               None),
    "Chest":            ("+",   False,    0,  0,  2,  None,         None,               None),
    "Closet":           ("#",   True,     3,  3,  5,  None,         None,               None),
    "Circle":           (".",   False,    0,  0,  1,  None,         None,               None),
    "Compartment":      ("+",   False,    0,  0,  1,  None,         None,               None),
    "Door":             ("-",   False,    0,  0,  4,  None,         None,               None),
    "Empty":            ("",    False,    0,  0,  1,  None,         None,               None),
    "Fountain":         ("&",   False,    0,  0,  3,  None,         None,               None),
    "Grease":           (" ",   False,    0,  2,  2,  "Steel Grey", None,               "Oil"),
    "Ice":              (" ",   False,    0,  2,  2,  "Ice",        "Ice Fog",          "Ice"),
    "Laboratory":       ("#",   False,    2,  2,  6,  None,         None,               None),
    "Pedestal":         ("*",   False,    2,  2,  2,  None,         None,               None),
    "Rubbish":          ("#",   False,    1,  1,  9,  None,         None,               None),
    "Stair":            ("//",  False,    0,  0,  5,  None,         None,               None),
    "Stair Up":         ("<",   False,    0,  0,  5,  None,         None,               None),
    "Stair Down":       (">",   False,    0,  0,  5,  None,         None,               None),
    "Statue":           ("#",   False,    2,  2,  4,  None,         None,               None),
    "Trap":             ("^",   False,    0,  5,  1,  None,         None,               None),
    "Web":              ("^",   False,    0,  1,  1,  None,         None,               "Webbing"),
    "Well":             ("&",   False,    0,  0,  4,  None,         None,               None)
}

furnishing_functions = {  # Tuples of (type, function_name)
    "Door":             (("Interaction", "Door Use"),),
}

##################################################################################################################
#                                       Actor Dictionaries.
##################################################################################################################

# Actor traits
actor_traits = {
    "Player":           ("Player",),
    # Aberrations
    "Darkmantle":       (),
    # Animals
    "Giant Ant":        (),
    "Giant Badger":     (),
    "Bat":              (),
    "Giant Bee":        (),
    "Fire Beetle":      ("Beetle", "Insect", "Animal"),
    "Horned Beetle":    (),
    "Centipede":        (),
    "Dog":              (),
    "Lizard":           (),
    "Pony":             (),
    "Rat":              (),
    "Dire Rat":         (),
    "Scorpion":         (),
    "Viper":            (),
    "Spider":           (),
    "Stirge":           (),
    "Weasel":           (),
    "Wolf":             (),
    # Constructs
    "Earthen Statue":   (),
    # Devils
    "Black Abishai":    (),
    "Lemure":           (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf":       (),
    # Elementals
    "Earth Vermin":     (),
    "Earth Elemental":  ("Elemental", "Earth", "Immune to Poison", "Immune to Crits", "Immune to Disease",
                         "Immune to Mental"),
    "Fire Vermin":      (),
    "Lightning Vermin": (),
    # Elves
    "High Elf":         (),
    "Wood Elf":         (),
    # Goblins
    "Goblin":           (),
    # Halflings
    "Halfling":         (),
    # Kobolds
    "Kobold":           (),
    "Kobold Acolyte":   ("Humanoid", "Reptile", "Kobold", "Divine"),
    "Kobold Apprentice": ("Humanoid", "Reptile", "Kobold", "Arcane"),
    "Kobold Scout":     (),
    # Lycanthropes
    "Wererat":          (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton":         (),
    "Skeleton Archer":  (),
    "Zombie":           ()
}

# Actor details
actor_details = {           # Sym   Fgcolor         Align   Sub/Ob          Poss    Cha_1   VD  Vis
    "Player":               ("@",   "Black",        "Good", "You",          "Your", 1,      6,  0),
    # Aberrations
    "Darkmantle": (),
    # Animals
    "Giant Ant": (),
    "Giant Badger": (),
    "Bat": (),
    "Giant Bee": (),
    "Fire Beetle":          ("b",   "Red",          "Neut", "a fire beetle", "its", 1,      5,  4),
    "Horned Beetle": (),
    "Centipede": (),
    "Dog": (),
    "Lizard": (),
    "Pony": (),
    "Rat": (),
    "Dire Rat": (),
    "Scorpion": (),
    "Viper": (),
    "Spider": (),
    "Stirge": (),
    "Weasel": (),
    "Wolf": (),
    # Constructs
    "Earthen Statue": (),
    # Devils
    "Black Abishai": (),
    "Lemure": (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf": (),
    # Elementals
    "Earth Vermin": (),
    "Earth Elemental":      ("E", "Red Brown",   "Neut", "an earth elemental", "its", 3, 4,  0),
    "Fire Vermin": (),
    "Lightning Vermin": (),
    # Elves
    "High Elf": (),
    "Wood Elf": (),
    # Goblins
    "Goblin": (),
    # Halflings
    "Halfling": (),
    # Kobolds
    "Kobold": (),
    "Kobold Acolyte":       ("k",   "White",    "Evil", "a kobold acolyte",     "her",  2,  5,  0),
    "Kobold Apprentice":    ("k",  "Magic Purple", "Evil", "a kobold apprentice",  "his",  2, 6, 0),
    "Kobold Scout": (),
    # Lycanthropes
    "Wererat": (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton": (),
    "Skeleton Archer": (),
    "Zombie": ()
}

# Actor Stats
actor_stats = {             # Str Int Wis Dex Con    MvL MS     Fort,   Refl,   Will,   hp
    "Player":               (11, 11, 11, 11, 11,     0, 10,     0,      0,      0,      10),
    # Aberrations
    "Darkmantle": (),
    # Animals
    "Giant Ant": (),
    "Giant Badger": (),
    "Bat": (),
    "Giant Bee": (),
    "Fire Beetle":          (13, 0,  11, 9,  13,    0, 14,      3,      0,      0,      8),
    "Horned Beetle": (),
    "Centipede": (),
    "Dog": (),
    "Lizard": (),
    "Pony": (),
    "Rat": (),
    "Dire Rat": (),
    "Scorpion": (),
    "Viper": (),
    "Spider": (),
    "Stirge": (),
    "Weasel": (),
    "Wolf": (),
    # Constructs
    "Earthen Statue": (),
    # Devils
    "Black Abishai": (),
    "Lemure": (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf": (),
    # Elementals
    "Earth Vermin": (),
    "Earth Elemental":      (15, 2,  11, 7,  15,    0, 16,      5,      1,      3,      8),
    "Fire Vermin": (),
    "Lightning Vermin": (),
    # Elves
    "High Elf": (),
    "Wood Elf": (),
    # Goblins
    "Goblin": (),
    # Halflings
    "Halfling": (),
    # Kobolds
    "Kobold": (),
    "Kobold Acolyte":       (11, 13, 16, 13, 13,    0, 9,       3,      0,      3,      8),
    "Kobold Apprentice":    (7,  16, 11, 15, 11,    0, 9,       1,      1,      3,      6),
    "Kobold Scout": (),
    # Lycanthropes
    "Wererat": (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton": (),
    "Skeleton Archer": (),
    "Zombie": ()
}

actor_defenses = {          # AC,    DR,    Hard,   SR,     AR, CR, ER, FR, NR
    "Player":               (10,    False,  0,      0,      0,  0,  0,  0,  0),
    # Aberrations
    "Darkmantle": (),
    # Animals
    "Giant Ant": (),
    "Giant Badger": (),
    "Bat": (),
    "Giant Bee": (),
    "Fire Beetle":          (16,    False,  0,      0,      0,  0,  0,  0,  0),
    "Horned Beetle": (),
    "Centipede": (),
    "Dog": (),
    "Lizard": (),
    "Pony": (),
    "Rat": (),
    "Dire Rat": (),
    "Scorpion": (),
    "Viper": (),
    "Spider": (),
    "Stirge": (),
    "Weasel": (),
    "Wolf": (),
    # Constructs
    "Earthen Statue": (),
    # Devils
    "Black Abishai": (),
    "Lemure": (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf": (),
    # Elementals
    "Earth Vermin": (),
    "Earth Elemental":      (18,    False,  0,      0,      0,  0,  0,  0,  0),
    "Fire Vermin": (),
    "Lightning Vermin": (),
    # Elves
    "High Elf": (),
    "Wood Elf": (),
    # Goblins
    "Goblin": (),
    # Halflings
    "Halfling": (),
    # Kobolds
    "Kobold": (),
    "Kobold Acolyte":       (16,    False,  0,      0,      0,  0,  0,  0,  0),
    "Kobold Apprentice":    (14,    False,  0,      0,      0,  0,  0,  0,  0),
    "Kobold Scout": (),
    # Lycanthropes
    "Wererat": (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton": (),
    "Skeleton Archer": (),
    "Zombie": ()
}

monster_details = {  # CR, Demeanor, AI Functions
    # Aberrations
    "Darkmantle": (),
    # Animals
    "Giant Ant": (),
    "Giant Badger": (),
    "Bat": (),
    "Giant Bee": (),
    "Fire Beetle": (),
    "Horned Beetle": (),
    "Centipede": (),
    "Dog": (),
    "Lizard": (),
    "Pony": (),
    "Rat": (),
    "Dire Rat": (),
    "Scorpion": (),
    "Viper": (),
    "Spider": (),
    "Stirge": (),
    "Weasel": (),
    "Wolf": (),
    # Constructs
    "Earthen Statue": (),
    # Devils
    "Black Abishai": (),
    "Lemure": (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf": (),
    # Elementals
    "Earth Vermin": (),
    "Earth Elemental": (),
    "Fire Vermin": (),
    "Lightning Vermin": (),
    # Elves
    "High Elf": (),
    "Wood Elf": (),
    # Goblins
    "Goblin": (),
    # Halflings
    "Halfling": (),
    # Kobolds
    "Kobold": (),
    "Kobold Acolyte": (),
    "Kobold Apprentice": (),
    "Kobold Scout": (),
    # Lycanthropes
    "Wererat": (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton": (),
    "Skeleton Archer": (),
    "Zombie": ()
}

monster_attacks = {
    # Aberrations
    "Darkmantle": (),
    # Animals
    "Giant Ant": (),
    "Giant Badger": (),
    "Bat": (),
    "Giant Bee": (),
    "Fire Beetle": (),
    "Horned Beetle": (),
    "Centipede": (),
    "Dog": (),
    "Lizard": (),
    "Pony": (),
    "Rat": (),
    "Dire Rat": (),
    "Scorpion": (),
    "Viper": (),
    "Spider": (),
    "Stirge": (),
    "Weasel": (),
    "Wolf": (),
    # Constructs
    "Earthen Statue": (),
    # Devils
    "Black Abishai": (),
    "Lemure": (),
    # Dragons
    "Young White Dragon": (),
    "Young Black Dragon": (),
    "Small Zombie Dragon": (),
    # Dwarves
    "Deep Dwarf": (),
    # Elementals
    "Earth Vermin": (),
    "Earth Elemental": (),
    "Fire Vermin": (),
    "Lightning Vermin": (),
    # Elves
    "High Elf": (),
    "Wood Elf": (),
    # Goblins
    "Goblin": (),
    # Halflings
    "Halfling": (),
    # Kobolds
    "Kobold": (),
    "Kobold Acolyte": (),
    "Kobold Apprentice": (),
    "Kobold Scout": (),
    # Lycanthropes
    "Wererat": (),
    # Misc
    "Fire Beetle Nest": (),
    # Undead
    "Skeleton": (),
    "Skeleton Archer": (),
    "Zombie": ()
}
