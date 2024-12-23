from sentence_transformers import SentenceTransformer, util
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os

import config


class Chatbot:
    def __init__(self, api_key, golden_answers_path, rag_doc_path):
        """Initialize the chatbot."""
        os.environ["OPENAI_API_KEY"] = api_key
        self.golden_answers_path = golden_answers_path
        self.rag_doc_path = rag_doc_path
        self.vector_store = None
        self.retriever = None
        self.qa_chain = None
        self.rag_vector_store = None
        self.rag_retriever = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Semantic similarity model
        self.rag_text = None  # Plain-text RAG content
        self._setup()

    def _setup(self):
        """Set up the chatbot."""
        self.rebuild_vector_store()

        llm = OpenAI(temperature=0.0)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.retriever,
            return_source_documents=True
        )

        # Load and cache the plain-text RAG document
        with open(self.rag_doc_path, "r") as file:
            self.rag_text = file.read().strip()
        print("Chatbot setup complete.")

    def rebuild_vector_store(self):
        """Rebuild the vector stores for golden answers and RAG document."""
        # Rebuild vector store for golden answers
        with open(self.golden_answers_path, "r") as file:
            golden_texts = file.read().strip().split("\n\n")

        golden_embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(golden_texts, golden_embeddings)
        self.retriever = self.vector_store.as_retriever()

        # Rebuild vector store for RAG document
        with open(self.rag_doc_path, "r") as file:
            rag_lines = [line.strip() for line in file if line.strip()]  # Read and split into lines

        rag_embeddings = OpenAIEmbeddings()
        self.rag_vector_store = FAISS.from_texts(rag_lines, rag_embeddings)
        self.rag_retriever = self.rag_vector_store.as_retriever()

    def query(self, query_text, expected_output):
        """Retrieve relevant data, rate the response, and return the response with its rating."""
        print(f"Received Query: {query_text}")

        # Step 1: Check Golden Answers
        response_data = self.qa_chain.invoke({"query": query_text})
        response = response_data["result"].strip()
        source_documents = response_data["source_documents"]

        # Log golden answer source documents
        print("Source Documents (Golden Answers):")
        for doc in source_documents:
            print(doc.page_content)

        # Compare response with exact match from source documents
        for doc in source_documents:
            content = doc.page_content.strip()
            if "Q:" in content and "A:" in content:
                question, answer = content.split("A:", 1)
                if query_text.lower() == question.replace("Q:", "").strip().lower():
                    print(f"Golden Answer Found: {answer.strip()}")
                    return answer.strip(), 3

        # Step 2: Retrieve from Plain-Text RAG Document
        print("Searching RAG Document...")
        rag_docs = self.rag_retriever.get_relevant_documents(query_text)
        if rag_docs:
            best_line = rag_docs[0].page_content
            print(f"RAG Response Found: {best_line}")

            # Use AI to phrase the response based on the matched line
            phrased_response = self.phrase_response(query_text, best_line)
            if phrased_response:
                print(f"AI-Generated Response: {phrased_response}")

                # Step 2.1: Rate the phrased response
                similarity = self.calculate_similarity(phrased_response, expected_output)
                if similarity > 0.8:
                    rating = 3
                elif similarity > 0.4:
                    rating = 2
                else:
                    rating = 1

                return phrased_response, rating

        # Step 3: Fallback - Use AI-Generated Response
        print("No relevant answers found. Falling back to AI-generated response.")
        return "I don’t know.", 1

    def calculate_similarity(self, response, query_text):
        """Calculate semantic similarity between the response and the query using SentenceTransformer."""
        query_embedding = self.model.encode(query_text, convert_to_tensor=True)
        response_embedding = self.model.encode(response, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, response_embedding)[0][0].item()
        print(f"Calculated Similarity Rating: {similarity}")
        return similarity

    def phrase_response(self, query_text, matched_line):
        """Use AI to phrase the response based on the query and the matched line."""
        print(f"Phrasing response with AI for: Query: {query_text}, Matched Line: {matched_line}")
        prompt = (
            f"You are assisting with questions about e-commerce."
            f"You are an intelligent assistant. A user has asked the question: '{query_text}'. "
            f"The most relevant information found is: '{matched_line}'. "
            f"Based on this information, generate a concise and accurate response."
        )

        # Use OpenAI LLM to phrase the response
        llm = OpenAI(temperature=0.0)
        response = llm(prompt)
        return response.strip()


