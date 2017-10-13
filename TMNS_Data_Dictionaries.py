##################################################################################################################
#                                       Material Dictionary.
##################################################################################################################

material_properties = {  # AC,  DR, HA, SR,     AR, CR, ER, FR, NR,     HP/V,   Adjective,  fgcolor, Traits
    "Wood":         (10,    False,  2,  0,     -10, 10, -10, -20, -30,  5,      "Wooden",   "Wood Brown",
                     {"Wood", "Organic"})
}

##################################################################################################################
#                                       Furnishing Dictionary.
##################################################################################################################

furnishing_details = {  # Sym,  BLos, BMov, SMov, Vol bgc,          fogcolor            material
    "Altar":            ("#",   False,    1,  1,  5,  None,         None,               "immune"),
    "Barricade":        ("|",   False,    3,  3,  3,  None,         None,               None),
    "Cage":             ("#",   False,    3,  3,  3,  None,         None,               None),
    "Chest":            ("+",   False,    1,  1,  2,  None,         None,               None),
    "Closet":           ("#",   True,     4,  4,  5,  None,         None,               None),
    "Circle":           (".",   False,    1,  1,  1,  None,         None,               "immune"),
    "Compartment":      ("+",   False,    1,  1,  1,  None,         None,               None),
    "Door":             ("+",   True,     5,  5,  4,  None,         None,               None)
}

furnishing_functions = {  # Tuples of (type, function_name)
    "Barricade":        ()
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
    "Player":       (11, 11, 11, 11, 11,     1, 10,     0,      0,      0,      (1, 10))
}

actor_defenses = {  # AC,    DR,    Hard,   SR,     AR, CR, ER, FR, NR
    "Player":       (10,    False,  0,      0,      0,  0,  0,  0,  0)
}
