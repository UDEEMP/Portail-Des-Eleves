#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import random
from os.path import expanduser
from getpass import getpass

def createEnv():
    print("Où voulez-vous installer l'environnement virtuel ? [defaut: ~/@django/]")
    env = input()
    if env is "":
        env = "~/@django/"
    env = expanduser(env)
    if not env[-1] == "/":
        env += "/"
    p = subprocess.Popen([sys.executable, "-m", "venv", env], shell=False)
    retval = p.wait()
    if retval != 0:
        print("Impossible d'installer l'environnement virtuel")
        exit(-1)
    print("Environnement virtuel installé")
    python = env + "bin/python"
    pip = env + "bin/pip"
    requirements = os.path.dirname(os.path.realpath(__file__)) + "/requirements.txt"
    p = subprocess.Popen([pip, 'install', '-r', requirements])
    p.wait();
    if retval != 0:
        print("Impossible d'installer les différents packets")
        exit(-1)
    ##WALLAH TOUT EST INSTALLÉ
    return env

def editSettings():
    template = os.path.dirname(os.path.realpath(__file__)) + "/portail/settings.py.template"
    settings = os.path.dirname(os.path.realpath(__file__)) + "/portail/settings.py"
    try:
        f = open(template, 'r')
        f2 = open(settings, 'w')
    except Exception :
        print("Chelou le fichier /portail/settings.py.template n'existe pas :/")
        exit(-1)
    SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    INTRANET_SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(32)])
    YEARBOOK_SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(16)])
    NAME = input("Nom de la BDD: ")
    USER = input("Nom d'utilisateur (root en localhost): ")
    PASSWORD = getpass("Mot de passe: ")
    HOST = input("Host (vide en localhost): ")
    PORT = input("Port (vide par défaut): ")
    for line in f:
        line = line.replace("{%%SECRET_KEY%%}", SECRET_KEY)
        line = line.replace("{%%INTRANET_SECRET_KEY%%}", INTRANET_SECRET_KEY)
        line = line.replace("{%%YEARBOOK_SECRET_KEY%%}", YEARBOOK_SECRET_KEY)
        line = line.replace("{%%NAME%%}", NAME)
        line = line.replace("{%%USER%%}", USER)
        line = line.replace("{%%PASSWORD%%}", PASSWORD)
        line = line.replace("{%%HOST%%}", HOST)
        line = line.replace("{%%PORT%%}", PORT)
        f2.write(line)
    f.close()
    f2.close()


if __name__ == '__main__':
    try :
        p = subprocess.Popen([sys.executable, "--version"] , shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        v = str(p.stdout.readlines()[0])[2:-3].replace("Python ", "").split(".")
        if (int(v[0]), int(v[1])) != (3,5):
            print("Veuillez relancer le script avec Python 3.5")
            exit(-1)
    except Exception :
        print("Veuillez relancer le script avec Python 3.5")
        exit(-1)
    editSettings()
    env = createEnv()
    print("Terminé")
    print("Vous pouvez ajouter l'alias @django='source " + env + "bin/activate'")
    print("Une fois dans l'environnement virtuel et dans le dossier du portail")
    print("  python manage.py runserver  ")
    print("Pour démarrer le serveur")
