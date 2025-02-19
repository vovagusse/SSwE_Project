import sqlite3
import sqlite3 as s
from pprint import pprint


flush_all_queries = (
        "DROP TABLE IF EXISTS 'employees'",
        "DROP TABLE IF EXISTS 'suppliers'",
        "DROP TABLE IF EXISTS 'coffee_varieties'",
        "DROP TABLE IF EXISTS 'sweets'",
        "DROP TABLE IF EXISTS 'reports'",
        "DROP TABLE IF EXISTS 'contracts'"
    )


def flush_all(cursor: sqlite3.Cursor):
    for query in flush_all_queries:
        q(cursor, query)


def q(cursor: sqlite3.Cursor, 
      sequel_query: str, 
      insert_values: list = None, 
      safe: bool = True, 
      print_query: bool = False) -> bool:
    """short name for SQLite3 Q-uery, the first letter, yes. Does whatever Cursor.execute() does."""
    
    if print_query:
        print(sequel_query)
    
    if safe:
        if insert_values:
            try: cursor.execute(sequel_query, insert_values)
            except: 
                print("oopsie")
                return False
            return True
        try: cursor.execute(sequel_query)
        except: return False
        return True
    if insert_values:
        cursor.execute(sequel_query, insert_values)
        return True
    cursor.execute(sequel_query)
    return True


def get_schema(tables: list):
    print("="*100)
    for table in tables:
        print(table, end="\n\n")
    print("="*100)


"""
CONSTANTS (queries)
"""


