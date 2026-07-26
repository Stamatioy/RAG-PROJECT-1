To run llama.cpp server: Open a powershell window

cd "D:\Programming\Projects\RAG\Simple RAG\RAG Project 1\src\llama_cpp"

.\llama-server.exe `
-m "..\models\qwen2.5-7b-instruct-q5_k_m-00001-of-00002.gguf" `
-c 8192

to run backend server: In powershell

cd "D:\Programming\Projects\RAG\Simple RAG\RAG Project 1"

uvicorn src.api.main:app --reload

To run frontend:

cd "PS D:\Programming\Projects\RAG\Simple RAG\RAG Project 1\frontend"

 npm run dev
