# PLANNING.md

## Project Goal

To develop a "Procurement Recommendation Demo" application. This application will allow users to:
- View weekly sales data and purchase recommendations.
- Interact with an AI Data Assistant to get insights from the displayed data.
- Select different branches and sales weeks to analyze.

## Architecture

- **Frontend:** Streamlit
- **Backend Data Source:** Google BigQuery
- **AI Language Model:** Google Gemini (specifically `gemini-1.5-flash`)
- **Data Tables:** `st_aggrid` for interactive and groupable tables.

## Style & Conventions

- **Language:** Python 3.x
- **Formatting:** PEP8, `black` (implied by global rules, good to note)
- **Type Hints:** Used throughout the codebase.
- **Data Validation:** (Currently not explicitly using Pydantic, but could be added if forms or complex inputs are introduced)
- **Modularity:** Aim for functions and logical separation of concerns. As per global rules, files should not exceed 500 lines.

## Key Features

- **Data Visualization:**
    - Weekly Sales Table (all branches, for a selected week).
    - Recommended Purchase Schedule (based on historical sales and stock on hand for a selected branch).
- **Interactive Controls:**
    - Branch selection.
    - Sales week selection.
    - Toggle between "Weekly Sales Report" and "Create Purchase Schedule" views.
    - Manual data refresh button.
- **AI Data Assistant:**
    - Conversational interface in a right-hand column.
    - Answers questions based *only* on the currently displayed table data.
    - Caches LLM responses and data context for speed.

## Data Sources (BigQuery Tables)

- `sales`: Transactional sales data.
- `stock_onhands`: Current stock levels.
- `stock`: Item master data (descriptions, categories, supplier IDs).
- `suppliers`: Supplier master data.

## Constraints & Considerations

- **API Key Management:**
    - `SERVICE_ACCOUNT_JSON` for BigQuery.
    - `GEMINI_API_KEY` for the AI assistant.
    - These are currently hardcoded but should be moved to environment variables or a secure config management solution for production.
- **Caching:**
    - Data retrieval functions (BigQuery queries) are cached using `st.cache_data`.
    - LLM responses and context summaries are also cached.
    - Manual data refresh clears these caches.
- **Error Handling:** Basic error handling (e.g., "No data available") is in place, can be expanded.
- **Scalability:** For a demo, current approach is fine. For larger scale, consider more robust backend API, database optimizations, and potentially more advanced state management.
- **Security:** As this is a demo, security aspects like input sanitization for SQL (though parameters are used) or XSS in chat (markdown is used) are minimal. For production, these would need careful review. 