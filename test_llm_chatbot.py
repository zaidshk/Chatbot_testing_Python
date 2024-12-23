import pytest
import os

if __name__ == "__main__":
    # Ensure the reports directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # # Run predefined answers tests
    # print("Running predefined answers tests...")
    # pytest.main([
    #     "tests/TC01_test_chatbot_predefined_answers.py",
    #     "--html=reports/test_predefined_answers.html",
    #     "--self-contained-html"
    # ])
    #
    # # Run relevance answers tests
    # print("Running relevance answers tests...")
    # pytest.main([
    #     "tests/TC02_test_chatbot_relevance_answers.py",
    #     "--html=reports/test_relevance_answers.html",
    #     "--self-contained-html"
    # ])

    # Run single thread/session performance test against the chatbot AI
    print("Running performance tests")
    pytest.main([
        "tests/TC03_test_chatbot_performance.py",
        "--html=reports/test_chatbot_performance.html",
        "--self-contained-html"
    ])

