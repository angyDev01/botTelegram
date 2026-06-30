#Création de bot telegrame
import os 
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import datetime
import random
import json

load_dotenv()

token = os.getenv('TOKEN_BOT')
chat_id = int(os.getenv('CHANNEL_ID'))

#

async def start(update, context):
    user = update.message.from_user
    await update.message.reply_text(f"""
👋 Bienvenue sur DailyPub ! 🐍
    {user.first_name}, je suis ton assistant automatisé dédié à l'univers Python.
    Chaque jour, je diffuse des astuces, des tutoriels et des snippets pour t'aider à mieux coder.

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
    keyboard = [
        [InlineKeyboardButton("Contactez mon developpeur", url="https://t.me/@Angy_Dev")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

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
Si tu rencontres un bug ou que tu as une idée de tutoriel à proposer, n'hésite pas à contacter mon créateur.
    """, reply_markup=reply_markup, parse_mode="Markdown")


#Developpement de la commande /about

async def about(update, context):
    text = """
🤖 **À propos de DailyPub**

Ce bot Telegram a été conçu pour t'accompagner dans ton apprentissage de la programmation Python.

🔹 **Technologie :** Python & python-telegram-bot.
🔹 **Hébergement :** Railway.
🔹 **Version :** v1.2

Clique sur le bouton ci-dessous pour voir le code source sur GitHub :
    """
    
    # Création du bouton
    keyboard = [
        [InlineKeyboardButton("Voir le code sur GitHub 📂", url="https://github.com/angyDev01/botTelegram")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Envoi du message avec le bouton
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")



#commande pour envoyer la publication quotidienne
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Charger les données du fichier JSON
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        await update.message.reply_text("Erreur : Le fichier data.json est introuvable.")
        return

    # 2. Choisir une astuce au hasard
    post = random.choice(data)
    
    # 3. Créer les boutons interactifs
    keyboard = [
        [InlineKeyboardButton("🔗 Lire la source", url=post['url'])],
        [InlineKeyboardButton("👍 J'aime", callback_data='like')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 4. Envoyer sur la chaîne configurée
    try:
        # On utilise ton CHANNEL_ID configuré dans main()
        await context.bot.send_message(
            chat_id=chat_id, 
            text=f"💡 **{post['title']}**\n\n{post['content']}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        # Confirmation à l'utilisateur qui a tapé la commande
        await update.message.reply_text("✅ Publication envoyée avec succès sur la chaîne !")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l'envoi : {e}")


#script pour gérer le clic sur le bouton "J'aime"

# Configuration des chemins pour le stockage persistant
DATA_DIR = '/app/data'
LIKES_FILE = os.path.join(DATA_DIR, 'likes.json')

# S'assurer que le dossier de stockage existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Récupération de l'ID du canal depuis les variables d'environnement
CHANNEL_ID = os.getenv("CHANNEL_ID")
TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Fonctions de gestion des Likes ---

def load_likes():
    """Charge les likes depuis le fichier JSON persistant."""
    if not os.path.exists(LIKES_FILE):
        return {}
    with open(LIKES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_likes(data):
    """Sauvegarde les likes dans le fichier JSON."""
    with open(LIKES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère le clic sur le bouton 'J'aime'."""
    query = update.callback_query
    await query.answer()

    message_id = str(query.message.message_id)
    likes_data = load_likes()
    
    # Incrémentation
    likes_data[message_id] = likes_data.get(message_id, 0) + 1
    save_likes(likes_data)
    
    count = likes_data[message_id]
    
    # Mise à jour du message
    original_text = query.message.text.split("\n\n❤️")[0]
    new_text = f"{original_text}\n\n❤️ {count} personne{'s' if count > 1 else ''} a/ont aimé cette astuce !"
    
    await query.edit_message_text(
        text=new_text, 
        reply_markup=query.message.reply_markup,
        parse_mode="Markdown"
    )


#Script pour envoyer la publication quotidienne à 09h00 chaque jour
def main():
    # 1. Je crées l'application avec mon token donné par BotFather
    application = Application.builder().token(token).build()

    # 2. ajout des commandes (ici, on relie la commande /start à ta fonction start)
    application.add_handler(CommandHandler("start", start)) #commande /start
    application.add_handler(CommandHandler("help", help))   #commande /help
    application.add_handler(CommandHandler("about", about)) #commande /about
    application.add_handler(CommandHandler("daily", daily)) #commande /daily
    application.add_handler(CallbackQueryHandler(button_click)) #gestion du clic sur le bouton "J'aime"

    # 3. Je lance le bot en mode "écoute continue"
    print("🤖 Démarrage de DailyPub...")
    
    # Programmer la publication à 09h00 chaque jour
    job_queue = application.job_queue
    job_queue.run_daily(daily, time=datetime.time(hour=3, minute=50))
    
    application.run_polling()

# --- Le bloc principal pour démarrer le bot ---
if __name__ == '__main__':
    main()