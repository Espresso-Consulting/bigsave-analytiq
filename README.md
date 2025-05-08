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

1.  **Clone the repository (if applicable) or ensure you have all project files.**

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content (or add to your existing one):
    ```txt
    streamlit
    pandas
    google-cloud-bigquery
    google-generativeai
    st-aggrid
    # Add other specific versions if known or necessary
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Google Cloud Credentials:**
    - Ensure you have a Google Cloud service account JSON key file named `bigsave-6767d8651634.json` in the root of the project directory, or update the `SERVICE_ACCOUNT_JSON` variable in `app.py` to point to its location.
    - This service account needs permissions to access your BigQuery dataset (`bigsave.demo`).

5.  **Configure Gemini API Key:**
    - The application uses a Google Gemini API key. Currently, this key is hardcoded in `app.py`:
      `GEMINI_API_KEY = "AIzaSyARy_krVAWwZja4UkGFNROkcKFpqYmCQ6Q"`
    - **For security, it is strongly recommended to move this key to an environment variable** or a more secure configuration method, especially if deploying or sharing the application.
      Example: Set an environment variable `GEMINI_API_KEY` and modify `app.py` to read `os.getenv("GEMINI_API_KEY")`.

## Running the Application

Once the setup is complete, run the Streamlit app from your terminal:

```bash
streamlit run app.py
```

The application should open in your default web browser.

## Project Structure

- `app.py`: The main Streamlit application script.
- `bigsave-6767d8651634.json`: Google Cloud service account key (sensitive, manage securely).
- `Espresso Test Data.xlsx`: (Assumed to be source data for BigQuery tables, not directly used by `app.py`).
- `list_excel_sheets.py`: (Assumed to be a utility script, not directly used by `app.py`).
- `upload_to_bigquery.py`: (Assumed to be a utility script for populating BigQuery, not directly used by `app.py`).
- `PLANNING.md`: Project planning document.
- `TASK.md`: Task tracking document.
- `README.md`: This file.
- `venv/`: Python virtual environment directory.

## Key Dependencies

- `streamlit`: For building the web application interface.
- `pandas`: For data manipulation.
- `google-cloud-bigquery`: For interacting with Google BigQuery.
- `google-generativeai`: For using the Gemini LLM.
- `st-aggrid`: For displaying interactive data tables. 