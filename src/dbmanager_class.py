import psycopg2


class DBManager:
    """Класс для работы с базой данной PostgreSQL"""

    def __init__(self, database_name: str, params: dict):
        """Инициализатор класса"""
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def __del__(self):
        """Метод для закрытия соединения с базой данных перед удалением экземпляра"""
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, open_vacancies FROM public.employers
                ORDER BY open_vacancies DESC
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
            названия вакансии и зарплаты и ссылки на вакансию"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, vacancies.name, salary_min, salary_max, vacancies.alternate_url
                FROM public.vacancies 
                LEFT JOIN employers USING(employer_id)
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary_min) FROM vacancies;
            """)
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT vacancies.name, salary_min, salary_max, employers.name, vacancies.alternate_url FROM vacancies
                LEFT JOIN employers USING(employer_id)
                WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies)
                ORDER BY salary_min DESC
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, key_word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT vacancies.name, salary_min, salary_max, vacancies.alternate_url FROM vacancies
                WHERE name LIKE '%{key_word}%'
                ORDER BY salary_min DESC
            """)
            return cur.fetchall()