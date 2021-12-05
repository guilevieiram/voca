from src.controller import MainController, FlaskController, UserController, DummyUserController

app: MainController = FlaskController(user_controller=DummyUserController())

if __name__ == "__main__":
    app.run()