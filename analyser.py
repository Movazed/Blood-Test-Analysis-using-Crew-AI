import os
from crewai import Agent, Task, Crew
from PyPDF2 import PdfReader
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Configure API keys for external tools
os.environ["SERPER_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

# Define the path to the PDF and the pages to extract
pdf_file_path = 'reports.pdf'
pages_to_extract = [1, 10]

def extract_text_from_pages(file_path, page_numbers):
    collected_text = ''
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_index in page_numbers:
            page = pdf_reader.pages[page_index - 1]
            text_content = page.extract_text()
            if text_content:
                collected_text += text_content
    return collected_text

extracted_text = extract_text_from_pages(pdf_file_path, pages_to_extract)
print(extracted_text)

# Initialize tools for searching
serper_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

# Create different agents with distinct roles and objectives
test_report_specialist = Agent(
    role='Test Report Specialist',
    goal='Examine the blood test report and provide a summary.',
    backstory='A specialist with expertise in analyzing blood test results.',
    verbose=True,
    allow_delegation=False
)

research_expert = Agent(
    role='Research Expert',
    goal='Find relevant health articles based on the test results.',
    backstory='A researcher skilled in locating health-related information.',
    tools=[serper_tool, web_search_tool],
    verbose=True,
    allow_delegation=False,
)

wellness_advisor = Agent(
    role='Wellness Advisor',
    goal='Offer health recommendations derived from the articles.',
    backstory='An advisor experienced in delivering health guidance.',
    verbose=True,
    allow_delegation=False,
)

# Define tasks to be handled by the agents
task_analyze_report = Task(
    description=f'Analyze the blood test report: "{extracted_text}"',
    expected_output='Summary of the blood test findings.',
    agent=test_report_specialist,
)

task_find_articles = Task(
    description='Look for health articles related to the blood test analysis.',
    expected_output='List of pertinent health articles with links.',
    agent=research_expert,
    context=[task_analyze_report]
)

task_provide_recommendations = Task(
    description='Generate health recommendations based on the identified articles.',
    expected_output='Health advice with links to relevant articles.',
    agent=wellness_advisor,
    context=[task_find_articles]
)

# Assemble and initiate the crew
medical_crew = Crew(
    agents=[test_report_specialist, research_expert, wellness_advisor],
    tasks=[task_analyze_report, task_find_articles, task_provide_recommendations],
    verbose=2
)

# Begin task execution
medical_crew.kickoff()
