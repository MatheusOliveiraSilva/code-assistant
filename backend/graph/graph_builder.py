import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from backend.core.langchain_utils import get_llm
from backend.graph.utils.repo_scrap_utils import get_tree_string
from backend.graph.prompts.repo_tree_prompt import REPO_TREE_PROMPT

load_dotenv(dotenv_path=".env")

class RepositoryToGraph:
    def __init__(self, max_retries=5):
        self.graph = Neo4jGraph(refresh_schema=True)
        # self.llm = get_llm(max_tokens=20000)
        self.llm = ChatOpenAI(openai_api_key=os.getenv("OLD_OPENAI_API_KEY"))

        # Initialize the transformers
        self.repo_tree_generator = self.repo_tree_generator()
        self.relations_generator = self.relations_generator()

    def repo_tree_generator(self) -> LLMGraphTransformer:
        """
        LLMGraphTransformer to convert a repository tree in nodes and relationships.
        """
        return LLMGraphTransformer(
            llm=self.llm,
            prompt=REPO_TREE_PROMPT,
            allowed_nodes=["DIRECTORY", "FILE"],
            allowed_relationships=["CONTAINS"],
            node_properties=[
                # directory properties
                "name",
                "path",

                # file properties
                "name",
                "relative_path",
            ]
        )

    def relations_generator(self) -> LLMGraphTransformer:
        """
        LLMGraphTransformer to convert ddls in nodes and relationships.
        """
        return LLMGraphTransformer(
            llm=self.llm,
#prompt=RELATIONS_PROMPT,
            allowed_nodes=["FILE", "CLASS", "FUNCTION"],
            allowed_relationships=[
                "DEFINES", "IMPORTS", "USES",
                "CALLS"
            ],
            node_properties=[
                # class properties
                "name",
                "file_name",
                "docstring",
                "body"
                
                # function properties
                "name",
                "signature",
                "file_name",
                "docstring",
                "body",
            ]
        )

    def create_tree(self, repo_root):
        """
        Create the nodes from the augmented schema chunks.
        :return: None
        """

        tree_str = get_tree_string(repo_root)

        doc = Document(page_content=tree_str, metadata={"repo_root": repo_root})

        graph_document = self.repo_tree_generator.convert_to_graph_documents([doc])

        self.graph.add_graph_documents(graph_document, include_source=False)

        print("Finished first phase, repository tree created!")

if __name__ == "__main__":
    repo_to_graph = RepositoryToGraph()
    repo_to_graph.create_tree("/Users/matheussilva/Documents/projects/code-assistant")
