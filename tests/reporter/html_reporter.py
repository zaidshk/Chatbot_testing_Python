from pyhtmlreport import Report

class HTMLReporter:
    def __init__(self, report_path):
        self.report = Report()
        self.report_path = report_path
        self.report.setup_report("Chatbot Test Summary", self.report_path)

    def add_test_result(self, name, status, response_time):
        self.report.add_testcase(name, status, response_time)

    def finalize_report(self):
        self.report.generate_report()
