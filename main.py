#Création de bot telegrame
import os 
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

token = os.getenv('TOKEN_BOT')

#

async def start(update, context):
    await update.message.reply_text("""
👋 Bienvenue sur DailyPub ! 🐍

Je suis ton assistant automatisé dédié à l'univers Python. Chaque jour, je diffuse des astuces, des tutoriels et des snippets pour t'aider à mieux coder.

Voici les commandes que tu peux utiliser pour interagir avec moi :

📌 **Commandes générales**
/start - Afficher ce message de bienvenue
/help - Comment utiliser le bot et contacter l'admin
/about - En savoir plus sur DailyPub et la confidentialité

💻 **Exploration du contenu**
/daily - Recevoir la publication ou l'astuce du jour
/random - Afficher un bout de code (snippet) au hasard
/categories - Voir les thèmes couverts (Django, Data Science, Scripts...)
/search <mot-clé> - Chercher une publication spécifique

🔔 **Gestion des alertes**
/subscribe - T'abonner pour recevoir les nouveautés en message privé
/unsubscribe - Arrêter les notifications privées

Tape une de ces commandes pour commencer ! 🚀
    """)

#developpement de la commande d'aide

async def help(update, context):
    await update.message.reply_text("""
🆘 **Centre d'aide DailyPub** 🐍

Ce bot est conçu pour t'aider à progresser en Python avec du contenu quotidien. Voici comment interagir avec moi :

📖 **Comment ça marche ?**
Je publie automatiquement des astuces et des tutoriels sur le canal principal. Mais tu peux aussi me demander du contenu directement ici, en message privé !

🛠 **Liste de mes commandes :**
• /daily : Affiche l'astuce ou le tutoriel d'aujourd'hui.
• /random : Envoie un snippet de code Python aléatoire pour t'entraîner.
• /categories : Affiche les thèmes disponibles (Django, Data Science, Bases, etc.).
• /search <mot-clé> : Cherche une publication précise (ex: tape "/search boucle" ou "/search fastapi").
• /subscribe : Abonne-toi pour recevoir mes publications en message privé.
• /unsubscribe : Arrête les envois en message privé.
• /about : Affiche les infos du bot et la politique de confidentialité.

👨‍💻 **Un problème ou une suggestion ?**
Si tu rencontres un bug ou que tu as une idée de tutoriel à proposer, n'hésite pas à contacter mon créateur :@Angy_Dev.
    """)


#Developpement de la commande /about

async def about(update, context):
    text = """
🤖 **À propos de DailyPub**

Ce bot Telegram a été conçu pour t'accompagner dans ton apprentissage de la programmation Python.

🔹 **Technologie :** Python & python-telegram-bot.
🔹 **Hébergement :** Railway.

Clique sur le bouton ci-dessous pour voir le code source sur GitHub :
    """
    
    # Création du bouton
    keyboard = [
        [InlineKeyboardButton("Voir le code sur GitHub 📂", url="https://github.com/angyDev01/botTelegram")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Envoi du message avec le bouton
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# --- Le bloc principal pour démarrer le bot ---
if __name__ == '__main__':
    # 1. Je crées l'application avec mon token donné par BotFather
    application = Application.builder().token(token).build()

    # 2. ajout des commandes (ici, on relie la commande /start à ta fonction start)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("about", about))
    # 3. Je lance le bot en mode "écoute continue"
    print("🤖 Démarrage de DailyPub...")
    application.run_polling()