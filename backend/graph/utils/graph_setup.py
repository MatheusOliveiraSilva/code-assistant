import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, basic_auth
from langchain_neo4j import Neo4jGraph

load_dotenv()


class GraphSetup:
    def __init__(self, db_name: str):
        """
        Inicializa a configuração do grafo para o banco especificado.

        Args:
            db_name (str): Nome do banco de dados que será usado (por exemplo, "MY_DATABASE").
        """
        self.db_name = db_name
        self.driver = self.create_driver()
        self.check_or_create_database()
        # Utiliza o banco criado ou existente para inicializar o Neo4jGraph
        self.graph = Neo4jGraph(database=self.db_name, refresh_schema=True)
        print(f"Conectado ao banco de dados: {self.db_name}")

    def create_driver(self):
        """
        Cria e retorna um driver do Neo4j usando as variáveis de ambiente.
        """
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        return GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def check_or_create_database(self):
        """
        Conecta à database "system" e verifica se o banco com o nome especificado existe.
        Se não existir, cria-o.

        Nota: Este comando requer a edição Enterprise do Neo4j, que suporta multi-database.
        """
        with self.driver.session(database="system") as session:
            result = session.run("SHOW DATABASES")
            databases = [record["name"] for record in result]
            if self.db_name in databases:
                print(f"Database '{self.db_name}' já existe.")
            else:
                print(f"Database '{self.db_name}' não existe. Criando...")
                session.run(f"CREATE DATABASE {self.db_name}")
                print(f"Database '{self.db_name}' criado.")

    def close(self):
        """
        Fecha a conexão com o driver do Neo4j.
        """
        self.driver.close()


# Exemplo de uso:
if __name__ == "__main__":
    # Defina o nome do banco que deseja utilizar
    db_name = "MY_DATABASE"
    setup = GraphSetup(db_name)

    # A partir daqui, utilize setup.graph para interagir com o banco
    # ...

    setup.close()
