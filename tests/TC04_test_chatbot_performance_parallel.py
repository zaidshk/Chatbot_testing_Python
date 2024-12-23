import pytest
import json
from chatbot.chatbot import Chatbot
import config
import time

# Load test data
with open("tests/test_data_performance_testing.json") as f:
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
def test_performance(chatbot, case):
    """OBJECTIVE: Test chatbot responses for performance in parallel chatbot session."""
    query = case["query"] # Input query
    expected_output = " "
    max_response_time = case["max_response_time_parallel"]

    start_time = time.time()
    response, rating = chatbot.query(query, expected_output)
    response_time = time.time() - start_time

    print(f"AI Response: {response}")
    print(f"AI Response time: {response_time} Maximum Response time: {max_response_time}")


    # Validate response time based on the max_response_time_parallel criteria mentioned in the test data json file,
    ## Simple query- 4 seconds
    ## Complex query - 10 seconds
    assert response_time <= max_response_time, (
        f"Response time {response_time}s exceeded the limit of {max_response_time}s"
    )
