from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent, Mention

import os

app = Flask(__name__)

# LINE 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("lmzbrx+uf0CA0b6/xCrNVDrPxkqmc6IZHGyA97UKz9D9GRJSe2KXsGxML8jcMV32Xby2FMYdktTM4/uwbi2U6+VxyJ4ERiSverSTnhrkbL9Vzl8pV8CI5Tjmqi6LvAmDWLmgsHvYQaVbhYytcxEuzQdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("8b3d98b1778b1cc862574f22f0d24e35")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    # 獲取 LINE 傳來的 HTTP 請求內容
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# **當新成員加入時，標註新成員並發送歡迎訊息**
@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    try:
        new_member = event.joined.members[0].user_id  # 取得新成員的 User ID
        group_id = event.source.group_id  # 取得群組 ID
        mention = Mention(user_id=new_member)  # 創建 Mention 標註

        welcome_text = (
            f"@{mention.user_id}\n"
            "新成員你好，進來請先看記事本的群規須知。\n"
            "也可以看看記事本與相簿裡的攻略熟悉一下。\n"
            "若已有帳號，請將遊戲名片放入相簿裡。"
        )

        line_bot_api.push_message(group_id, TextSendMessage(text=welcome_text, mention=[mention]))

    except Exception as e:
        print(f"發送歡迎訊息時出錯: {e}")

# **當有人說「請問」時，自動回覆**
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text  # 取得使用者訊息

    if "請問" in user_message:
        reply_text = "請善用搜尋\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
