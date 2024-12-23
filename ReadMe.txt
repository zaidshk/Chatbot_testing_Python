## Project Overview
This project focuses on automating the functional, Relevance Accuracy and performance testing of an AI-powered chatbot tailored for an e-commerce domain.
The chatbot utilizes Retrieval-Augmented Generation (RAG) to deliver accurate and relevant responses by integrating knowledge from predefined "golden answers" and a comprehensive RAG document.
The scope includes functional validation, response quality evaluation, and performance testing.


---

Github Link - https://github.com/zaidshk/Chatbot_testing_Python
---

## Project Structure

LLM_chatbot_testing/
│
├── chatbot/                        # Contains chatbot implementation
│   ├── __init__.py
│   ├── chatbot.py                  # Core chatbot implementation
│
├── logs/                           # Stores logs generated during test runs
│
├── reports/                        # Stores test reports in HTML format
│   ├── test_predefined_answers.html
│   ├── test_relevance_answers.html
│   ├── test_chatbot_performance.html
│   ├── test_chatbot_performance_parallel_session1.html
│   ├── test_chatbot_performance_parallel_session2.html
│
├── tests/                          # Test cases for chatbot
│   ├── TC01_test_chatbot_predefined_answers.py  # Functional tests
│   ├── TC02_test_chatbot_relevance_answers.py   # Response quality tests
│   ├── TC03_test_chatbot_performance.py         # Single session performance tests
│   ├── TC04_test_chatbot_performance_parallel.py # Parallel performance tests
│   ├── reporter/                   # HTML Reporter Module
│       ├── html_reporter.py
│   ├── test_data_predefined_answers.json        # Predefined answers test data
│   ├── test_data_relevance_answers.json         # Relevance test data
│   ├── test_data_performance_testing.json       # Performance test data
│
├── golden_answers.txt              # Contains golden answers
├── e_commerce_RAG_doc.txt          # RAG document for e-commerce knowledge
├── requirements.txt                # Python dependencies
├── config.py                       # Configuration for API keys and file paths
├── test_llm_chatbot.py             # Test runner for functional tests
├── test_llm_chatbot_performance.py # Parallel performance test runner


---

## Project Requirements

### Dependencies
The project requires the following Python packages:
- `langchain`
- `openai`
- `faiss-cpu`
- `sentence_transformers`
- `pytest`
- `pytest-html`
- `pytest-xdist`
- `pyhtmlreport`
- `pandas`
- `tiktoken`

Install dependencies using:
pip install -r requirements.txt


##Files
Golden Answers Document:

golden_answers.txt: Contains predefined responses for frequently asked questions.
RAG Document:

e_commerce_RAG_doc.txt: Contains detailed e-commerce-related information for RAG.
Configuration:

config.py: Configures API keys and file paths.


---

##Test Suite
1. Functional Testing
Objective: Validate the correctness of predefined chatbot responses.

Test file: TC01_test_chatbot_predefined_answers.py
Test data: test_data_predefined_answers.json
Output: test_predefined_answers.html
2. Response Quality Testing
Objective: Validate the relevance and accuracy of responses to various queries, including complex edge cases.

Test file: TC02_test_chatbot_relevance_answers.py
Test data: test_data_relevance_answers.json
Output: test_relevance_answers.html
3. Performance Testing
Objective: Measure response times and validate performance under load.

Single Session:

Test file: TC03_test_chatbot_performance.py
Test data: test_data_performance_testing.json
Output: test_chatbot_performance.html
Parallel Execution:

Test file: TC04_test_chatbot_performance_parallel.py
Test data: test_data_performance_testing.json
Output:
test_chatbot_performance_parallel_session1.html
test_chatbot_performance_parallel_session2.html

---

##Execution

Functional and Relevance Tests
Run all functional and relevance tests:  python test_llm_chatbot.py

Performance Tests
Single Session: pytest tests/TC03_test_chatbot_performance.py --html=reports/test_chatbot_performance.html --self-contained-html

Parallel Execution: python test_llm_chatbot_performance.py
