ATTRIBUTES=[
    {'name':'Attractivness','abbr':'ATTR', 'skills':['Personal Grooming', 'Wardrobe & Style']},
    {'name':'Body','abbr':'BODY', 'skills':['Endurance', 'Strength Feat', 'Swimming']},
    {'name':'Cool','abbr':'COOL', 'skills':['Interrogation', 'Intimidate', 'Oratory', 'Resist Torture/Drugs', 'Streetwise']},
    {'name':'Empathy','abbr':'EMP', 'skills':['Human Perception','Interview','Leadership','Seduction','Social','Persuasion & Fast Talk','Perform']},
    {'name':'Intelligence','abbr':'INT', 'skills':['Accounting','Anthropology','Awareness/Notice','Biology','Botany','Chemistry','Composition','Diagnose Illness','Education & General Knowledge','Expert','Gamble','Geology','Hide/Evade','History','Language','Library Search','Mathematics','Physics','Programming','Stock Market','System Knowledge','Teaching','Wilderness Survival','Zoology']},
    {'name':'Luck','abbr':'LUCK', 'skills':[]},
    {'name':'Movement Allowance','abbr':'MA', 'skills':[]},
    {'name':'Reflex','abbr':'REF', 'skills':['Archery','Athletics','Brawling','Dance','Dodge & Escape','Driving','Fencing','Handgun','Heavy Weapons','Martial Art','Melee','Motorcycle','Operate Heavy Machinery','Pilot (Gyro)','Pilot (Fixed Wing)','Pilot (Dirigible)','Pilot (Vector Thrust Vehicle)','Rifle','Stealth','Submachinegun']},
    {'name':'Tech','abbr':'TECH', 'skills':['Aero Tech','AV Tech','Basic Tech','Cryotank Operation','Cyberdeck Design','Cyber Tech','Demolitions','Disguise','Electronics','Electronic Security','First Aid','Forgery','Gyro Tech','Paint/Draw','Photo & Film','Pharmacuticals','Pick Lock','Pick Pocket','Play Instrument','Weaponsmith']}
]

def default_attributes():
    default_attributes = {}
    for attr in ATTRIBUTES:
        default_attributes[attr['abbr']] = {'value':0, 'skills':[]};
    return default_attributes
