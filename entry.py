from src import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run(port=(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)