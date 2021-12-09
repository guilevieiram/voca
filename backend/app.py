from src.controller import MainController, FlaskController, TerminalController, UserController, MyUserController
from src.model import UserModel, MyUserModel, DataBaseModel, LocalDataBaseModel

db_model: DataBaseModel = LocalDataBaseModel()
user_model: UserModel = MyUserModel(db_model=db_model)
user_controller: UserController = MyUserController(user_model=user_model)
main_controller: MainController = FlaskController(user_controller=user_controller)

app = main_controller.app

if __name__ == "__main__":
    main_controller.run()