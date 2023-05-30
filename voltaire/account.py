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
        "lang": "en_CA"
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
        "lang": "en_CA"
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
            "Avoir/Être/Il y a": 0,
            "Les articles": 0,
            "Pronoms sujets": 0,
            "Les mots interrogatifs": 0
        },
        "1b": {
            "Présent régulier": 0,
            "La négation": 0,
            "Adjectif régulier + emploi": 0,
            "Les prépositions 1": 0,
            "Les mots liens 1": 0
        },
        "2a": {
            "Présent": 0,
            "Futur proche": 0,
            "Les adverbes": 0,
            "Interrogation inversé": 0
        },
        "2b": {
            "Adjectifs possessifs et démonstratifs": 0,
            "Verbes pronominaux": 0,
            "Adjectifs": 0,
            "Les prépositions 2": 0,
            "Impératif": 0
        },
        "3a": {
            "Comparatif et superlatif": 0,
            "Adjectifs irréguliers": 0,
            "Adverbes": 0,
            "Jouer à, de + faire de": 0
        },
        "3b": {
            "Les mots lien 2": 0,
            "Compléments d'object direct": 0,
            "Passé composé réguliers": 0,
            "Futur simple": 0
        },
        "4a": {
            "Présent OIR": 0,
            "Impératif employé avec COD": 0,
            "Présent avec changement orthographique": 0,
            "La négation du passé composé": 0,
        },
        "4b": {
            "Les participes passés irréguliers + pronominaux + négation": 0,
            "i=Imparfait + négation": 0,
            "Compléments d'object indirect": 0,
            "Conditionnel présent": 0
        },
        "5a": {
            "Concordance des temps 1": 0,
            "Impératif employe avec COI": 0,
            "Phrases de conditions 1": 0,
            "Y et en": 0
        },
        "5b": {
            "Verbes avec prépositions": 0,
            "Passé composé avec COD + accord": 0,
            "subjonctif 1": 0
        },
        "6a": {
            "Pronoms possessifs et relatifs": 0,
            "Les mots liens 3": 0,
            "Participe passé employé comme adjectif": 0,
            "subjonctif 2": 0
        },
        "6b": {
            "Participe présent": 0,
            "Plus-que-parfait": 0,
            "Futur antérieur": 0,
            "Conditionnel passé": 0,
            "Subjonctif 3": 0
        },
        "7a": {
            "Pronoms relatifs composés": 0,
            "Concordance des temps 2": 0,
            "Subjonctif 4": 0
        },
        "7b": {
            "Subjonctif 5": 0,
            "Phrases de condition 2": 0
        },
        "8a": {
            "Pronoms démonstratifs": 0,
            "Passé simple - emploi": 0,
            "Subjonctif 6": 0
        },
        "8b": {
            "Gérondif et adjectif verbal": 0,
            "Concordance des modes": 0
        },
        "9a": {
            "Gérondif et adjectif verbal - participe présent": 0,
            "Passé simple - emploi dans un texte": 0,
            "Subjonctif passé 1": 0
        },
        "9b": {
            "La voix passive": 0,
            "Subjonctif passé 2": 0
        }
    }

    return progress