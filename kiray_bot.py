import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

# ============================================
# ⚙️ CONFIG — Token እና Channel ስም ቀይር
# ============================================
BOT_TOKEN = "8874025247:AAHRmOD4o-yFsCsu8U4_4mL0O6JAdWseJO8"  # ← Bot Token ይህ ቦታ ላይ ቀይር
CHANNEL_ID = "@KirayGebeyaET"      # ← Channel username
ADMIN_ID = 434846475               # ← Admin Chat ID
TELEBIRR_NUMBER = "0909837397"     # ← Telebirr ቁጥር
LISTING_FEE = 100                  # ← Listing fee (ብር)

# ============================================
# ደረጃዎች
# ============================================
(PAYMENT, KIRAY, AYNET, METEN, FOK, WELEL, SEFERI, MENGED, TIMHIRT,
 UHA, TANKER, MEBRAT, MABESYA, SHOWER, MEKINA, LEMAN,
 AKERAY, SILKI, PHOTO) = range(19)

logging.basicConfig(level=logging.INFO)

# Code counter (ለ CODE BT XXXX)
import random

def generate_code():
    return f"BT {random.randint(1000, 9999)}"

# ============================================
# START
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 እንኳን ደህና መጡ!\n\n"
        "🏠 *KirayGebeya ET* — ቤትዎን ለማስተዋወቅ እንረዳዎታለን!\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "💳 *የምዝገባ ክፍያ: 100 ብር*\n\n"
        "📱 Telebirr: *0909837397*\n\n"
        "1. 100 ብር ወደ 0909837397 ላኩ\n"
        "2. የክፍያ screenshot ወይም transaction ID ይላኩ\n\n"
        "ክፍያ ሲረጋገጥ ቤትዎ ይለጠፋል! ✅",
        parse_mode="Markdown"
    )
    return PAYMENT


# ============================================
# ክፍያ ማረጋገጫ
# ============================================
async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Accept photo screenshot or text transaction ID
    if update.message.photo:
        payment_proof = update.message.photo[-1].file_id
        context.user_data['payment_proof'] = payment_proof
        proof_type = "screenshot"
    else:
        context.user_data['payment_proof'] = update.message.text
        proof_type = "text"

    user = update.message.from_user
    username = f"@{user.username}" if user.username else str(user.id)

    # Notify admin for verification
    keyboard = ReplyKeyboardMarkup(
        [[f"✅ አረጋግጥ {user.id}", f"❌ አትቀበል {user.id}"]],
        one_time_keyboard=True
    )
    
    admin_msg = (
        f"💳 አዲስ ክፍያ ደረሰ!\n\n"
        f"👤 ተጠቃሚ: {username}\n"
        f"💰 100 ብር\n"
        f"📋 ማስረጃ: {proof_type}\n\n"
        f"✅ ለማረጋገጥ: /approve_{user.id}\n"
        f"❌ ለመሰረዝ: /reject_{user.id}"
    )
    
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=payment_proof,
            caption=admin_msg
        )
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)

    context.user_data['user_id'] = user.id
    context.user_data['chat_id'] = update.message.chat_id

    await update.message.reply_text(
        "✅ ክፍያዎ ተቀብሏል!\n\n"
        "⏳ እየተረጋገጠ ነው — ትንሽ ይጠብቁ...\n\n"
        "ሲረጋገጥ ጥያቄዎቹን እንጀምራለን!"
    )
    return ConversationHandler.END

