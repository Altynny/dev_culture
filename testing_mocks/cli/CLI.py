import requests
import questionary
import os
import json
import sys
from typing import Dict, Any, Optional, List
from enum import Enum, auto
from rich.console import Console
from rich.table import Table
from rich import box


BASE_URL = "http://localhost:8000"
TOKEN_FILE = ".token.json"


class Command(Enum):
    LOGIN = auto()
    REGISTER = auto()
    UPLOAD_FILE = auto()
    LIST_MY_FILES = auto()
    VIEW_FILE_DATA = auto()
    LIST_USERS = auto()
    LIST_USER_FILES = auto()
    LOGOUT = auto()
    EXIT = auto()


class ApiClient:
    def __init__(self, base_url: str, token_file: str):
        self.base_url = base_url
        self.token_file = token_file
        self.console = Console()

    def save_token(self, token: str) -> None:
        with open(self.token_file, "w") as f:
            json.dump({"token": token}, f)

    def load_token(self) -> Optional[str]:
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                data = json.load(f)
                return data.get("token")
        return None

    def get_headers(self) -> Dict[str, str]:
        token = self.load_token()
        if not token:
            questionary.print("Вы не авторизованы! Пожалуйста, выполните вход.", style="bold red")
            return {}
        return {"Authorization": f"Bearer {token}"}

    def is_authenticated(self) -> bool:
        return self.load_token() is not None

    def login(self) -> None:
        username = questionary.text("Имя пользователя:").ask()
        password = questionary.password("Пароль:").ask()
        
        if not password or len(password.strip()) == 0:
            questionary.print("Ошибка: Пароль не может быть пустым!", style="bold red")
            return
        
        try:
            response = requests.post(
                f"{self.base_url}/token",
                data={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                self.save_token(token)
                questionary.print("Успешный вход в систему!", style="bold green")
            else:
                questionary.print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def register(self) -> None:
        username = questionary.text("Введите имя пользователя:").ask()
        
        if not username or len(username.strip()) == 0:
            questionary.print("Ошибка: Имя пользователя не может быть пустым!", style="bold red")
            return
            
        password = questionary.password("Введите пароль:").ask()
        
        if not password or len(password.strip()) == 0:
            questionary.print("Ошибка: Пароль не может быть пустым!", style="bold red")
            return
            
        password_confirm = questionary.password("Подтвердите пароль:").ask()
        
        if password != password_confirm:
            questionary.print("Пароли не совпадают!", style="bold red")
            return
        
        try:
            response = requests.post(
                f"{self.base_url}/users/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 201:
                questionary.print("Пользователь успешно зарегистрирован!", style="bold green")
                if questionary.confirm("Выполнить вход с новой учетной записью?").ask():
                    login_resp = requests.post(
                        f"{self.base_url}/token",
                        data={"username": username, "password": password}
                    )
                    if login_resp.status_code == 200:
                        token = login_resp.json().get("access_token")
                        self.save_token(token)
                        questionary.print("Вход выполнен успешно!", style="bold green")
            else:
                questionary.print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def list_users(self) -> None:
        headers = self.get_headers()
        if not headers:
            return
        
        try:
            response = requests.get(f"{self.base_url}/users/", headers=headers)
            
            if response.status_code == 200:
                users = response.json()
                
                if not users:
                    questionary.print("Нет зарегистрированных пользователей", style="bold yellow")
                    return
                
                table = Table(title="Список пользователей", box=box.ROUNDED)
                table.add_column("ID", justify="right", style="cyan")
                table.add_column("Имя пользователя", style="green")
                
                for user in users:
                    table.add_row(str(user["id"]), user["username"])
                
                self.console.print(table)
            else:
                questionary.print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def list_my_files(self) -> None:
        headers = self.get_headers()
        if not headers:
            return
        
        try:
            response = requests.get(f"{self.base_url}/users/me/files/", headers=headers)
            
            if response.status_code == 200:
                files = response.json()
                
                if not files:
                    questionary.print("У вас нет загруженных файлов", style="bold yellow")
                    return
                
                table = Table(title="Мои файлы", box=box.ROUNDED)
                table.add_column("ID", justify="right", style="cyan")
                table.add_column("Имя файла", style="green")
                table.add_column("Дата загрузки", style="blue")
                
                for file in files:
                    table.add_row(str(file["id"]), file["filename"], file["upload_date"])
                
                self.console.print(table)
            else:
                questionary.print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def list_user_files(self) -> None:
        headers = self.get_headers()
        if not headers:
            return
        
        try:
            users_response = requests.get(f"{self.base_url}/users/", headers=headers)
            
            if users_response.status_code != 200:
                questionary.print(f"Ошибка: {users_response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
                return
            
            users = users_response.json()
            if not users:
                questionary.print("Нет зарегистрированных пользователей", style="bold yellow")
                return
            
            choices = [f"{user['id']} - {user['username']}" for user in users]
            selected_user = questionary.select(
                "Выберите пользователя:",
                choices=choices
            ).ask()
            
            if not selected_user:
                return
            
            user_id = selected_user.split(" - ")[0]
            
            files_response = requests.get(f"{self.base_url}/users/{user_id}/files/", headers=headers)
            
            if files_response.status_code == 200:
                files = files_response.json()
                
                if not files:
                    questionary.print("У этого пользователя нет загруженных файлов", style="bold yellow")
                    return
                
                table = Table(title=f"Файлы пользователя (ID: {user_id})", box=box.ROUNDED)
                table.add_column("ID", justify="right", style="cyan")
                table.add_column("Имя файла", style="green")
                table.add_column("Дата загрузки", style="blue")
                
                for file in files:
                    table.add_row(str(file["id"]), file["filename"], file["upload_date"])
                
                self.console.print(table)
            else:
                questionary.print(f"Ошибка: {files_response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def upload_file(self) -> None:
        headers = self.get_headers()
        if not headers:
            return
        
        file_path = questionary.path(
            "Выберите CSV файл для загрузки:",
            file_filter=lambda path: path.endswith('.csv')
        ).ask()
        
        if not file_path:
            return
        
        if not os.path.exists(file_path):
            questionary.print("Файл не найден!", style="bold red")
            return
        
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, 'text/csv')}
                response = requests.post(
                    f"{self.base_url}/users/me/files/",
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 201:
                questionary.print("Файл успешно загружен!", style="bold green")
            else:
                questionary.print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def view_file_data(self) -> None:
        headers = self.get_headers()
        if not headers:
            return
        
        try:
            files_response = requests.get(f"{self.base_url}/users/me/files/", headers=headers)
            
            if files_response.status_code != 200:
                questionary.print(f"Ошибка: {files_response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
                return
            
            files = files_response.json()
            if not files:
                questionary.print("У вас нет загруженных файлов", style="bold yellow")
                return
            
            choices = [f"{file['id']} - {file['filename']} ({file['upload_date']})" for file in files]
            selected_file = questionary.select(
                "Выберите файл для просмотра:",
                choices=choices
            ).ask()
            
            if not selected_file:
                return
            
            file_id = selected_file.split(" - ")[0]
            
            data_response = requests.get(f"{self.base_url}/users/me/files/{file_id}/data/", headers=headers)
            
            if data_response.status_code == 200:
                data = data_response.json()
                
                if not data:
                    questionary.print("Файл пуст или не содержит данных", style="bold yellow")
                    return
                
                table = Table(title="Данные файла", box=box.ROUNDED)
                for key in data[0].keys():
                    table.add_column(key)
                
                max_rows = 20
                for idx, row in enumerate(data):
                    if idx >= max_rows:
                        break
                    table.add_row(*[str(row[key]) for key in row.keys()])
                
                self.console.print(table)
                
                if len(data) > max_rows:
                    questionary.print(f"Показаны первые {max_rows} из {len(data)} записей", style="bold yellow")
                    
                if questionary.confirm("Хотите сохранить данные в JSON файл?").ask():
                    output_file = questionary.text(
                        "Введите путь для сохранения JSON файла:", 
                        default="output.json"
                    ).ask()
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    questionary.print(f"Данные сохранены в файл {output_file}", style="bold green")
                    
            else:
                questionary.print(f"Ошибка: {data_response.json().get('detail', 'Неизвестная ошибка')}", style="bold red")
        except requests.RequestException as e:
            questionary.print(f"Ошибка соединения: {str(e)}", style="bold red")

    def logout(self) -> None:
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
            questionary.print("Выход выполнен успешно!", style="bold green")
        else:
            questionary.print("Вы не были авторизованы", style="bold yellow")


class App:
    def __init__(self):
        self.api_client = ApiClient(BASE_URL, TOKEN_FILE)
        self.commands_map = {
            Command.LOGIN: self.api_client.login,
            Command.REGISTER: self.api_client.register,
            Command.UPLOAD_FILE: self.api_client.upload_file,
            Command.LIST_MY_FILES: self.api_client.list_my_files,
            Command.VIEW_FILE_DATA: self.api_client.view_file_data,
            Command.LIST_USERS: self.api_client.list_users,
            Command.LIST_USER_FILES: self.api_client.list_user_files,
            Command.LOGOUT: self.api_client.logout,
            Command.EXIT: self.exit_app
        }

    def get_menu_choices(self) -> List[Dict[str, Any]]:
        if self.api_client.is_authenticated():
            return [
                {"name": "Загрузить CSV файл", "value": Command.UPLOAD_FILE},
                {"name": "Просмотреть мои файлы", "value": Command.LIST_MY_FILES},
                {"name": "Просмотреть данные файла", "value": Command.VIEW_FILE_DATA},
                {"name": "Просмотреть список пользователей", "value": Command.LIST_USERS},
                {"name": "Просмотреть файлы пользователя", "value": Command.LIST_USER_FILES},
                {"name": "Выйти из аккаунта", "value": Command.LOGOUT},
                {"name": "Выйти из программы", "value": Command.EXIT}
            ]
        else:
            return [
                {"name": "Войти", "value": Command.LOGIN},
                {"name": "Зарегистрироваться", "value": Command.REGISTER},
                {"name": "Выйти из программы", "value": Command.EXIT}
            ]

    def exit_app(self) -> None:
        questionary.print("До свидания!", style="bold green")
        sys.exit(0)

    def run(self) -> None:
        questionary.print("===== Клиент для сервера обработки данных пользователей =====", style="bold blue")
        
        while True:
            choices = self.get_menu_choices()
            action = questionary.select(
                "Выберите действие:",
                choices=choices
            ).ask()
            
            if not action:
                break
            
            handler = self.commands_map.get(action)
            if handler:
                handler()


if __name__ == "__main__":
    app = App()
    app.run()