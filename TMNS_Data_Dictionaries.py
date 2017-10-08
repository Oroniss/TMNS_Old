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
