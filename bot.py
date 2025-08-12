# bot.py

from utils import clear_console, colored_text
from instagram_manager import (
    login_instagram,
    recover_accounts,
    list_accounts,
    delete_account,
    show_trash
)
from telegram_bot import start_telegram_bot
import time

def main_menu():
    while True:
        clear_console()
        print(colored_text("=== SMMKingdomTask Bot - Menu Principal ===", "cyan"))
        print(colored_text("""
[1] Se connecter à un compte Instagram
[2] Récupérer les comptes
[3] Se connecter aux comptes
[4] Déconnexion T/6
[5] Liste des comptes
[6] Supprimer un compte
[7] Corbeille
[8] Générer User-Agent
[9] Récupérer ma clé
[10] Mettre à jour l'Outil
[11] Démarrer Bot Telegram
[0] Quitter
        """, "yellow"))

        choice = input(colored_text("Choix ➤ ", "green")).strip()

        if choice == '1':
            login_instagram()
        elif choice == '2':
            recover_accounts()
        elif choice == '3':
            print("Connexion multiple aux comptes (non implémentée)...")
        elif choice == '4':
            print("Déconnexion T/6 (non implémentée)...")
        elif choice == '5':
            list_accounts()
        elif choice == '6':
            delete_account()
        elif choice == '7':
            show_trash()
        elif choice == '8':
            print("Génération User-Agent (en développement)...")
        elif choice == '9':
            print("Système de clé (bientôt)...")
        elif choice == '10':
            print("Mise à jour de l’outil...")
        elif choice == '11':
            start_telegram_bot()
        elif choice == '0':
            print("Fermeture...")
            break
        else:
            print("Choix invalide...")
        time.sleep(2)

if __name__ == "__main__":
    main_menu()

