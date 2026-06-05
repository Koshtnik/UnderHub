from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "undertale_wiki.db"


def init_db():


    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')


    characters_data = [
        ("Санс", "Санс (Sans)",
         "Ленивый скелет, брат Папируса. Известен своими шутками, каламбурами, любовью к кетчупу и судейством игрока в конце игры. Один из самых опасных боссов на пути Геноцида."),
        ("Папирус", "Папирус (Papyrus)",
         "Высокий скелет, младший брат Санса. Он мечтает поймать человека, чтобы вступить в Королевскую гвардию. Очень добрый, оптимистичный и обожает готовить спагетти."),
        ("Фриск", "Фриск (Frisk)",
         "Главный герой игры, человек, упавший в Подземелье. Обладает красной душой Решимости, которая позволяет сохранять и перезагружать игру."),
        ("Андайн", "Андайн (Undyne)",
         "Глава Королевской гвардии, антропоморфная рыба-рыцарь. Очень сильная и вспыльчивая. Охотится за душой человека, чтобы освободить всех монстров."),
        ("Ториэль", "Ториэль (Toriel)",
         "Хранительница Руин, бывшая королева. Спасает человека в начале игры, заботится о нём как мать, печет пироги и пытается уберечь от опасностей Подземелья."),
        ("Флауи", "Флауи (Flowey)",
         "Первый персонаж в игре. Выглядит как говорящий цветок, но за милой внешностью скрывается жестокий манипулятор, живущий по правилу 'убей или будь убитым'.")
    ]


    cursor.executemany('''
        INSERT OR IGNORE INTO characters (name, title, description) 
        VALUES (?, ?, ?)
    ''', characters_data)

    conn.commit()
    conn.close()
    print("База данных SQLite успешно создана и заполнена!")


def get_character_from_db(character_name):

    character_name = character_name.strip().capitalize()


    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM characters WHERE name = ?", (character_name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        #
        return {
            "title": row["title"],
            "text": row["description"]
        }

    return {
        "error": f"Персонаж '{character_name}' не найден в базе данных. Доступны: Санс, Папирус, Фриск, Андайн, Ториэль, Флауи."
    }

@app.route("/")
def index():
    text = [
        {"zagolowok": "Добро пожаловать!",
         "text": "Данный сайт -- копия вики по undertale, работающая на базе данных SQLite. Тут есть кнопка с логотипом для возвращения и кнопка поиска. Удачи!"},
        {"zagolowok": "Популярные темы:", "text": "Попробуйте поискать: Санс, Папирус, Фриск, Андайн, Ториэль, Флауи."}
    ]
    return render_template("index.html", text=text)

@app.route("/search")
def search():
    query = request.args.get("query")

    result = get_character_from_db(query) if query else {"error": "Вы ничего не ввели в поиск."}
    return render_template("search.html", result=result, query=query)


init_db()
app.run()
