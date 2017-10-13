##################################################################################################################
#                                       Material Dictionary.
##################################################################################################################

material_properties = {  # AC,  DR, HA, SR,     AR, CR, ER, FR, NR,     HP/V,   Adjective,  fgcolor, Traits
    "Cloth":        (0,     False,  0,  0,     -25, 5,  -15, -30, -30,  5,      "Cloth",    "Putrid Green",
                     {"Cloth", "Organic"}),
    "Glass":        (0,     False,  0,  0,      5,  15, -30, 20, -20,   5,      "Glass",    "Magic Purple",
                     {"Glass", "Inorganic"}),
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

furnishing_details = {  # Sym,  BLos, BMov, SMov, Vol bgc,          fogcolor            material
    "Altar":            ("#",   False,    0,  0,  5,  None,         None,               None),
    "Barricade":        ("|",   False,    2,  2,  3,  None,         None,               None),
    "Cage":             ("#",   False,    2,  2,  3,  None,         None,               None),
    "Chest":            ("+",   False,    0,  0,  2,  None,         None,               None),
    "Closet":           ("#",   True,     3,  3,  5,  None,         None,               None),
    "Circle":           (".",   False,    0,  0,  1,  None,         None,               None),
    "Compartment":      ("+",   False,    0,  0,  1,  None,         None,               None),
    "Door":             ("+",   True,     3,  3,  4,  None,         None,               None),
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
    "Barricade":        (),
    "Cage":             (),
    "Circle":           (),
    "Empty":            (),
    "Grease":           (),  # TODO: Add stuff here
    "Ice":              (),  # TODO: Add stuff here
    "Laboratory":       (),
    "Pedestal":         (),
    "Rubbish":          (),
    "Stair":            (),
    "Statue":           (),
    "Web":              (),
    "Well":             ()
}

##################################################################################################################
#                                       Actor Dictionaries.
##################################################################################################################

# Actor traits
actor_traits = {
    "Player":           ("Player",)
}

# Actor details
actor_details = {   # Sym   Fgcolor         Align   Sub/Ob          Poss    Cha_1   VD  Vis
    "Player":       ("@",   "Black",        "Good", "You",          "Your", 1,      6,  0)
}

# Actor Stats
actor_stats = {    # Str Int Wis Dex Con    MvL MS      Fort,   Refl,   Will,   hp
    "Player":       (11, 11, 11, 11, 11,     0, 10,     0,      0,      0,      (1, 10))
}

actor_defenses = {  # AC,    DR,    Hard,   SR,     AR, CR, ER, FR, NR
    "Player":       (10,    False,  0,      0,      0,  0,  0,  0,  0)
}
