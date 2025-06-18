import psycopg2

class Postgre_Sql_Context:
    def __init__(self):
        # Parâmetros de conexão
        self.parametros_conexao = {
            'host': "localhost",
            'port': "5432",
            'database': "notas",
            'user': "postgres",
            'password': "iatandia27"
        }
        self.conexao = None
        self.cursor = None

    def conectar(self):
        """Estabelece a conexão com o banco de dados."""
        if self.conexao is None or self.conexao.closed:
            try:
                self.conexao = psycopg2.connect(
                    host=self.parametros_conexao.get('host'),
                    port=self.parametros_conexao.get('port'),
                    database=self.parametros_conexao.get('database'),
                    user=self.parametros_conexao.get('user'),
                    password=self.parametros_conexao.get('password')
                )
                print("Conectado com sucesso!")
                return True
            except psycopg2.Error as e:
                print("Não foi possível se conectar ao banco de dados.")
                print(f"Erro -> {e}")
                self.conexao = None
                return False
        return True

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao is not None and not self.conexao.closed:
            self.conexao.close()
            self.conexao = None
            print("Desconectado com sucesso!")

    def executar_update_sql(self, query, params=None):
        """Executa uma query de atualização ou inserção no banco de dados."""
        if not self.conectar():
            print("Falha na conexão. Não é possível executar a query.")
            return False
        try:
            self.cursor = self.conexao.cursor()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conexao.commit()
            self.cursor.close()
            print("Query executada com sucesso!")
            return True
        except psycopg2.Error as e:
            print("Erro ao executar a query.")
            print(f"Erro -> {e}")
            self.conexao.rollback()
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def executar_query_sql(self, query, params=None):
        """
        Executa uma consulta SQL e retorna os resultados.
        Parâmetros:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Parâmetros para a query.
        Retorno:
            Lista de tuplas com os resultados ou None em caso de erro.
        """
        if not self.conectar():
            print("Falha na conexão. Não é possível executar a query.")
            return None
        try:
            self.cursor = self.conexao.cursor()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados
        except psycopg2.Error as e:
            print(f"Erro ao executar a query: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()