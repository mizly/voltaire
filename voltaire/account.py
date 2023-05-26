def new_teacher(id_info):
    """
    Creates a new teacher profile based on the provided Google account information.
    
    Parameters:
        id_info: the information provided by authentication
    
    Returns:
        teacher: the new teacher profile
    """
    teacher = {
        "_id": id_info.get("sub"),
        "given_name": id_info.get("given_name"),
        "family_name": id_info.get("family_name"),
        "class": [],
        "default_lang": "en_CA"
    }

    return teacher

def new_student(id_info):
    """
    Creates a new student profile based on the provided Google account information.
    
    Parameters:
        id_info: the information provided by authentication
    
    Returns:
        student: the new student profile
    """
    student = {
        "_id": id_info.get("sub"),
        "given_name": id_info.get("given_name"),
        "family_name": id_info.get("family_name"),
        "grade": None,
        "class": "",
        "default_lang": "en_CA"
    }

    return student

def new_progress(id_info):
    """
    Creates a new progress profile based on the provided Google account information.
    
    Parameters:
        id_info: the information provided by authentication
    
    Returns:
        progress: the new progress profile
    """
    progress = {
        "_id": id_info.get("sub"),
        "1a": {
            "avoir/etre/il y a": 0,
            "les articles": 0,
            "pronoms sujets": 0,
            "les mots interrogatifs": 0
        },
        "1b": {
            "present regulier": 0,
            "la negation": 0,
            "adjectif regulier + emploi": 0,
            "les prepositions 1": 0,
            "les mots liens 1": 0
        },
        "2a": {
            "present": 0,
            "futur proche": 0,
            "les adverbes": 0,
            "interrogation inverse": 0
        },
        "2b": {
            "adjectifs possessifs et demonstratifs": 0,
            "verbes pronominaux": 0,
            "adjectifs": 0,
            "les prepositions 2": 0,
            "imperatif": 0
        },
        "3a": {
            "comparatif et superlatif": 0,
            "adjectifs irreguliers": 0,
            "adverbes": 0,
            "jouer a, de + fare de": 0
        },
        "3b": {
            "les mots lien 2": 0,
            "complements d'object direct": 0,
            "passe compose reguliers": 0,
            "futur simple": 0
        },
        "4a": {
            "present oir": 0,
            "imperatif employe avec cod": 0,
            "present avec changement orthographique": 0,
            "la negation du passse compose": 0,
        },
        "4b": {
            "les participes passes irreguliers + pronominaux + negation": 0,
            "imparfait + engation": 0,
            "completions d'object indirect": 0,
            "conditionnel present": 0
        },
        "5a": {
            "concordance des temps 1": 0,
            "imperatif employe avec coi": 0,
            "phrases de conditions 1": 0,
            "y et en": 0
        },
        "5b": {
            "verbes avec prepositions": 0,
            "passe compose avec cod + accord": 0,
            "subjonctif 1": 0
        },
        "6a": {
            "pronoms possessifs et relatifs": 0,
            "les mots liens 3": 0,
            "participe passe employe comme adjectif": 0,
            "subjonctif 2": 0
        },
        "6b": {
            "participe present": 0,
            "plus-que-parfait": 0,
            "futur anterieur": 0,
            "conditionnel passe": 0,
            "subjonctif 3": 0
        },
        "7a": {
            "pronoms relatifs composes": 0,
            "concordance des temps 2": 0,
            "subjonctif 4": 0
        },
        "7b": {
            "subjonctif 5": 0,
            "phrases de condition 2": 0
        },
        "8a": {
            "pronoms demonstratifs": 0,
            "passe simple - emploi": 0,
            "subjonctif 6": 0
        },
        "8b": {
            "gerondif et adjectif verbal": 0,
            "concordance des modes": 0
        },
        "9a": {
            "gerondif et adjectif verbal - participe present": 0,
            "passe simple - emploi dans un texte": 0,
            "subjonctif passe 1": 0
        },
        "9b": {
            "la voix passive": 0,
            "subjonctif passe 2": 0
        }
    }

    return progress