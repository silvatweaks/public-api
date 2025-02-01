from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Token do bot do Discord (coloque o seu aqui)
DISCORD_BOT_TOKEN = "MTMzNTA0MzI3Nzg4MzE3OTExMQ.GtDAcz.Ri3npx-8mr0gGmk0PM4LlcBrpNCZVm4BoDorag"
HEADERS = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

DISCORD_API_BASE = "https://discord.com/api/v10"

def get_user_data(user_id):
    url = f"{DISCORD_API_BASE}/users/{user_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        user = response.json()
        avatar_url = (
            f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.{'gif' if user['avatar'].startswith('a_') else 'png'}?size=512"
            if user.get("avatar")
            else "https://cdn.discordapp.com/embed/avatars/1.png"
        )
        return {
            "id": user["id"],
            "username": user["username"],
            "display_name": user.get("global_name", user["username"]),
            "avatar": avatar_url,
        }
    return None

@app.route("/user/<user_id>")
def get_user(user_id):
    data = get_user_data(user_id)
    if data:
        return jsonify(data)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
