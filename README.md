# Adaptative Context Code Assistant

### Project overview
The main goal is to have an app that we run in MacBook and we can select a repository of code that our code assistant will know everything about it.
When we select the repository, we create a knowledge graph about the repository automatically and chunk function bodies into documents that will be used as context for assistant when we ask any help to create new features, debug, optimize code, refactor etc.

### Repository selection
<img width="804" alt="image" src="https://github.com/user-attachments/assets/b1dbfb21-78a6-4b2a-b412-6b9ff5939372" />

When user open the app will have options to select the repository that the chat will be about. If the repository already is preprocessed and we have the documents and knowledge graph about it, we proceed to chat, otherwise we process all data and create this context information.
In first version, we will not save chat history, so project have less complexity, but would be easy to store all chat history in a database and create id's for each new chat, and manage this with MemorySaver class built-in on langgraph.

Also during conversation, it's possible that user change some stuff at the files, and the agent can't have access to outdated information about repository, that can lead to more errors. So we need to make a system that detect changes at files that are in that repository during conversation and update/delete/create new nodes on graph and also change documents stored.
This is showed at the following diagram:

<img width="805" alt="image" src="https://github.com/user-attachments/assets/fce406c2-a9d8-4f83-8bdf-44c61eb2e518" />

It's also possible that we make changes on repository while app is closed, so that's why in first diagram we say "updated knowledge".

### Querying process
<img width="966" alt="image" src="https://github.com/user-attachments/assets/3f202d41-b9bc-478c-823f-c039e2ea7d8a" />

In my experience using AI agents as code helpers, more context you give about your repository, better it perform. It can also infer things that are not shown on context because of it prior knowledge (e.g. Agent can see a database connection but don't see database Schema, so it will need to receive information from user like tables available to query). Because of that, all my efforts will be allocated to make the best context and prompt manegement i can do, but sometimes (rarely) the problem is not in our code, and we did everything we could do (very rare, always is likely to be skill issue bug) and need to search on web for community discussions of how to solve that. So it's good to have a web search layer on our context construction.

Our app will have a resource that is "@" and user can use it to link the files that are related with his query. If user use the @ to tag the relevant files, we first of all look to context of tagged files and ask to LLM as Judge if that is enought to answer user's query. If yes, we go ahead for answer, if not we search on web for solutions.

### Code Assistant Architecture
<img width="1207" alt="image" src="https://github.com/user-attachments/assets/1aa8777f-f7be-46e4-93dd-b20a2bd609e6" />

When we send a message to chatbot (Node __START__), we collect context information executing a search algorithm on knowledge graph (first node). We get all nodes connected with our tagged documents, and filter the nodes with more semantic pontuation. The algorithm will be better explained in read.me inside of graph algorithms directory.

In second node we send a prompted message to llm with resumed and polished context that we have retrieved, and give to llm the possibility to call the websearch tool. If llm decide that we don't have enought context to answer question, it call web search (multiple times, if needed but i'll put a cap of searchs in future if it cause problems).

After collecting context information for answer user question, added to graph context, we answer of ask for user to give more especific informations that we see that is missing.


