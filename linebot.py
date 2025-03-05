from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent

import os

app = Flask(__name__)

# 從環境變數讀取 Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("lmzbrx+uf0CA0b6/xCrNVDrPxkqmc6IZHGyA97UKz9D9GRJSe2KXsGxML8jcMV32Xby2FMYdktTM4/uwbi2U6+VxyJ4ERiSverSTnhrkbL9Vzl8pV8CI5Tjmqi6LvAmDWLmgsHvYQaVbhYytcxEuzQdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("8b3d98b1778b1cc862574f22f0d24e35")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

# 🔹 功能 1：歡迎新成員並 @tag
@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    new_member_id = event.joined.members[0].user_id
    welcome_message = f"@{new_member_id}\n新成員你好，進來請先看記事本的群規須知。\n也可以看看記事本與相簿裡的攻略熟悉一下。\n若已有帳號，請將遊戲名片放入相簿裡。"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

# 🔹 功能 2：偵測關鍵字「請問」並回覆
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if "請問" in user_message:
        reply_message = "請善用搜尋\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
