# Blood-Test-Analysis-using-Crew-AI
=======
# Blood Test Analysis and Health Recommendations Workflow

This notebook demonstrates a workflow for analyzing a blood test report, searching for relevant health articles, and providing health recommendations based on those articles.

## Steps to Execute the Workflow

### 1. Setup

First, ensure you have the necessary libraries and API keys configured. You will need to install the required Python packages and set up environment variables for API keys.

**API Keys Configuration**

- `SERPER_API_KEY`: For the Serper search tool.
- `OPENAI_API_KEY`: For OpenAI services.

```python
import os
from crewai import Agent, Task, Crew
from PyPDF2 import PdfReader
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Configure API keys for external tools
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"


This Markdown provides a comprehensive guide on how to use the code, including setup instructions, code cells, and additional information about required libraries and documentation.
>>>>>>> 5e46b31 (The commit)
