# Employee Handbook RAG

## PURPOSE
- I recently read [Hands-On RAG for Production By Ofer Mendelevitch and Forrest Sheng Bao](https://learning.oreilly.com/library/view/hands-on-rag-for/9798341621701/) so decided to build a RAG system based on my learning

## Expectations
### Sanitization
- Purposefully add test cases with wrong encodings or build a system that can handle it.
- Try model as judge to label maliciousness, ideally I would try this out with jev but no free 5$ credits atm.
- Try non aggressive sanitization ie we get the user input instead of fully rejecting we will try to see if there is any non malicious part I think this might even make ppl not try to break the system.

### Retrieval
- Explore different chunking methods such as fixed length chunking, sentence, paragraph based and recursive.
- Figure out how the performace metrics such as common ones like precision, accuracy, recall and nDCG changes with different chunking methods.
- Performace with and without reranking.
- Test out pgvector, qdrant and pinecone. In pinecone I want to know what will happend if we hit max sequence length.

### Generation
- Test Nuggetization on the model I will be trying out from openrouter.
- Build a eval dataset and test out multiple free small models from openrouter.
- Relevance and token usage and other metrics as part of logging. Also try my hand on traces.

### Query
- Query expansion/rewriting, abbreviation expansion, query decomposition for multi-part questions(ig this would be a agent sorta application but lets see)

