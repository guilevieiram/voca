from src.controller import MainController, FlaskController, TerminalController, UserController, MyUserController
from src.model import UserModel, MyUserModel, DataBaseModel, LocalDataBaseModel

app: MainController = TerminalController(
    user_controller=MyUserController(
        user_model=MyUserModel(
            db_model=LocalDataBaseModel()
        )
    )
)

if __name__ == "__main__":
    app.run()