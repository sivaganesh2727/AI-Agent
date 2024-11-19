AI Web Search Agent
This project is a Streamlit-based application that combines web scraping (via ScraperAPI), Google Sheets integration, and OpenAI's language model to fetch and analyze web search results. Users can upload data (CSV or Google Sheets), perform web searches, and update results back to Google Sheets.

Features
Upload Data: Supports CSV file uploads or Google Sheets for input data.
Web Search: Fetches web search results using ScraperAPI.
AI-Powered Analysis: Processes the scraped results using OpenAI's GPT model.
Google Sheets Integration: Reads from and writes back to Google Sheets.
Customizable Queries: Allows query customization with placeholders for entities.
Requirements
Python 3.8+
A valid ScraperAPI key.
A valid OpenAI API key.
A Google service account and its credentials.json file for accessing Google Sheets.

Installation
Clone the Repository:
git clone https://github.com/your-repo-name/ai-web-search-agent.git
cd ai-web-search-agent

Install Dependencies: Install all required Python libraries using:
pip install -r requirements.txt

Set Up Google Sheets Integration:

Create a Google service account and download the credentials.json file.
Place the credentials.json file in the root of your project directory.
Set API Keys:

Replace the placeholders for SCRAPERAPI_KEY and OPENAI_API_KEY in app.py (or set them as environment variables).

Usage
Run the Application: Start the Streamlit app:
streamlit run app.py

Upload or Connect Data:

Upload a CSV file or enter a Google Sheet name to load data.
Perform Web Searches:

Select a column with entities from the data.
Enter a query template using {entity} as a placeholder.
Analyze Results:

View the extracted information.
(Optional) Update results to Google Sheets.

File Structure

.
├── app.py # Main application file
├── websearch.py # Handles web search functionality
├── openai.py # Manages OpenAI API interactions
├── requirements.txt # Python dependencies
├── credentials.json # Google Sheets service account file (not included in repo)
└── README.md # Project documentation

Example
Query Template:
Get information about {entity}.

Input CSV:
Name
Google
OpenAI
Streamlit

Output: The app performs web searches for "Google," "OpenAI," and "Streamlit," processes results with OpenAI GPT, and displays or updates the data.

Environment Variables (Optional)
Set API keys as environment variables for security:
export SCRAPERAPI_KEY="your_scraperapi_key"
export OPENAI_API_KEY="your_openai_api_key"

Dependencies
See requirements.txt for a full list of dependencies.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Troubleshooting
Google Sheets Errors: Ensure the service account has access to the specified Google Sheets file.
ScraperAPI Errors: Verify your API key and usage limits.
OpenAI Errors: Ensure your API key is valid and has sufficient credits.
