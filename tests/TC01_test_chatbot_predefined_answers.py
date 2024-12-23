import pytest
import json
from chatbot.chatbot import Chatbot
import config
import time

# Load test data
with open("tests/test_data_predefined_answers.json") as f:
    test_cases = json.load(f)

@pytest.fixture
def chatbot():
    """Fixture to initialize the chatbot."""
    return Chatbot(
        api_key=config.API_KEY,
        golden_answers_path=config.GOLDEN_ANSWERS,
        rag_doc_path="e_commerce_RAG_doc.txt"
    )

@pytest.mark.parametrize("case", test_cases)
def test_predefined_answers(chatbot, case):
    """OBJECTIVE: Test chatbot responses for accuracy and rating."""
    query = case["query"] # input query
    expected_output = case["expected_output"]

    response, rating = chatbot.query(query,expected_output)

    print(f"AI Response: {response}")

    # Validate response rating, Rating 3 Accuracy 8/10, Rating 2 Accuracy 4/10 , Rating 1 Accuracy 1/10
    if rating == 3:  # High accuracy
        assert response.strip() == expected_output.strip(), (
            f"Expected '{expected_output}', but got '{response}'"
        )
    elif rating == 2:  # Average accuracy
        pytest.xfail(f"Average response for '{query}': {response}")
    else:  # Low accuracy
        pytest.fail(f"Low accuracy for '{query}': {response}")

