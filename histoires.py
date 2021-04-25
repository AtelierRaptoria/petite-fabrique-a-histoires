#!/usr/bin/python3
# coding: utf-8

"""
La Petite Fabrique a histoires
Génération d'histoires très courtes affichées sur une écran relié à une Arduino

Dépôt Gitlab : https://gitlab.com/AtelierRaptoria/petite-fabrique-a-histoires

Matériel :
- 1 carte Arduino
- 1 breadboard
- 1 écran LCD
- 1 potentiomère
- 1 bouton poussoir
- 1 résistance 10kΩ
- 1 résistance 220Ω
- câbles

Installation des dépendances Python :
pip install -r requirements.txt

Câblage :
Câbler vote Arduino comme indiqué sur cablage.png

Usage :
1. Compiler et téléverser le script petite-fabrique-a-histoires.ino sur votre Arduino
2. Lancer le script histoires.py --port <port de votre Arduino>
3. Appuyer sur le bouton poussoir
4. Lire les histoires 😁
"""


# Métadonnées
# ==============================================================================

__author__ = "Raptoria"
__copyright__ = "Copyright 2021"
__date__ = "Avril 2021"
__credits__: ["Raptoria"]
__version__ = "1.0"
__maintainer__ = "Raptoria"
__email__ = "raptoria@raptoria.fr"
__status__ = "Production"


# Bibliothèques
# ==============================================================================

import argparse
import random
import re
import serial


# Arguments
# ==============================================================================

parser = argparse.ArgumentParser(description="Connexion avec la carte Arduino")
parser.add_argument("--port", "-p",
                    default="/dev/ttyACM0", metavar="port",
                    help="Port sur lequel se trouve votre carte Arduino (default: '/dev/ttyACM0')")
args = parser.parse_args()
port = args.port


# Connexion à Arduino
# ==============================================================================

try:
   arduino = serial.Serial(port, 9600, timeout=0.1)
   print("Arduino connectée !")
except:
   print(f"Impossible de se connecter sur ${ port }")


# Grammaire
# ==============================================================================

