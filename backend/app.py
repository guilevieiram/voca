# To deploy on heroku, run from the root app directory the command
# git subtree push --prefix backend heroku main

from src.controller import MainController, FlaskController, TerminalController, UserController, MyUserController, DummyUserController
from src.model import UserModel, MyUserModel, DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel

db_model: DataBaseModel = PostgresqlDataBaseModel
user_model: UserModel = MyUserModel
user_controller: UserController = MyUserController
main_controller: MainController = FlaskController



endpoint = main_controller(
    user_controller=user_controller(
        user_model=user_model(
            db_model=db_model()
        )
    )
)
app = endpoint.app

if __name__ == "__main__":
    endpoint.run()