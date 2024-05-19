from flask import Flask
from views.views import views
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")
# print(app.secret_key)

app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True)


# print(os.getenv("AWS_ACCESS_KEY"))
