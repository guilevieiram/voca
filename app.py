from src.controller import MainController, FlaskController, TerminalController, UserController, DummyUserController

app: MainController = TerminalController(user_controller=DummyUserController())

if __name__ == "__main__":
    app.run()