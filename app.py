from flask import Flask, request, jsonify
from flask_cors import CORS
from reply_drafter import draft_reply
from critic_agent import critique_reply
from reply_reviser import revise_reply
from reply_sender import send_email
from email_reader import fetch_unread_emails

app = Flask(__name__)
CORS(app)

@app.route('/api/email/latest', methods=['GET'])
def get_latest_email():
    email_data = fetch_unread_emails()
    return jsonify(email_data)

@app.route('/api/reply/revise_final', methods=['POST'])
def generate_final_reply():
    data = request.get_json()
    email_body = data.get('email_body')
    draft = draft_reply(email_body)
    critique = critique_reply(email_body, draft)
    revised = revise_reply(draft, critique)
    return jsonify({'revised': revised})

@app.route('/api/reply/send', methods=['POST'])
def send():
    data = request.get_json()
    email_body = data.get('email_body')
    reply_text = data.get('message_body')

    send_email(email_body, reply_text)
    return jsonify({'message': 'Email sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)
