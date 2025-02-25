# Building repository knowledge graph

This document describes the process of building the repository knowledge graph.

### Phase 1: Create repository nodes using a tree

In path code-assistant/backend/graph/utils/repo_scrap_utils.py we have a function that gives us the repository organized as a tree is respect to the repository root given in the input.

At the moment i have feel files in repository, so the tree is like:
```
/Users/matheussilva/Documents/projects/code-assistant/
├── README.md
├── backend/
│   ├── core/
│   │   ├── config.py
│   │   ├── gptconfig.py
│   │   └── langchain_utils.py
│   └── graph/
│       ├── graph_builder.py
│       ├── graph_search.py
│       ├── neo4j.sh
│       ├── prompts/
│       │   └── repo_tree_prompt.py
│       └── utils/
│           ├── graph_setup.py
│           └── repo_scrap_utils.py
├── frontend/
│   └── AppDelegate.py
└── requirements.txt
```
So the graph will be like: 
![image](https://github.com/user-attachments/assets/fbacf391-9e61-40e4-894f-c14824fb6f9e)

That seems to be correct, this part is refered in code-assistant/backend/graph/graph_builder.py in function `create_tree`.

### Phase 2: TODO
