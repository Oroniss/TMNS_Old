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
    "Barricade":        ("|",   False,    3,  3,  3,  None,         None,               None)
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
