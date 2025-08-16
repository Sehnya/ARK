from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_mail import Mail, Message
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, origins=(['*', 'http://localhost:3000']))

# =======================
# Flask-Mail Config
# =======================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME", "dummy@example.com")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD", "dummy")
app.config['MAIL_DEFAULT_SENDER'] = ('ARC Website', os.getenv("MAIL_USERNAME", "dummy@example.com"))
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

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

    body = f"""
📩 New Quote Request (Test Mode)

👤 Name: {name}
📧 Email: {email}
📞 Phone: {phone}

📝 Project Details:
{details}
"""

    try:
        # TEMPORARY: print to console instead of sending email
        print(body)

        # Uncomment below when Gmail credentials ready
        # msg = Message(
        #     subject=f"New Quote Request from {name}",
        #     recipients=["yourbusiness@email.com"],  # replace with actual email
        #     body=body
        # )
        # mail.send(msg)

        flash("✅ Form submitted! (Email not sent in test mode)", "success")
    except Exception as e:
        print("❌ Error:", e)
        flash("⚠️ Something went wrong.", "error")

    return redirect(url_for('index'))

# =======================
# Run Server
# =======================
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=int(os.environ.get("PORT", 5000)), debug=True)
