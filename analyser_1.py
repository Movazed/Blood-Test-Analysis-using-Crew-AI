import os
from crewai import Agent, Task, Crew
from PyPDF2 import PdfReader
from crewai_tools import SerperDevTool, WebsiteSearchTool
import openai

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

# Define GPT-3.5 chat completion function
def get_gpt35_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

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

# Define a function to use GPT-3.5 for summarizing, searching, and recommending
def use_gpt35_for_tasks():
    # Example task: Analyzing the report
    summary = get_gpt35_completion(f"Summarize the following blood test report:\n\n{extracted_text}")
    print("Summary:", summary)

    # Example task: Finding articles (This would require actual integration with search tools)
    # For demonstration purposes, we assume the tool returns a list of article titles
    articles = research_expert.perform_task(task_find_articles)
    print("Found Articles:", articles)

    # Example task: Providing recommendations
    recommendations = get_gpt35_completion(f"Provide health recommendations based on these articles:\n\n{articles}")
    print("Recommendations:", recommendations)

# Run the GPT-3.5 tasks
use_gpt35_for_tasks()

# Begin task execution
medical_crew.kickoff()
