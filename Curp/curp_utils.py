import random
from datetime import datetime
import calendar
import re

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_month(month, year):
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return calendar.monthrange(year, 1)[1]

def clean_name(text):
    """Remove special characters and convert to uppercase"""
    special_chars = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'X',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'x'
    }
    text = ''.join(special_chars.get(c, c) for c in text)
    return text.upper().strip()

def get_consonants(text):
    """Get consonants from text, excluding first letter"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    text = text[1:] if text else ''  #Excluir la primera letra
    return ''.join(c for c in text.upper() if c in consonants)

def get_first_internal_consonant(text):
    """Get first internal consonant, with special handling for Ñ"""
    consonants = get_consonants(text)
    if not consonants:
        return 'X'
    if consonants[0] == 'Ñ':
        return 'X'
    return consonants[0]

def get_first_vowel(text):
    """Get first vowel from text"""
    vowels = 'AEIOU'
    for c in text.upper():
        if c in vowels:
            return c
    return 'X'

def is_common_word(word):
    """Check if word is a common word that should be avoided"""
    common_words = {'MARIA', 'JOSE', 'MA', 'MA.', 'J', 'J.'}
    return word.upper() in common_words

def remove_article_prefix(name):
    """Remove articles and prepositions from the beginning of names"""
    prefixes = {'DA', 'DAS', 'DE', 'DEL', 'DER', 'DI', 'DIE', 'DD', 'EL', 
               'LA', 'LOS', 'LAS', 'LE', 'LES', 'MAC', 'MC', 'VAN', 'VON', 'Y'}
    
    parts = name.upper().split()
    if parts and parts[0] in prefixes:
        return ' '.join(parts[1:])
    return name

def check_forbidden_words(curp_start):
    """Check and replace forbidden words in CURP"""
    forbidden_words = {
        'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO', 
        'CAKA', 'CAKO', 'COGE', 'COGI', 'COJA', 'COJE', 'COJI', 'COJO', 
        'COLA', 'CULO', 'FALO', 'FETO', 'GETA', 'GUEI', 'GUEY', 'JETA', 
        'JOTO', 'KACA', 'KACO', 'KAGA', 'KAGO', 'KAKA', 'KAKO', 'KOGE', 
        'KOGI', 'KOJA', 'KOJE', 'KOJI', 'KOJO', 'KOLA', 'KULO', 'LOCA', 
        'LOCO', 'LOKA', 'LOKO', 'MAME', 'MAMO', 'MEAR', 'MEAS', 'MEON', 
        'MIAR', 'MION', 'MOCO', 'MOKO', 'MULA', 'MULO', 'NACA', 'NACO', 
        'PEDA', 'PEDO', 'PENE', 'PIPI', 'PITO', 'POPO', 'PUTA', 'PUTO', 
        'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN', 'SENO', 'TETA', 
        'VACA', 'VAGA', 'VAGO', 'VAKA', 'VUEI', 'VUEY', 'WUEI', 'WUEY'
    }
    
    if curp_start[:4] in forbidden_words:
        curp_start = curp_start[:1] + 'X' + curp_start[2:]
    return curp_start

def generate_curp(nombres, apellido1, apellido2, fecha_nac, sexo, estado):
    # Limpieza y preparación de los datos de entrada
    nombres = clean_name(nombres)
    apellido1 = clean_name(apellido1) if apellido1 else ''
    apellido2 = clean_name(apellido2) if apellido2 else ''
    
    # Controlar nombres compuestos
    nombres_parts = nombres.split()
    if len(nombres_parts) > 1:
        if nombres_parts[0] in ['MARIA', 'MA', 'MA.', 'JOSE', 'J', 'J.']:
            nombres = ' '.join(nombres_parts[1:])
    
    # Eliminar artículos y preposiciones
    apellido1 = remove_article_prefix(apellido1)
    apellido2 = remove_article_prefix(apellido2)
    nombres = remove_article_prefix(nombres)
    
    # Empieza a construir CURP
    curp = ''
    
    # Primera letra del primer apellido
    curp += apellido1[0] if apellido1 else 'X'
    
    # Primera vocal interna del primer apellido
    if apellido1:
        curp += get_first_vowel(apellido1[1:])
    else:
        curp += 'X'
    
    # Primera letra del segundo apellido
    curp += apellido2[0] if apellido2 else 'X'
    
    # Primera letra del nombre
    curp += nombres[0]
    
    # Comprueba si hay palabras prohibidas y reemplácelas si es necesario
    curp = check_forbidden_words(curp)
    
    # Agregar fecha de nacimiento
    year, month, day = fecha_nac.split('-')
    curp += year[2:]
    curp += month
    curp += day
    
    # Agregar sexo
    curp += sexo.upper()
    
    # Agregar código de estado
    curp += estado
    
    # Añadir la primera consonante interna del primer apellido
    if apellido1:
        curp += get_first_internal_consonant(apellido1)
    else:
        curp += 'X'
    
    # Añadir la primera consonante interna del segundo apellido
    if apellido2:
        curp += get_first_internal_consonant(apellido2)
    else:
        curp += 'X'
    
    # Agregue la primera consonante interna del nombre
    curp += get_first_internal_consonant(nombres)
    
    # Agregue el dígito de diferenciación para el año de nacimiento
    curp += '0' if int(year) < 2000 else 'A'
    
    # Agregar dígito de verificación aleatorio
    curp += str(random.randint(0, 9))
    
    return curp

def validate_date(day, month, year):
    try:
        max_days = get_days_in_month(int(month), int(year))
        return 1 <= int(day) <= max_days
    except ValueError:
        return False