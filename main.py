from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = "undertale_wiki.db"


def save_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS characters (name TEXT UNIQUE, title TEXT, text TEXT)")

    characters_data = [
        ("Санс", "Санс ", "Ленивый скелет, брат Папируса. Обожает шутки, кетчуп и судейство игрока."),
        ("Папирус", "Папирус ",
         "Высокий скелет, младший брат Санса. Мечтает вступить в гвардию и готовит спагетти."),
        ("Фриск", "Фриск ", "Главный герой, упавший в Подземелье. Обладает душой Решимости."),
        ("Андайн", "Андайн", "Глава Королевской гвардии, сильная и вспыльчивая рыба-рыцарь."),
        ("Ториэль", "Ториэль ", "Хранительница Руин, заботится о человеке как мать и печет пироги."),
        (
        "Флауи", "Флауи ", "Говорящий цветок. Жестокий манипулятор, живущий по правилу убей или будь убитым.")
    ]

    cursor.executemany("INSERT OR REPLACE INTO characters VALUES (?, ?, ?)", characters_data)

    conn.commit()
    conn.close()

@app.route("/")
def index():
    text = [
        {"zagolowok": "Добро пожаловать!", "text": "Данный сайт -- копия вики по undertale.Тут на данный момент есть всего две кнопки:кнопка логотипа, которая возвращает н главную страницу и кнопка поиска по персонажам, работающая на баез SQLite"},
        {"zagolowok": "Попробуй поискать:", "text": " Санс, Папирус, Фриск, Андайн, Ториэль, Флауи."}
        ]
    return render_template("index.html", text=text)


@app.route("/search")
def search():
    query = request.args.get("query", "").strip().capitalize()


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, text FROM characters WHERE name = ?", (query,))
    row = cursor.fetchone()
    conn.close()

    if row:
        result = {"title": row[0], "text": row[1]}
    else:
        result = {"error": f"Персонаж '{query}' не найден. Доступны: Санс, Папирус, Фриск, Андайн, Ториель, Флауи"}

    return render_template("search.html", result=result)

save_to_db()
app.run()