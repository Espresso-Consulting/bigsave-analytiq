# TASK.md

This document tracks the tasks for the Procurement Recommendation Demo project.

## Completed Tasks

- **Initial Setup & Core Functionality**
    - [x] `YYYY-MM-DD`: Setup basic Streamlit app structure.
    - [x] `YYYY-MM-DD`: Implement BigQuery data retrieval functions for sales, stock, suppliers, and item details.
    - [x] `YYYY-MM-DD`: Create Weekly Sales Table view with `st_aggrid`.
    - [x] `YYYY-MM-DD`: Create Purchase Schedule recommendation view with `st_aggrid`.
    - [x] `YYYY-MM-DD`: Implement toggle functionality between Weekly Sales and Purchase Schedule views.
    - [x] `YYYY-MM-DD`: Add sidebar controls for Branch and Sales Week selection.
- **AI Data Assistant**
    - [x] `YYYY-MM-DD`: Implement AI Data Assistant chat UI in a right-hand column.
    - [x] `YYYY-MM-DD`: Integrate Google Gemini (`gemini-1.5-flash`) for chat responses.
    - [x] `YYYY-MM-DD`: Restrict AI responses to the context of the currently displayed table data.
    - [x] `YYYY-MM-DD`: Store and display chat history within the session.
    - [x] `YYYY-MM-DD`: Refine chat UI to be more traditional (input at bottom, scrollable history, user/AI alignment, modern icons).
- **Performance & UX**
    - [x] `YYYY-MM-DD`: Implement caching for BigQuery data retrieval functions (`@st.cache_data`).
    - [x] `YYYY-MM-DD`: Implement caching for AI context summaries and LLM responses (`@st.cache_data`).
    - [x] `YYYY-MM-DD`: Add a manual "Refresh Data" button to clear caches.
    - [x] `YYYY-MM-DD`: Display a "Last data refresh" timestamp.
    - [x] `YYYY-MM-DD`: Ensure chat input bar is always visible and chat history scrolls correctly.

## Pending Tasks / To Do

- **Refinements & Enhancements**
    - [x] 2024-06-10: Enable AI Data Assistant to answer questions about suppliers (by name or ID) and products, not just sales data. Adjust context and retrieval logic as needed.
    - [ ] `YYYY-MM-DD`: Further refine AI Data Assistant UI (e.g., auto-scroll to latest message, better loading/error states for AI response).
    - [ ] `YYYY-MM-DD`: Enhance context provided to the AI (e.g., include more details from the `display_df` or even full DataFrame if token limits allow, or use vector search for larger contexts).
    - [ ] `YYYY-MM-DD`: Improve error handling for BigQuery queries and AI API calls (show user-friendly messages).
    - [ ] `YYYY-MM-DD`: Add loading spinners for long-running operations (BigQuery queries, initial AI response).
- **Code Quality & Best Practices**
    - [x] 2025-05-08: Secure API Keys: Move hardcoded `SERVICE_ACCOUNT_JSON` path and `GEMINI_API_KEY` to environment variables or a `.env` file.
    - [ ] `YYYY-MM-DD`: Add comprehensive docstrings for all functions following Google style (as per global rules).
    - [x] 2025-05-08: Create `requirements.txt` based on actual final imports.
    - [x] 2025-05-08: Add `.gitignore` and clean repo to remove large/sensitive files from git history.
- **Testing (as per Global Rules)**
    - [ ] `YYYY-MM-DD`: Create Pytest unit tests for data retrieval functions (mocking BigQuery client).
    - [ ] `YYYY-MM-DD`: Create Pytest unit tests for data processing logic in Purchase Schedule.
    - [ ] `YYYY-MM-DD`: Create Pytest unit tests for AI chat logic (mocking Gemini API).
    - [ ] `YYYY-MM-DD`: Ensure tests cover expected use, edge cases, and failure cases.
- **Deployment Considerations (Future)**
    - [x] 2024-06-09: Deploy to Streamlit Community Cloud and document secrets handling (GEMINI_API_KEY, GOOGLE_SERVICE_ACCOUNT_JSON) in README and PLANNING.md.

## Discovered During Work

*(This section can be used to note down any new tasks, bugs, or ideas that come up during development.)*

- `YYYY-MM-DD`: Streamlit versioning issue with `st.experimental_rerun` vs `st.rerun` (Resolved by using `st.rerun`).
- `YYYY-MM-DD`: Initial `NameError` for `display_df` due to AI chat code placement (Resolved by reordering and conditional rendering).
- 2025-05-08: Large file in git history caused GitHub push to fail; resolved by cleaning repo, updating `.gitignore`, and force-pushing a clean initial commit.
- 2024-06-09: Updated documentation to clarify Streamlit Cloud deployment and secrets management. Fixed issues with environment variable loading and BigQuery/Gemini integration on cloud.
- 2024-06-10: If more supplier/product fields are needed for richer AI answers, consider expanding the context with additional columns from the stock and suppliers tables.

*(Please replace `YYYY-MM-DD` with the actual dates as you work on these tasks.)* 