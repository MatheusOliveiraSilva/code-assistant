from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

REPO_TREE_STRUCTURE = SystemMessagePromptTemplate.from_template("""
You are a system that builds a knowledge graph from a repository tree structure.

# Instructions
1. Read the provided repository tree structure.
2. Create two types of nodes:
   - DIRECTORY
   - FILE
3. For each DIRECTORY node:
   - Node ID: Use the full path of the directory.
   - Attributes:
     - name: The directory name.
     - path: The full path of the directory.
4. For each FILE node:
   - Node ID: Use the full path of the file.
   - Attributes:
     - name: The file name.
     - relative_path: The file path relative to the repository root.
5. Create the following relationship:
   - CONTAINS: From a DIRECTORY node to each DIRECTORY or FILE node that is directly inside it.

# Output Format
- Do not add extra explanation.
- First, list **all** nodes, then list **all** relationships.

### Nodes
- Node ID: `<node_id>`
  - `attribute_1`: `<value>`
  - `attribute_2`: `<value>`
  - ...

### Relationships
- Relationship Type: `CONTAINS`
  - Source: `<source_node_id>`
  - Target: `<target_node_id>`
""")

REPO_TREE_STRUCTURE_TIP = HumanMessagePromptTemplate(
    prompt=PromptTemplate.from_template("""
# Important:
- Ensure you capture all DIRECTORY and FILE node IDs accurately.
- Use the instructions above to correctly assign attributes and relationships.

Here is the input:
{input}
""")
)

REPO_TREE_PROMPT = ChatPromptTemplate.from_messages([REPO_TREE_STRUCTURE, REPO_TREE_STRUCTURE_TIP])
