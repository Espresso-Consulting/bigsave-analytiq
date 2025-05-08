# Procurement Recommendation Demo

This Streamlit application provides a demonstration of a procurement recommendation system. It allows users to view weekly sales data, generate purchase schedule recommendations, and interact with an AI Data Assistant to get insights from the displayed data.

## Features

- **Interactive Data Tables:** View Weekly Sales and Recommended Purchase Schedules using `st_aggrid`.
- **Parameter Selection:** Filter data by Branch and Sales Week.
- **View Toggling:** Switch between the Weekly Sales Report and the Purchase Schedule creation view.
- **AI Data Assistant:**
    - Chat with an AI (powered by Google Gemini) to discuss the data shown in the tables.
    - AI responses are based strictly on the context of the currently displayed table.
    - Chat history is maintained during the session.
- **Data Caching:**
    - BigQuery query results are cached to improve performance on repeated views.
    - LLM responses and data summaries for the AI chat are also cached.
    - Manual data refresh capability.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Espresso-Consulting/bigsave-analytiq.git
    cd bigsave-analytiq
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    - Create a `.env` file in the project root with the following content:
      ```
      GEMINI_API_KEY=your-gemini-api-key-here
      ```
    - Ensure your Google Cloud service account JSON key file is named `bigsave-6767d8651634.json` and is in the root directory (this file is excluded from git by `.gitignore`).

5.  **BigQuery Access:**
    - The service account must have access to your BigQuery dataset (`bigsave.demo`).

## Running the Application

Once the setup is complete, run the Streamlit app from your terminal:

```bash
streamlit run app.py
```

The application should open in your default web browser.

## Project Structure

- `app.py`: The main Streamlit application script.
- `.env`: Environment variables (not tracked by git).
- `bigsave-6767d8651634.json`: Google Cloud service account key (sensitive, not tracked by git).
- `requirements.txt`: Python dependencies.
- `PLANNING.md`: Project planning document.
- `TASK.md`: Task tracking document.
- `README.md`: This file.
- `venv/`: Python virtual environment directory (not tracked by git).
- `sample_data/`: (Local sample data, not tracked by git).

## Key Dependencies

- `streamlit`: For building the web application interface.
- `pandas`: For data manipulation.
- `google-cloud-bigquery`: For interacting with Google BigQuery.
- `google-generativeai`: For using the Gemini LLM.
- `st-aggrid`: For displaying interactive data tables.
- `python-dotenv`: For loading environment variables from `.env`.

## Notes

- Sensitive files and data (such as `.env`, service account keys, and sample data) are excluded from version control using `.gitignore`.
- See the [GitHub repository](https://github.com/Espresso-Consulting/bigsave-analytiq.git) for the latest code and updates. 