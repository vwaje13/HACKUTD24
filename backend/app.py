from flask import Flask
from routes.vectorize import vectorize_bp

app = Flask(__name__)

# Register the vectorize blueprint
app.register_blueprint(vectorize_bp)

if __name__ == '__main__':
    app.run(debug=True)