# ============================================
# ጥያቄ 1 — ኪራይ ዋጋ
# ============================================
async def get_kiray(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['kiray'] = update.message.text
    keyboard = [["1 ክፍል", "2 ክፍል"], ["3 ክፍል", "ቪላ"], ["ሱቅ/ቢሮ", "ሌላ"]]
    await update.message.reply_text(
        "✅ ዋጋ ተመዝግቧል!\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "🏠 *የቤት አይነት ምንድን ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return AYNET

# ============================================
# ጥያቄ 2 — አይነት
# ============================================
async def get_aynet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['aynet'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "📐 *የቤቱ መጠን ስንት ነው?*\n"
        "_(ምሳሌ: 5X5፣ 4X6)_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return METEN

# ============================================
# ጥያቄ 3 — መጠን
# ============================================
async def get_meten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['meten'] = update.message.text
    keyboard = [["መሬት ወለል", "1ኛ ፎቅ"], ["2ኛ ፎቅ", "3ኛ ፎቅ"], ["4ኛ ፎቅ+", "ሌላ"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🏗️ *የትኛው ፎቅ ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return FOK

# ============================================
# ጥያቄ 4 — ፎቅ
# ============================================
async def get_fok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fok'] = update.message.text
    keyboard = [["ሴራሚክ", "ፓርኬ"], ["ሲሚንቶ", "ሌላ"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🪟 *ወለሉ ምን አይነት ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return WELEL

# ============================================
# ጥያቄ 5 — ወለል
# ============================================
async def get_welel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['welel'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "📍 *ሰፈሩ የት ነው?*\n"
        "_(ምሳሌ: ገርጂ - የረር አለማየሁ)_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return SEFERI

# ============================================
# ጥያቄ 6 — ሰፈር
# ============================================
async def get_seferi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['seferi'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🚕 *ከዋና መንገድ ምን ያህል ቅርብ ነው?*\n"
        "_(ምሳሌ: ከቦሌ 1 ታክሲ 20 ብር)_",
        parse_mode="Markdown"
    )
    return MENGED

# ============================================
# ጥያቄ 7 — ከዋና መንገድ
# ============================================
async def get_menged(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['menged'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🏫 *አቅራቢያ ያሉ ትምህርት ቤቶች/ዩኒቨርሲቲዎች?*\n"
        "_(ምሳሌ: Unity University, Ethio-Parents School)_\n"
        "_ከሌለ 'የለም' ብለው ይላኩ_",
        parse_mode="Markdown"
    )
    return TIMHIRT

# ============================================
# ጥያቄ 8 — ትምህርት ቤት
# ============================================
async def get_timhirt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['timhirt'] = update.message.text
    keyboard = [["ሁልጊዜ አለ", "በሳምንት 2/3 ቀን"], ["አልፎ አልፎ", "የለም"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "💧 *ውሃ እንዴት ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return UHA

# ============================================
# ጥያቄ 9 — ውሃ
# ============================================
async def get_uha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['uha'] = update.message.text
    keyboard = [["አለ ✅", "የለም ❌"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🚰 *ታንከር አለ?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return TANKER

# ============================================
# ጥያቄ 10 — ታንከር
# ============================================
async def get_tanker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tanker'] = update.message.text
    keyboard = [["እንደሌላው አካባቢ", "ብዙ ጊዜ አለ"], ["አልፎ አልፎ ይጠፋል"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "⚡ *መብራት እንዴት ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MEBRAT

# ============================================
# ጥያቄ 11 — መብራት
# ============================================
async def get_mebrat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mebrat'] = update.message.text
    keyboard = [["አለ ✅", "የለም ❌"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🍳 *ማብሰያ ክፍል አለ?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MABESYA

# ============================================
# ጥያቄ 12 — ማብሰያ
# ============================================
async def get_mabesya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mabesya'] = update.message.text
    keyboard = [["ብቻዬን ✅", "ከ1 ክፍል ጋር የጋራ"], ["ከ2+ ክፍል ጋር የጋራ"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🚿 *ሻወር/ሽንት ቤት እንዴት ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return SHOWER

# ============================================
# ጥያቄ 13 — ሻወር
# ============================================
async def get_shower(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shower'] = update.message.text
    keyboard = [["አለ ✅", "የለም ❌"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🚗 *መኪና ማቆሚያ አለ?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MEKINA

# ============================================
# ጥያቄ 14 — መኪና ማቆሚያ
# ============================================
async def get_mekina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mekina'] = update.message.text
    keyboard = [["ለላጤ", "ለባለትዳር"], ["ለሁለቱም ✅"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "👨‍👩‍👧 *ቤቱ ለማን ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return LEMAN

# ============================================
# ጥያቄ 15 — ለማን
# ============================================
async def get_leman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['leman'] = update.message.text
    keyboard = [["አከራዩ ግቢ ውስጥ የለም ✅", "አከራዩ ግቢ ውስጥ አለ"]]
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "🏘️ *አከራዩ ግቢ ውስጥ ነው?*",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return AKERAY

# ============================================
# ጥያቄ 16 — አከራይ
# ============================================
async def get_akeray(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['akeray'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "📞 *የስልክ ቁጥርዎ ምንድን ነው?*\n"
        "_(ምሳሌ: 0911234567)_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return SILKI

# ============================================
# ጥያቄ 17 — ስልክ
# ============================================
async def get_silki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['silki'] = update.message.text
    await update.message.reply_text(
        "✅\n\n━━━━━━━━━━━━━━━━\n"
        "📸 *የቤቱን ፎቶ ይላኩ!*\n"
        "_(እስከ 5 ፎቶ መላክ ይቻላል)_",
        parse_mode="Markdown"
    )
    context.user_data['photos'] = []
    return PHOTO

# ============================================
# ጥያቄ 18 — ፎቶ
# ============================================
async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_id = update.message.photo[-1].file_id
        context.user_data['photos'].append(photo_id)

        if len(context.user_data['photos']) < 5:
            await update.message.reply_text(
                f"✅ ፎቶ {len(context.user_data['photos'])} ተቀብሏል!\n"
                "📸 ሌላ ፎቶ ይላኩ ወይም /done ብለው ይጨርሱ"
            )
            return PHOTO
        else:
            return await post_to_channel(update, context)
    elif update.message.text and update.message.text == "/done":
        if context.user_data['photos']:
            return await post_to_channel(update, context)
        else:
            await update.message.reply_text("⚠️ ቢያንስ 1 ፎቶ ይላኩ!")
            return PHOTO

# ============================================
# Channel ላይ Post አድርግ
# ============================================
async def post_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = context.user_data
    code = generate_code()

    # Format text
    mabesya = "አለ ✅" if "አለ" in d.get('mabesya','') else "የለም ❌"
    tanker = "አለ ✅" if "አለ" in d.get('tanker','') else "የለም ❌"
    mekina = "አለ ✅" if "አለ" in d.get('mekina','') else "የለም ❌"

    caption = (
        f"🔥 የሚከራይ {d.get('aynet','')} 🔥\n"
        f"▫️ CODE {code}\n\n"
        f"🟢 ኪራይ፡ {d.get('kiray','')}\n"
        f"🟢 {d.get('aynet','')} ({d.get('meten','')}፣ {d.get('welel','')} ወለል፣ {d.get('fok','')})\n"
        f"🟢 ሰፈሩ፡ {d.get('seferi','')}\n"
        f"🟢 {d.get('menged','')}\n"
    )

    if d.get('timhirt','') and d.get('timhirt') != 'የለም':
        caption += f"🟢 ትምህርት ቤት፡ {d.get('timhirt','')}\n"

    caption += (
        f"🟢 ውሃ፡ {d.get('uha','')}\n"
        f"🟢 ታንከር፡ {tanker}\n"
        f"🟢 መብራት፡ {d.get('mebrat','')}\n"
        f"🟢 ማብሰያ ክፍል፡ {mabesya}\n"
        f"🟢 ሻወር/ሽንት ቤት፡ {d.get('shower','')}\n"
        f"🟢 መኪና ማቆሚያ፡ {mekina}\n"
        f"🟢 {d.get('leman','')}\n"
        f"🟢 {d.get('akeray','')}\n\n"
        f"📞 ለመጠይቅ፡ @JR_ErmiDo\n\n"
        f"🏠 @KirayGebeyaET"
    )

    photos = d.get('photos', [])

    try:
        if len(photos) == 1:
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photos[0],
                caption=caption
            )
        elif len(photos) > 1:
            from telegram import InputMediaPhoto
            media = [InputMediaPhoto(media=p) for p in photos]
            media[0] = InputMediaPhoto(media=photos[0], caption=caption)
            await context.bot.send_media_group(chat_id=CHANNEL_ID, media=media)

        await update.message.reply_text(
            f"🎉 ተሳካ!\n\n"
            f"✅ ቤትዎ @KirayGebeyaET ላይ ተለጠፈ!\n"
            f"🔑 CODE፡ {code}\n\n"
            "ሌላ ቤት ለማስተዋወቅ /start ይላኩ"
        )

        # Admin notification
        admin_msg = (
            f"🔔 አዲስ ቤት ተለጠፈ!\n\n"
            f"🏠 {d.get('aynet','')} — {d.get('seferi','')}\n"
            f"💰 {d.get('kiray','')}\n"
            f"📞 {d.get('silki','')}\n"
            f"🔑 CODE: {code}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)

    except Exception as e:
        await update.message.reply_text(f"❌ ስህተት ተፈጠረ: {e}")

    context.user_data.clear()
    return ConversationHandler.END

# ============================================
# Cancel
# ============================================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ ተሰርዟል። እንደገና ለመጀመር /start ይላኩ",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# ============================================
# Admin Approve/Reject
# ============================================
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(context.args[0]) if context.args else int(update.message.text.split("_")[1])
    except:
        await update.message.reply_text("❌ User ID አልተገኘም")
        return

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "✅ ክፍያዎ ተረጋግጧል!\n\n"
            "አሁን ቤትዎን እናስተዋውቅ — /start ይላኩ 🏠"
        )
    )
    await update.message.reply_text(f"✅ User {user_id} approved!")

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(context.args[0]) if context.args else int(update.message.text.split("_")[1])
    except:
        await update.message.reply_text("❌ User ID አልተገኘም")
        return

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "❌ ክፍያዎ አልተረጋገጠም\n\n"
            "እባክዎ እንደገና ይሞክሩ ወይም @KirayGebeyaET ያግኙን"
        )
    )
    await update.message.reply_text(f"❌ User {user_id} rejected!")

# ============================================
# MAIN
# ============================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PAYMENT: [MessageHandler(filters.TEXT | filters.PHOTO, get_payment)],
            KIRAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_kiray)],
            AYNET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_aynet)],
            METEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_meten)],
            FOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fok)],
            WELEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_welel)],
            SEFERI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_seferi)],
            MENGED: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_menged)],
            TIMHIRT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_timhirt)],
            UHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_uha)],
            TANKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tanker)],
            MEBRAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mebrat)],
            MABESYA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mabesya)],
            SHOWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_shower)],
            MEKINA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mekina)],
            LEMAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_leman)],
            AKERAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_akeray)],
            SILKI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_silki)],
            PHOTO: [
                MessageHandler(filters.PHOTO, get_photo),
                CommandHandler("done", get_photo)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
    print("🤖 KirayGebeya Bot እየሰራ ነው...")
    app.run_polling()

if __name__ == "__main__":
    main()
