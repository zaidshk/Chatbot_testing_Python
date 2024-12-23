import threading
import pytest
import os

def run_performance_test(session_name):
    """Run the performance test session."""
    print(f"Starting {session_name}")
    pytest.main([
        "tests/TC04_test_chatbot_performance_parallel.py",
        "--html=reports/test_chatbot_performance_parallel_session" + session_name + ".html",
        "--self-contained-html"
    ])
    print(f"Finished {session_name}")

if __name__ == "__main__":
    # Ensure the reports directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Create two threads for performance testing
    thread1 = threading.Thread(target=run_performance_test, args=("session1",))
    thread2 = threading.Thread(target=run_performance_test, args=("session2",))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

    print("Performance testing completed.")