# those queries create tables basically
tables = (
    #сотрудники
	"""CREATE TABLE IF NOT EXISTS 'employees' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'name' TEXT,
     'email' TEXT,
     'phone_number' TEXT,
     'position' TEXT,
     'department' TEXT,
     'chief_id' INTEGER
     )""",
    #поставщики
	"""CREATE TABLE IF NOT EXISTS 'suppliers' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'company_name' TEXT,
     'owner_name' TEXT,
     'address' TEXT,
     'postal_code' TEXT,
     'phone_number' TEXT
     )""",
    #виды кофе
	"""CREATE TABLE IF NOT EXISTS 'coffee_varieties' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'name' TEXT,
     'manufacturer' TEXT,
     'country' TEXT,
     'intensity' INTEGER,
     'acidity' INTEGER,
     'sweetness' INTEGER,
     'roast' TEXT,
     'dark_or_light_roast' BOOLEAN,
     'weight' REAL,
     'price' INTEGER,
     'production_date' DATE,
     'expiration_date' DATE,
     'supplier_id' INTEGER DEFAULT 0,
     'contract_id' INTEGER DEFAULT 0,
	 FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
	 FOREIGN KEY (contract_id) REFERENCES contracts(id)
     )""",
    #сладости
	"""CREATE TABLE IF NOT EXISTS 'sweets' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'name' TEXT,
     'manufacturer' TEXT,
     'country' TEXT,
     'weight' REAL,
     'price' INTEGER,
     'calories' INTEGER,
     'production_date' DATE,
     'expiration_date' DATE,
     'supplier_id' INTEGER DEFAULT 0,
     'contract_id' INTEGER DEFAULT 0,
	 FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
     FOREIGN KEY (contract_id) REFERENCES contracts(id)
     )""",
    #фин отчёты (квартальный отчет за 1 квартал 2024) 
	"""CREATE TABLE IF NOT EXISTS 'reports' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'number' TEXT,
     'date' TEXT,
     'report_type' TEXT,
     'description' TEXT,
     'money_earned' INTEGER,
     'money_spent' INTEGER,
     'employee_id' INTEGER DEFAULT 0,
     FOREIGN KEY (employee_id) REFERENCES employees(id)
     )""",
    #договоры
	"""CREATE TABLE IF NOT EXISTS 'contracts' (
     'id' INTEGER PRIMARY KEY AUTOINCREMENT,
     'number' TEXT,
     'date' TEXT,
     'deal_type' TEXT,
     'description' TEXT,
     'status' BOOLEAN,
     'total_cost' INTEGER,
     'employee_id' INTEGER DEFAULT 0,
     'supplier_id' INTEGER DEFAULT 0,
     FOREIGN KEY (employee_id) REFERENCES employees(id),
     FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
     )"""
)
#those queries are for inserting to those tables
inserts = {
 	"employees" : """INSERT INTO 'employees' (
     'name',
     'email',
     'phone_number',
     'position',
     'department',
     'chief_id'
     ) 
     VALUES (?, ?, ?, ?, ?, ?)""",
 	"employees_id" : """INSERT INTO 'employees' (
     'id',
     'name',
     'email',
     'phone_number',
     'position',
     'department',
     'chief_id'
     ) 
     VALUES (?, ?, ?, ?, ?, ?, ?)""",
    "suppliers" : """INSERT INTO 'suppliers' (
     'company_name',
     'owner_name',
     'address',
     'postal_code',
     'phone_number'
     )
     VALUES (?, ?, ?, ?, ?)""",
    "suppliers_id" : """INSERT INTO 'suppliers' (
     'id',
     'company_name',
     'owner_name',
     'address',
     'postal_code',
     'phone_number'
     )
     VALUES (?, ?, ?, ?, ?, ?)""",
	"coffee_varieties" : """INSERT INTO 'coffee_varieties' (
	'name',
	'manufacturer',
	'country',
	'intensity',
	'acidity',
	'sweetness',
	'roast',
	'dark_or_light_roast',
	'weight',
	'price',
	'production_date',
	'expiration_date',
	'supplier_id',
    'contract_id'
	)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
	"coffee_varieties_no_contract" : """INSERT INTO 'coffee_varieties' (
	'name',
	'manufacturer',
	'country',
	'intensity',
	'acidity',
	'sweetness',
	'roast',
	'dark_or_light_roast',
	'weight',
	'price',
	'production_date',
	'expiration_date',
	'supplier_id'
	)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
	"sweets" : """INSERT INTO 'sweets' (
	'name',
	'manufacturer',
	'country',
	'weight',
	'price',
	'calories',
	'production_date',
	'expiration_date',
	'supplier_id',
    'contract_id'
	) 
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
	"sweets_no_contract" : """INSERT INTO 'sweets' (
	'name',
	'manufacturer',
	'country',
	'weight',
	'price',
	'calories',
	'production_date',
	'expiration_date',
	'supplier_id'
	) 
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
	"reports" : """INSERT INTO 'reports' (
	'number',
	'date',
	'report_type',
	'description',
    'money_earned',
    'money_spent',
	'employee_id'
	)
	VALUES (?, ?, ?, ?, ?, ?, ?)""",
	"contracts" : """INSERT INTO 'contracts' (
	'number',
	'date',
	'deal_type',
	'description',
    'status',
    'total_cost',
	'employee_id',
	'supplier_id'
	)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
}

import re
updates = inserts.copy()
for k,v in updates.items():
    p = r"""('[a-zA-Z_]+')\s*\("""
    find = re.findall(p, v)[0]
    new_v = v.replace(find, find + " SET")
    new_v = new_v.replace("INSERT INTO", "UPDATE")
    new_v = new_v.replace("VALUES", "=")
    new_v = new_v + " WHERE id = ?"
    updates[k] = new_v

# pprint(updates)    

#employees preset
employees = (
    (1, "Алымов Артём Олегович","artem@mail.ru", "+7(916)123-45-67", 
     "Директор компании", "Администрация", 0),
    
    (2, "Полсон Роберт Евгеньевич","robpolson@mail.ru", "+7(916)130-85-12 ", 
     "Главный бухгалтер", "Бухгалтерия", 1),
    
    (3, "Павлов Иван Владиславович","pavlovivan@mail.ru", "+7(916)634-52-79", 
     "Специалист по персоналу", "Отдел кадров", 1),
    
    (4, "Тарасов Андрей Даниилович","tarasovandrew@mail.ru", "+7(916)252-72-56", 
     "Главный повар", "Кулинарный отдел", 3),
    
    (5, "Баранова Александра Яковлевна","baranovaalex@mail.ru", "+7(916)161-55-47", 
     "Официант", "отдел3", 3),
    
    (6, "Алексеева Мария Данииловна","alexeevamarie@mail.ru", "+7(916)785-20-88", 
     "Кухонный работник", "отдел3", 3),
    
    (7, "Бирюков Андрей Богданович","birukovandrew@mail.ru", "+7(916)132-40-16", 
     "Бариста", "Обслуживающий персонал", 3),
    
    (8, "Ковалёв Никита Денисович","kovalevnikita@mail.ru", "+7(916)781-93-79", 
     "Уборщик", "Служебный персонал", 3),
    
    (9, "Борисова Сафия Викторовна","borisovasofia@mail.ru", "+7(916)310-95-76", 
     "Бариста", "Служебный персонал", 3),
    
    (10, "Усова Полина Георгиевна","usovapolina@mail.ru", "+7(916)615-60-43", 
     "Бухгалтер", "Бухгалтерия", 2),
    
    (11, "Демидова Полина Георгиевна","demidovapolina@mail.ru", "+7(916)755-86-22 ", 
     "Официант", "Служебный персонал", 3),
    
    (12, "Фролова Александра Максимовна","frolovaalexa@mail.ru", "+7(916)487-29-31", 
     "Разработчик СУРП", "Технический отдел", 2),
    
    (13, "Кузнецов Матвей Константинович","kuznecovmatvei@mail.ru", "+7(916)191-08-72", 
     "Главный системный администратор", "Служебный персонал", 2),
    
    (14, "Романов Семён Максимович","romanovsemen@mail.ru", "+7(916)665-23-35", 
     "Повар", "Обслуживающий персонал", 4),
    
    (15, "Прокофьев Сергей Леонидович","prokofievsergey@mail.ru", "+7(916)075-71-95 ", 
     "Системный администратор", "Технический отдел", 13),
)
""" виды кофе - name, manufacturer, country, 
           intensity, acidity, sweetness, 
           roast, dark_or_light_roast, weight (BOOL - 0 или 1),
           price (REAL), production_date (DATE lol),
           expiration_date (DATE lol x2), supplier_id """

# Current date and time expressed according to ISO 8601 
# Date : 2024-09-15
""" поставщики - id, company_name, owner_name, 
            address, postal_code, phone_number"""
suppliers_id = (
    (
        "1",
        'АО "ВКУС КАМПАНИ"', 
        "Мартоков Радион Русланович",
        "г. Санкт-Петербург, муниципальный округ Лиговка-Ямская вн.тер.г., ул. Атаманская, д. 3/6, лит. С, ПОМЕЩ. 1-Н, ОФИС 102,103",
        "191167",
        "8(800)550-73-52"
    ),
    (
        "2",
        'ООО "ЭЛЛАДА"',
        "Чинивизов Дионис Константинович",
        "г. Москва, вн.тер.г. Муниципальный Округ Даниловский, ул Автозаводская, д. 23А к. 2, этаж 3, помещ. 306.",
        "115280",
        "+7(495)662-67-78"
    ),
    (
        "3",
        'ООО "ГРИН ПОИНТ"',
        "Савельев Андрей Русланович",
        "г. Санкт-Петербург, вн.тер.г. Муниципальный Округ Адмиралтейский Округ, ул Большая Морская, д. 57 литера А, помещ. 13Н/КОМ4",
        "190121",
        # ЭТО НЕ НАСТОЯЩИЙ НОМЕР))) ДА И САЙТА У НИХ НЕТ)))
        "+7(812)438-95-42"
    ),
    (
        "4",
        'ООО "Фудс Импорт"',
        "Илизиров Эсеф Ильич",
        "город Москва, 2-Й Хорошёвский проезд, д. 7 стр. 1а",
        "123007",
        # ЭТО НЕ НАСТОЯЩИЙ НОМЕР 2
        "+7(495)892-28-28"
    ),
    (
        "5",
        'АО "Хлебокомбинат Георгиевский" ("НАТУРпродукт")',
        "Сергеев Александр Александрович",
        "Ставропольский край, город Георгиевск, ул Гагарина, д. 6",
        "357825",
        # ЭТО НЕ НАСТОЯЩИЙ НОМЕР 2
        "+7(495)297-18-22"
    )
)

reports = (
    ("100002", "15.09.2024", 
     "Отчёт о количестве заказов за 3 квартал 2024 года", 
     "Отчёт о количестве заказов и обращений к поставщикам за 3 квартал 2024 года, информация о чистой прибыли и о растратах компании.",
     "350000",
     "230000",
     "1"),
    ("100001", "11.06.2024", 
     "Отчёт о количестве заказов за 2 квартал 2024 года", 
     "Отчёт о количестве заказов и обращений к поставщикам за 2 квартал 2024 года, информация о чистой прибыли и о растратах компании.",
     "150000",
     "100000",
     "1"),
)

contracts = (
    (100001, "11.06.2024", "Договор с поставщиком", 
     "Договор с поставщиком на закупку кофе на период времени", 
     1, 50000, 1, 1),
    (100002, "15.09.2024", "Договор с поставщиком",
     "Договор с поставщиком на закупку кофе на период времени",
     1, 50000, 2, 2),
    (100003, "15.09.2024", "Договор с поставщиком",
     "Договор с поставщиком на закупку кофе на период времени",
     1, 50000, 2, 3),
    (100004, "15.09.2024", "Договор с поставщиком",
     "Договор с поставщиком на закупку сладостей на период времени",
     1, 10000, 2, 4),
    (100005, "15.09.2024", "Договор с поставщиком",
     "Договор с поставщиком на закупку сладостей на период времени",
     1, 10000, 2, 5),
)


coffees = (
    ("Свежая обжарка - кофе VKUS смесь I, 1000 г", 
     "VKUS Coffee Master", "Германия", 
     4, 2, 3, "60% арабика, 40% робуста", 
     0, "1.0", 2502, "2024-09-15", "2025-03-15", 1, 100001),
    ("Свежая обжарка - кофе VKUS смесь II, 1000 г", 
     "VKUS Coffee Master", "Германия", 
     4, 3, 2, "75% арабика, 25% робуста", 
     0, "1.0", 2502, "2024-09-15", "2025-03-15", 1, 100001),
    ("Lavazza Espresso кофе в зёрнах 1000 г", 
     "Lavazza", "Италия", 
     3, 2, 4, "55% арабика, 45% робуста", 
     0, "1.0", 2502, "2024-09-15", "2025-03-15", 2, 100002),
    ("Lavazza Aroma Piu кофе в зёрнах 1000 г", 
     "Lavazza", "Италия", 
     4, 3, 3, "60% арабика, 40% робуста", 
     0, "1.0", 2502, "2024-09-15", "2025-03-15", 2, 100002),
    ("Кофе в зернах Jardin Espresso Gusto, 1 кг", 
     "Jardin", "Швеция", 
     3, 4, 4, "100% арабика, 0% робуста", 
     1, "1.0", 2502, "2024-09-15", "2025-03-15", 3, 100003),
    ("Кофе в зернах Jardin Ethiopia Euphoria, 1 кг", 
     "Jardin", "Швеция", 
     3, 2, 2, "100% арабика, 0% робуста", 
     1, "1.0", 2502, "2024-09-15", "2025-03-15", 3, 100003)
)

sweets = (
    #1
    ("Шоколад Милка Европа", "Милка", "Россия", 
     "0.15", 150, 1000, "2024-07-20", "2025-07-20", 4, 100004),
    #2
    ("Шоколад Алёнка", "Красный Октябрь", "Россия", 
     "0.09", 90, 540, "2024-07-20", "2025-07-20", 4, 100004),
    #3
    ('Пряник "Кавксзский Сувенир" (маленький)', "Георгиевский Хлебокомбинат", "Россия", 
     "0.450", 70, 1620, "2024-07-20", "2024-09-20", 5, 100005),
    #4
    ('Пряник "Кавксзский Сувенир" (большой)', "Георгиевский Хлебокомбинат", "Россия", 
     "1", 150, 3310, "2024-07-20", "2024-09-20", 5, 100005),
    #5
    ('Печенье от "Хлебокомбината Георгиевского"', "Георгиевский Хлебокомбинат", "Россия", 
     "0.2", 74, 500, "2024-07-20", "2024-09-20", 5, 100005)
)


def main() -> None:
    get_schema(tables)
    # get_schema(inserts.values())
    # get_schema(updates.values())
    
    # """
    # directory = "D:\\kursovaya_isukk\\моя курсовая\\"
    # connection = sqlite3.connect(f'{directory}database.db')
    # cur = connection.cursor()
    
    # #clear previous schema
    # flush_all(cur)
    
    # #init tables
    # for query in tables:
    #     q(cur, query)
        
    # #filling in
    # for e in employees:
    #     q(cur, inserts["employees_id"], e)
    # for s in suppliers_id:
    #     q(cur, inserts["suppliers_id"], s)
    # for c in coffees:
    #     q(cur, inserts["coffee_varieties_no_contract"], c[:-1], False)
    # for s in sweets:
    #     q(cur, inserts["sweets_no_contract"], s[:-1], False)
    # for r in reports:
    #     q(cur, inserts["reports"], r)
    # for cn in contracts:
    #     q(cur, inserts["contracts"], cn, False)
    # connection.commit()
    # connection.close()
    # """



if __name__ == "__main__":
    main()
