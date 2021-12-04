from src.controller import Controller, FlaskController

app: Controller = FlaskController()

if __name__ == "__main__":
    app.run()