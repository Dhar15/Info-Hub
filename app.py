from flask import Flask, render_template
from app.routes import bp
import os

app = Flask(__name__, static_folder='app/static')
app.register_blueprint(bp)

# Global error handler for uncaught exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error.html"), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)