from main_app import app
from api import app as api_app

if __name__ == '__main__':
    app.run()
    api_app.run()
