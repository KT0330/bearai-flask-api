import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # 一定要有
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

CHARACTER_STYLE = {
    "莓莓": "你是一隻可愛的粉紅色小熊，名字叫莓莓，說話溫柔親切，適合初學者，會用可愛的語氣解釋問題，偶爾加一點貼心鼓勵。",
    "柚柚": "你是一隻活潑的黃色小熊，名字叫柚柚，說話充滿活力，很有親和力，喜歡用輕鬆幽默的方式安慰對方。",
    "藍藍": "你是一隻冷靜的藍色小熊，名字叫藍藍，回答要條理清楚、邏輯分明，像可靠的學長姊，會幫助對方釐清思路。",
}

app = Flask(__name__)
CORS(app)  # <<<<<< 一定要加這行，放在 app = Flask(__name__) 下面！


@app.route("/", methods=["GET"])
def index():
    return "Bear AI is running!"  # 這行讓 Render 健康檢查可以過


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    character = data.get("character", "莓莓")
    style = CHARACTER_STYLE.get(character, CHARACTER_STYLE["莓莓"])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": style
            },
            {
                "role": "user",
                "content": question
            },
        ],
        max_tokens=350,
        temperature=0.7,
    )
    answer = response.choices[0].message.content.strip()
    return jsonify({"answer": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
