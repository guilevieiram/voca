# To deploy on heroku, run from the root app directory the command
# git subtree push --prefix backend heroku main

from src.controller import MainController, FlaskController, TerminalController, UserController, MyUserController, DummyUserController
from src.model import UserModel, MyUserModel, DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel

db_model: DataBaseModel = LocalDataBaseModel()
user_model: UserModel = MyUserModel(db_model=db_model)
user_controller: UserController = MyUserController(user_model=user_model)
main_controller: MainController = FlaskController(user_controller=user_controller)

app = main_controller.app

if __name__ == "__main__":
    main_controller.run()