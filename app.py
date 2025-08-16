from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# =======================
# Load environment variables
# =======================
load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
PORT = int(os.getenv("PORT", 5000))

# =======================
# Initialize Flask app
# =======================
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, origins=(['*', 'http://localhost:3000']))
app.secret_key = SECRET_KEY

# =======================
# Flask-Mail setup
# =======================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = ('ARC Website', MAIL_USERNAME)

mail = Mail(app)

# =======================
# Routes
# =======================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions."""
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    details = request.form.get("details")

    # Nicely formatted email
    body = f"""
📩 New Quote Request from ARC Website

👤 Name: {name}
📧 Email: {email}
📞 Phone: {phone}

📝 Project Details:
{details}
"""

    try:
        if MAIL_USERNAME == "dummy@example.com" or MAIL_PASSWORD == "dummy":
            # Test mode: print to console instead of sending
            print("=== Contact Form Submission ===")
            print(body)
            flash("✅ Form submitted! (Email not sent in test mode)", "success")
        else:
            msg = Message(
                subject=f"New Quote Request from {name}",
                recipients=[RECIPIENT_EMAIL],
                body=body
            )
            mail.send(msg)
            flash("✅ Thank you! Your request has been submitted.", "success")

    except Exception as e:
        print("❌ Error sending email:", e)
        flash("⚠️ Something went wrong. Please try again later.", "error")

    return redirect(url_for('index'))


# =======================
# Run server
# =======================
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=PORT, debug=True)