HISTOIRES = {

    # Phrases d'introduction qui peuvent être utilisées tout le temps
    "INTRO_GEN": [
        "Il etait une fois",
        "Autrefois, il etait",
        "Jadis, il y avait",
        "Au temps jadis, il y avait",
        "Dans une galaxie lointaine, tres lointaine, il existait",
        "Il y a fort longtemps, il etait"
    ],

    # Phrases d'introduction à n'utiliser que si ce qui suit commence
    # par une voyelle
    "INTRO_VOY": [
        "C'est l'histoire d'"
    ],

    # Phrases d'introduction à n'utiliser que si ce qui suit commence
    # par une consonne
    "INTRO_CON": [
        "C'est l'histoire de"
    ],

    # Phrases d'introduction suivies d'un syntagme nominal au singulier
    "INTRO_SNG": [
        ["INTRO_GEN"],
        ["INTRO_VOY"]
    ],

    # Phrases d'introduction suivies d'un syntagme nominal au pluriel
    # commençant par une voyelle
    "INTRO_PLU_VOY": [
        ["INTRO_VOY"],
        ["INTRO_GEN", "des"]
    ],

    # Phrases d'introduction suivies d'un syntagme nominal au pluriel
    # commençant par une consonne
    "INTRO_PLU_CON": [
        ["INTRO_CON"],
        ["INTRO_GEN", "de"]
    ],

    # Phrases de conclusion si le protagoniste principal est
    # un substantif masculin au singulier
    "FIN_SNG_MASC": [
        ", et il mourut",
        ", et il trepassa",
        ", et il succomba",
        ", et il deceda",
        ", et il perit",
        ", et il clamsa",
        ", et il creva",
        ", et il passa l'arme a gauche",
        ", et il s'eteignit",
        ", et il calancha",
        ", et il claqua",
        ", et il poussa son dernier rale",
        ", et il deperit",
        ", et il rendit l'ame",
        ", et il cassa sa pipe",
        ", et il alla ad padres",
        ", et il partit les pieds devant",
        ", et il sortit entre quatre planches",
        ", et il y laissa ses guetres",
        ", et il y laissa ses houseaux"
    ],

    # Phrases de conclusion si le protagoniste principal est
    # un substantif féminin au singulier
    "FIN_SNG_FEM": [
        ", et elle mourut",
        ", et elle trepassa",
        ", et elle succomba",
        ", et elle deceda",
        ", et elle perit",
        ", et elle clamsa",
        ", et elle creva",
        ", et elle passa l'arme a gauche",
        ", et elle s'eteignit",
        ", et elle calancha",
        ", et elle claqua",
        ", et elle poussa son dernier rale",
        ", et elle deperit",
        ", et elle rendit l'ame",
        ", et elle cassa sa pipe",
        ", et elle alla ad padres",
        ", et elle partit les pieds devant",
        ", et elle sortit entre quatre planches",
        ", et elle y laissa ses guetres",
        ", et elle y laissa ses houseaux"
    ],

    # Phrases de conclusion si le protagoniste principal est
    # un substantif masculin au pluriel
    "FIN_PLU_MASC": [
        ", et ils moururent",
        ", et ils trepasserent",
        ", et ils succomberent",
        ", et ils decederent",
        ", et ils perirent",
        ", et ils clamserent",
        ", et ils creverent",
        ", et ils passerent l'arme a gauche",
        ", et ils s'eteignirent",
        ", et ils calancherent",
        ", et ils claquerent",
        ", et ils pousserent leur dernier rale",
        ", et ils deperirent",
        ", et ils rendirent l'ame",
        ", et ils casserent leur pipe",
        ", et ils allerent ad padres",
        ", et ils partirent les pieds devant",
        ", et ils sortirent entre quatre planches",
        ", et ils y laisserent leurs guetres",
        ", et ils y laisserent leurs houseaux"
    ],

    # Phrases de conclusion si le protagoniste principal est
    # un substantif féminin au pluriel
    "FIN_PLU_FEM": [
        ", et elles moururent",
        ", et elles trepasserent",
        ", et elles succomberent",
        ", et elles decederent",
        ", et elles perirent",
        ", et elles clamserent",
        ", et elles creverent",
        ", et elles passerent l'arme a gauche",
        ", et elles s'eteignirent",
        ", et elles calancherent",
        ", et elles claquerent",
        ", et elles pousserent leur dernier rale",
        ", et elles deperirent",
        ", et elles rendirent l'ame",
        ", et elles casserent leur pipe",
        ", et elles allerent ad padres",
        ", et elles partirent les pieds devant",
        ", et elles sortirent entre quatre planches",
        ", et elles y laisserent leurs guetres",
        ", et elles y laisserent leurs houseaux"
    ],

    # Quelques nombres
    "NOMBRES": [
        "trois",
        "quarante-deux",
        "quatorze",
        "cent dix-huit",
        "treize",
        "vingt-six",
        "quarante-douze",
        "trouze mille"
    ],

    # Substantifs au masculin singulier commençant par une voyelle
    "NOM_SNG_MASC_VOY": [
        "ornithorynque",
        "amphigouri",
        "etourneau",
        "echalas"
    ],

    # Substantifs au masculin singulier commençant par une consonne
    "NOM_SNG_MASC_CON": [
        "topinambour",
        "branquignol",
        "cassoulet",
        "parpaing",
        "cacemphate",
        "coquelicot",
        "pleutre",
        "cachalot"
    ],

    # Substantifs au féminin singulier commençant par une voyelle
    "NOM_SNG_FEM_VOY": [
        "enzyme",
        "aubergine",
        "aiguille a tricoter",
        "aphelie"
    ],

    # Substantifs au féminin singulier commençant par une voyelle
    "NOM_SNG_FEM_CON": [
        "melopee",
        "dereliction",
        "ratatouille",
        "mangrove",
        "lentille",
        "varicelle",
        "meteorite",
        "syzygie"
    ],

    # Ensemble des substantifs au masculin singulier
    "NOM_SNG_MASC" : [
        ["NOM_SNG_MASC_VOY"],
        ["NOM_SNG_MASC_CON"]
    ],

    # Ensemble des substantifs au féminin singulier
    "NOM_SNG_FEM" : [
        ["NOM_SNG_FEM_VOY"],
        ["NOM_SNG_FEM_CON"]
    ],

    # Substantifs au masculin pluriel commençant par une voyelle
    "NOM_PLU_MASC_VOY": [
        "ornithorynques",
        "amphigouris",
        "etourneaux",
        "echalas"
    ],

    # Substantifs au masculin pluriel commençant par une consonne
    "NOM_PLU_MASC_CON": [
        "topinambours",
        "branquignols",
        "cassoulets",
        "parpaings",
        "tabourets",
        "coquelicots",
        "pleutres",
        "cachalots"
    ],

    # Substantifs au féminin pluriel commençant par une voyelle
    "NOM_PLU_FEM_VOY": [
        "enzymes",
        "aubergines",
        "aiguilles a tricoter",
        "aphelies"
    ],

    # Substantifs au féminin pluriel commençant par une voyelle
    "NOM_PLU_FEM_CON": [
        "melopees",
        "derelictions",
        "ratatouilles",
        "mangroves",
        "lentilles",
        "varicelles",
        "meteorites",
        "syzygies"
    ],

    # Ensemble des substantifs au masculin pluriel
    "NOM_PLU_MASC" : [
        ["NOM_PLU_MASC_VOY"],
        ["NOM_PLU_MASC_CON"]
    ],

    # Ensemble des substantifs au féminin pluriel
    "NOM_PLU_FEM" : [
        ["NOM_PLU_FEM_VOY"],
        ["NOM_PLU_FEM_CON"]
    ],

    # Article indéfini au masculin singulier
    "ART_IND_SNG_MASC": [
        "un"
    ],

    # Article indéfini au féminin singulier
    "ART_IND_SNG_FEM": [
        "une"
    ],

    # Article indéfini au pluriel
    "ART_IND_PLU": [
        "des"
    ],

    # Déterminants au pluriel ('des' ou nombres)
    "DET_PLU": [
        ["ART_IND_PLU"],
        ["NOMBRES"]
    ],

    # Adjectifs qualificatifs au masculin singulier
    # Ces adjectifs sont placés AVANT le substantif
    "ADJ_SNG_MASC_AV": [
        "grand",
        "petit",
        "nouveau",
        "sacre",
        "simple",
        "pauvre"
        ""
    ],

    # Adjectifs qualificatifs au masculin singulier
    # Ces adjectifs sont placés APRÈS le substantif
    "ADJ_SNG_MASC_AP": [
        "ebahi",
        "ebaudi",
        "abasourdi",
        "curieux",
        "triste",
        "patibulaire",
        "taciturne",
        ""
    ],

    # Adjectifs qualificatifs au féminin singulier
    # Ces adjectifs sont placés AVANT le substantif
    "ADJ_SNG_FEM_AV": [
        "grande",
        "petite",
        "nouvelle",
        "sacree",
        "simple",
        "pauvre",
        ""
    ],

    # Adjectifs qualificatifs au féminin singulier
    # Ces adjectifs sont placés APRÈS le substantif
    "ADJ_SNG_FEM_AP": [
        "ebahie",
        "ebaudie",
        "abasourdie",
        "curieuse",
        "triste",
        "patibulaire",
        "taciturne",
        ""
    ],

    # Adjectifs qualificatifs au masculin pluriel
    # Ces adjectifs sont placés AVANT le substantif
    "ADJ_PLU_MASC_AV": [
        "grands",
        "petits",
        "nouveaux",
        "sacres",
        "simples",
        "pauvres",
        ""
    ],

    # Adjectifs qualificatifs au masculin pluriel
    # Ces adjectifs sont placés APRÈS le substantif
    "ADJ_PLU_MASC_AP": [
        "ebahis",
        "ebaudis",
        "abasourdis",
        "curieux",
        "tristes",
        "patibulaires",
        "taciturnes",
        ""
    ],

    # Adjectifs qualificatifs au féminin pluriel
    # Ces adjectifs sont placés AVANT le substantif
    "ADJ_PLU_FEM_AV": [
        "grandes",
        "petites",
        "nouvelles",
        "sacrees",
        "simples",
        "pauvres",
        ""
    ],

    # Adjectifs qualificatifs au féminin pluriel
    # Ces adjectifs sont placés APRÈS le substantif
    "ADJ_PLU_FEM_AP": [
        "ebahies",
        "ebaudies",
        "abasourdies",
        "curieuses",
        "tristes",
        "patibulaires",
        "taciturnes",
        ""
    ],

    # Syntagmes nominaux avec un substantif au masculin singulier
    "SN_SNG_MASC": [
        ["ART_IND_SNG_MASC", "ADJ_SNG_MASC_AV", "NOM_SNG_MASC", "ADJ_SNG_MASC_AP"],
        ["ART_IND_SNG_MASC", "ADJ_SNG_MASC_AV", "NOM_SNG_MASC"],
        ["ART_IND_SNG_MASC", "NOM_SNG_MASC", "ADJ_SNG_MASC_AP"],
        ["ART_IND_SNG_MASC", "NOM_SNG_MASC"]
    ],

    # Syntagmes nominaux avec un substantif au féminin singulier
    "SN_SNG_FEM": [
        ["ART_IND_SNG_FEM", "ADJ_SNG_FEM_AV", "NOM_SNG_FEM", "ADJ_SNG_FEM_AP"],
        ["ART_IND_SNG_FEM", "ADJ_SNG_FEM_AV", "NOM_SNG_FEM"],
        ["ART_IND_SNG_FEM", "NOM_SNG_FEM", "ADJ_SNG_FEM_AP"],
        ["ART_IND_SNG_FEM", "NOM_SNG_FEM"]
    ],

    # Syntagmes nominaux avec un substantif au masculin pluriel
    # Introduits par 'des'
    "SN_PLU_MASC_ART": [
        ["ART_IND_PLU", "ADJ_PLU_MASC_AV", "NOM_PLU_MASC", "ADJ_PLU_MASC_AP"],
        ["ART_IND_PLU", "ADJ_PLU_MASC_AV", "NOM_PLU_MASC"],
        ["ART_IND_PLU", "NOM_PLU_MASC", "ADJ_PLU_MASC_AP"],
        ["ART_IND_PLU", "NOM_PLU_MASC"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Sans article commençant par une voyelle
    "SN_PLU_MASC_NO_ART_VOY": [
        ["NOM_PLU_MASC"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Sans article commençant par une consonne
    "SN_PLU_MASC_NO_ART_CON": [
        ["ADJ_PLU_MASC_AV", "NOM_PLU_MASC", "ADJ_PLU_MASC_AP"],
        ["ADJ_PLU_MASC_AV", "NOM_PLU_MASC"],
        ["NOM_PLU_MASC", "ADJ_PLU_MASC_AP"]
    ],

    # Ensemble des syntagmes nominaux avec un substantif au féminin pluriel
    "SN_PLU_MASC_NO_ART": [
        ["SN_PLU_MASC_NO_ART_VOY"],
        ["SN_PLU_MASC_NO_ART_CON"]
    ],

    # Syntagmes nominaux avec un substantif au masculin pluriel
    # Introduits par un nombre
    "SN_PLU_MASC_NOMBRES": [
        ["NOMBRES", "ADJ_PLU_MASC_AV", "NOM_PLU_MASC", "ADJ_PLU_MASC_AP"],
        ["NOMBRES", "ADJ_PLU_MASC_AV", "NOM_PLU_MASC"],
        ["NOMBRES", "NOM_PLU_MASC", "ADJ_PLU_MASC_AP"],
        ["NOMBRES", "NOM_PLU_MASC"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Introduits par 'des'
    "SN_PLU_FEM_ART": [
        ["ART_IND_PLU", "ADJ_PLU_FEM_AV", "NOM_PLU_FEM", "ADJ_PLU_FEM_AP"],
        ["ART_IND_PLU", "ADJ_PLU_FEM_AV", "NOM_PLU_FEM"],
        ["ART_IND_PLU", "NOM_PLU_FEM", "ADJ_PLU_FEM_AP"],
        ["ART_IND_PLU", "NOM_PLU_FEM"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Sans article commençant par une voyelle
    "SN_PLU_FEM_NO_ART_VOY": [
        ["NOM_PLU_FEM"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Sans article commençant par une consonne
    "SN_PLU_FEM_NO_ART_CON": [
        ["ADJ_PLU_FEM_AV", "NOM_PLU_FEM", "ADJ_PLU_FEM_AP"],
        ["ADJ_PLU_FEM_AV", "NOM_PLU_FEM"],
        ["NOM_PLU_FEM", "ADJ_PLU_FEM_AP"]
    ],

    # Ensemble des syntagmes nominaux avec un substantif au féminin pluriel
    "SN_PLU_FEM_NO_ART": [
        ["SN_PLU_FEM_NO_ART_VOY"],
        ["SN_PLU_FEM_NO_ART_CON"]
    ],

    # Syntagmes nominaux avec un substantif au féminin pluriel
    # Introduits par un nombre
    "SN_PLU_FEM_NOMBRES": [
        ["NOMBRES", "ADJ_PLU_FEM_AV", "NOM_PLU_FEM", "ADJ_PLU_FEM_AP"],
        ["NOMBRES", "ADJ_PLU_FEM_AV", "NOM_PLU_FEM"],
        ["NOMBRES", "NOM_PLU_FEM", "ADJ_PLU_FEM_AP"],
        ["NOMBRES", "NOM_PLU_FEM"]
    ],

    # Ensemble des syntagmes nominaux avec un substantif au masculin pluriel
    "SN_PLU_MASC": [
        ["SN_PLU_MASC_ART"],
        ["SN_PLU_MASC_NOMBRES"]
    ],

    # Ensemble des syntagmes nominaux avec un substantif au féminin pluriel
    "SN_PLU_FEM": [
        ["SN_PLU_FEM_ART"],
        ["SN_PLU_FEM_NOMBRES"]
    ],

    # Ensemble des syntagmes nominaux
    "SN": [
        "SN_SNG_MASC",
        "SN_SNG_FEM",
        "SN_PLU_MASC",
        "SN_PLU_FEM"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du singulier
    # Imparfait de l'indicatif
    "VTD_IMP_SNG": [
        "flagornait",
        "persiflait",
        "lantiponnait",
        "desenchantait",
        "bleutait"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du singulier
    # S'utilisent avec la préposition 'de'
    # Imparfait de l'indicatif
    "VTI_IMP_DE_SNG": [
        "accouchait",
        "heritait",
        "revait"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'à'
    # Imparfait de l'indicatif
    "VTI_IMP_A_SNG": [
        "ressemblait",
        "desobeissait",
        "survivait"
    ],

    # Verbes intransitifs conjugués à la troisième personne du pluriel
    # Imparfait de l'indicatif
    "VIT_IMP_SNG": [
        "glougloutait",
        "felissait",
        "aboutait",
        "baguenaudait",
        "soliloquait"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du pluriel
    # Imparfait de l'indicatif
    "VTD_IMP_PLU": [
        "flagornaient",
        "persiflaient",
        "lantiponnaient",
        "desenchantaient",
        "bleutaient"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'de'
    # Imparfait de l'indicatif
    "VTI_IMP_DE_PLU": [
        "accouchaient",
        "heritaient",
        "revaient"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'à'
    # Imparfait de l'indicatif
    "VTI_IMP_A_PLU": [
        "ressemblaient",
        "desobeissaient",
        "survivaient"
    ],

    # Verbes intransitifs conjugués à la troisième personne du pluriel
    # Imparfait de l'indicatif
    "VIT_IMP_PLU": [
        "glougloutaient",
        "felissaient",
        "aboutaient",
        "baguenaudaient",
        "soliloquaient"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du singulier
    # Plus-que-parfait de l'indicatif
    "VTD_PQP_SNG": [
        "avait flagorne",
        "avait persifle",
        "avait lantiponne",
        "avait desenchante",
        "avait bleute"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du singulier
    # S'utilisent avec la préposition 'de'
    # Plus-que-parfait de l'indicatif
    "VTI_PQP_DE_SNG": [
        "avait accouche",
        "avait herite",
        "avait reve"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'à'
    # Plus-que-parfait de l'indicatif
    "VTI_PQP_A_SNG": [
        "avait ressemble",
        "avait desobeisse",
        "avait survécu"
    ],

    # Verbes intransitifs conjugués à la troisième personne du pluriel
    # Plus-que-parfait de l'indicatif
    "VIT_PQP_SNG": [
        "avait glougloute",
        "avait feli",
        "avait aboute",
        "avait baguenaude",
        "avait soliloque"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du pluriel
    # Plus-que-parfait de l'indicatif
    "VTD_PQP_PLU": [
        "avaient flagorne",
        "avaient persifle",
        "avaient lantiponne",
        "avaient desenchante",
        "avaient bleute"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'de'
    # Plus-que-parfait de l'indicatif
    "VTI_PQP_DE_PLU": [
        "avaient accouche",
        "avaient herite",
        "avaient reve"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'à'
    # Plus-que-parfait de l'indicatif
    "VTI_PQP_A_PLU": [
        "avaient ressemble",
        "avaient desobei",
        "avaient survecu"
    ],

    # Verbes intransitifs conjugués à la troisième personne du pluriel
    # Plus-que-parfait de l'indicatif
    "VIT_PQP_PLU": [
        "avaient glougloute",
        "avaient feli",
        "avaient aboute",
        "avaient baguenaude",
        "avaient soliloque"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du singulier
    # Passé simple de l'indicatif
    "VTD_PAS_SNG": [
        "flagorna",
        "persifla",
        "lantiponna",
        "desenchanta",
        "bleuta"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du singulier
    # S'utilisent avec la préposition 'de'
    # Plus-que-parfait de l'indicatif
    "VTI_PAS_DE_SNG": [
        "accoucha",
        "herita",
        "reva"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du singulier
    # S'utilisent avec la préposition 'à'
    # Passé simple de l'indicatif
    "VTI_PAS_A_SNG": [
        "ressembla",
        "desobeit",
        "survecut"
    ],

    # Verbes intransitifs conjugués à la troisième personne du singulier
    # Passé simple de l'indicatif
    "VIT_PAS_SNG": [
        "glouglouta",
        "felit",
        "abouta",
        "baguenauda",
        "soliloqua"
    ],

    # Verbes transitifs directs conjugués à la troisième personne du pluriel
    # Passé simple de l'indicatif
    "VTD_PAS_PLU": [
        "flagornerent",
        "persiflerent",
        "lantiponnerent",
        "desenchanterent",
        "bleuterent"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'de'
    # Plus-que-parfait de l'indicatif
    "VTI_PAS_DE_PLU": [
        "accoucherent",
        "heriterent",
        "reverent"
    ],

    # Verbes transitifs indirects conjugués à la troisième personne du pluriel
    # S'utilisent avec la préposition 'à'
    # Passé simple de l'indicatif
    "VTI_PAS_A_PLU": [
        "ressemblerent",
        "desobeirent",
        "survecurent"
    ],

    # Verbes intransitifs conjugués à la troisième personne du pluriel
    # Passé simple de l'indicatif
    "VIT_PAS_PLU": [
        "glouglouterent",
        "felirent",
        "s'ablutionnerent",
        "baguenauderent",
        "soliloquerent"
    ],

    # Préposition 'à'
    "PREP_A": [
        "a"
    ],

    # Préposition 'aux'
    "PREP_AUX": [
        "aux"
    ],

    # Syntagme prépositionnel introduit par 'à'
    "SP_A": [
        ["PREP_A", "SN_SNG_MASC"],
        ["PREP_A", "SN_SNG_FEM"],
        ["PREP_A", "SN_PLU_MASC_ART"],
        ["PREP_A", "SN_PLU_FEM_ART"],
        ["PREP_AUX", "SN_PLU_MASC_NOMBRES"],
        ["PREP_AUX", "SN_PLU_FEM_NOMBRES"]
    ],

    # Préposition 'de' suivie d'une voyelle
    "PREP_DE_VOY": [
        "d'"
    ],

    # Préposition 'de' suivie d'une consonne
    "PREP_DE_CON": [
        "de"
    ],

    # Syntagme prépositionnel introduit par 'à'
    "SP_DE": [
        ["PREP_DE_VOY", "SN_SNG_MASC"],
        ["PREP_DE_VOY", "SN_SNG_FEM"],
        ["PREP_DE_CON", "NOM_PLU_MASC_VOY"],
        ["PREP_DE_CON", "NOM_PLU_FEM_VOY"],
        ["PREP_DE_CON", "SN_PLU_MASC_NOMBRES"],
        ["PREP_DE_CON", "SN_PLU_FEM_NOMBRES"]
    ],

    # Règles de haut niveau qui génèrent les histoires
    "AVENTURES": [
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_IMP_SNG", "SN", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_IMP_SNG", "SN", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_IMP_SNG", "SN", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_IMP_SNG", "SN", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_IMP_SNG", "SN", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_IMP_SNG", "SN", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_IMP_SNG", "SN", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_IMP_SNG", "SN", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_A_SNG", "SP_A", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_IMP_DE_SNG", "SP_DE", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_IMP_SNG", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_IMP_SNG", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_IMP_SNG", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_IMP_SNG", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_IMP_SNG", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_IMP_SNG", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_IMP_SNG", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_IMP_SNG", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_PQP_SNG", "SN", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_PQP_SNG", "SN", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_PQP_SNG", "SN", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTD_PQP_SNG", "SN", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_PQP_SNG", "SN", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_PQP_SNG", "SN", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_PQP_SNG", "SN", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTD_PQP_SNG", "SN", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_A_SNG", "SP_A", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VTI_PQP_DE_SNG", "SP_DE", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_PQP_SNG", ". Un jour, il", "VTD_PAS_SNG", "SN", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_PQP_SNG", ". Un jour, il", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_PQP_SNG", ". Un jour, il", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_MASC"],
        ["INTRO_SNG", "SN_SNG_MASC", "qui", "VIT_PQP_SNG", ". Un jour, il", "VIT_PAS_SNG", "FIN_SNG_MASC"],

        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_PQP_SNG", ". Un jour, elle", "VTD_PAS_SNG", "SN", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_PQP_SNG", ". Un jour, elle", "VTI_PAS_A_SNG", "SP_A", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_PQP_SNG", ". Un jour, elle", "VTI_PAS_DE_SNG", "SP_DE", "FIN_SNG_FEM"],
        ["INTRO_SNG", "SN_SNG_FEM", "qui", "VIT_PQP_SNG", ". Un jour, elle", "VIT_PAS_SNG", "FIN_SNG_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_VOY", "SN_PLU_MASC_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_VOY", "SN_PLU_FEM_NO_ART_VOY", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_IMP_PLU", "SN", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_A_PLU", "SP_A", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_IMP_DE_PLU", "SP_DE", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_IMP_PLU", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTD_PQP_PLU", "SN", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_A_PLU", "SP_A", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VTI_PQP_DE_PLU", "SP_DE", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"],

        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTD_PAS_PLU", "SN", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_MASC"],
        ["INTRO_PLU_CON", "SN_PLU_MASC_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, ils", "VIT_PAS_PLU", "FIN_PLU_MASC"],

        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTD_PAS_PLU", "SN", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTI_PAS_A_PLU", "SP_A", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VTI_PAS_DE_PLU", "SP_DE", "FIN_PLU_FEM"],
        ["INTRO_PLU_CON", "SN_PLU_FEM_NO_ART_CON", "qui", "VIT_PQP_PLU", ". Un jour, elles", "VIT_PAS_PLU", "FIN_PLU_FEM"]
    ]

}


# Moulinettes
# ==============================================================================

# Génération d'une histoire
# ------------------------------------------------------------------------------

def generation(grammaire, regle):
    '''
    Génère une histoire à partir de la grammaire

    Parametres
    ----------
    grammaire: dict
               Grammaire contenant les regles a suivre
    regle: string
           Regle contenue dans la grammaire

    Retourne
    --------
    regle: string
           Regle contenue dans la grammaire
    texte: string
           Texte final apres parcours de toutes les regles
    '''

    if isinstance(regle, list):
        regles = (generation(grammaire, p) for p in regle)
        texte = " ".join(p for p in regles if p)
        return texte
    elif regle in grammaire:
        return generation(grammaire, random.choice(grammaire[regle]))
    else:
        return regle


# Corrections éventuelles pour que le texte paraisse naturel
# ------------------------------------------------------------------------------

def corrections(texte):
    '''
    Corrections typographiques sur l'histoire

    Parametres
    ----------
    texte: string
           Texte issu des regles de la grammaire

    Retourne
    --------
    histoire: string
              Histoire corrigee et prete a etre affichee
    '''

    texte = re.sub("' ", "'", texte)
    texte = re.sub(" ,", ",", texte)
    texte = re.sub(r" \.", ".", texte)
    texte = re.sub(r"$", ".", texte)

    tokens = list(texte)
    tokens[0] = tokens[0].capitalize()

    histoire = ''.join(tokens)

    return histoire.encode()


# Lancement
# ------------------------------------------------------------------------------

def lancement():
    '''
    Fonction d'exécution des histoires

    Retourne
    --------
    histoire: string
              Histoire corrigee et prete a etre affichee
    '''

    texte = generation(HISTOIRES, "AVENTURES")
    histoire = corrections(texte)
    return histoire


# Communication avec Arduino
# ==============================================================================

try:
    while True:
        data = arduino.read()
        if int.from_bytes(data, "big"):
            arduino.write(lancement())
except:
    print("Une erreur s'est produite.")
