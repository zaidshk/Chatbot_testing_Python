import pytest
import json
from chatbot.chatbot import Chatbot
import config
import time

# Load test data
with open("tests/test_data_relevance_answers.json") as f:
    test_cases = json.load(f)

@pytest.fixture
def chatbot():
    """Fixture to initialize the chatbot."""
    return Chatbot(
        api_key=config.API_KEY,
        golden_answers_path=config.GOLDEN_ANSWERS,
        rag_doc_path=config.RAG_doc
    )

@pytest.mark.parametrize("case", test_cases)
def test_relevance_answers(chatbot, case):
    """OBJECTIVE: Test chatbot responses for accuracy and rating."""
    query = case["query"] # Input query
    expected_output = case["expected_output"]

    response, rating = chatbot.query(query, expected_output)

    print(f"AI Response: {response}")

    # Validate response rating, Rating 3 Accuracy 8/10, Rating 2 Accuracy 4/10 , Rating 1 Accuracy 1/10
    if rating == 3:  # High accuracy
        assert True, f"Test passed for query: {query} with response: {response}"
    elif rating == 2:  # Average accuracy
        pytest.xfail(f"Average response for '{query}': {response}")
    else:  # Low accuracy
        pytest.fail(f"Low accuracy for '{query}': {response}")
