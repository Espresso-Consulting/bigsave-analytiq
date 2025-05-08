import os
import streamlit as st
print("Streamlit version:", st.__version__)
from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder
import google.generativeai as genai
from dotenv import load_dotenv

# Path to your service account key
SERVICE_ACCOUNT_JSON = 'bigsave-6767d8651634.json'
PROJECT_ID = 'bigsave'
DATASET = 'demo'

# Set up BigQuery client
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

load_dotenv()

@st.cache_data
def get_branches():
    query = f"""
        SELECT DISTINCT branch FROM `{PROJECT_ID}.{DATASET}.sales`
        WHERE branch IS NOT NULL
        ORDER BY branch
    """
    df = client.query(query).to_dataframe()
    return df['branch'].tolist()

@st.cache_data
def get_weeks():
    query = f"""
        SELECT DISTINCT FORMAT_DATE('%Y-%W', PARSE_DATE('%Y-%m-%d', TranDate)) AS week
        FROM `{PROJECT_ID}.{DATASET}.sales`
        WHERE TranDate IS NOT NULL
        ORDER BY week DESC
    """
    df = client.query(query).to_dataframe()
    return df['week'].dropna().tolist()

@st.cache_data
def get_sales_by_stockid(branch, week):
    query = f"""
        SELECT REGEXP_EXTRACT(StockID, r'([0-9]+(?:-[0-9]+)?)') AS StockID, SUM(CAST(Quantity AS FLOAT64)) AS total_qty
        FROM `{PROJECT_ID}.{DATASET}.sales`
        WHERE branch = @branch
          AND FORMAT_DATE('%Y-%W', PARSE_DATE('%Y-%m-%d', TranDate)) = @week
        GROUP BY StockID
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('branch', 'STRING', branch),
            bigquery.ScalarQueryParameter('week', 'STRING', week)
        ]
    )
    df = client.query(query, job_config=job_config).to_dataframe()
    return df

@st.cache_data
def get_stock_onhand_by_stockid(branch):
    query = f"""
        SELECT REGEXP_EXTRACT(StockCodeID, r'([0-9]+)') AS StockID, ONHAND
        FROM `{PROJECT_ID}.{DATASET}.stock_onhands`
        WHERE BRANCH = @branch
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('branch', 'STRING', branch)
        ]
    )
    df = client.query(query, job_config=job_config).to_dataframe()
    return df

@st.cache_data
def get_item_names_by_stockid(stockids):
    if not stockids:
        return pd.DataFrame(columns=['StockID', 'Description1'])
    codes_str = ','.join([f'"{code}"' for code in stockids])
    query = f"""
        SELECT StockID, Description1
        FROM `{PROJECT_ID}.{DATASET}.stock`
        WHERE StockID IN ({codes_str})
    """
    df = client.query(query).to_dataframe()
    return df

@st.cache_data
def get_item_details_by_stockid(stockids):
    if not stockids:
        return pd.DataFrame(columns=[
            'StockID', 'Description1', 'SupplierID', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand'
        ])
    codes_str = ','.join([f'"{code}"' for code in stockids])
    query = f'''
        SELECT StockID, Description1, SupplierID, Cat0, Cat1, Cat2, Cat3, Cat4, Brand
        FROM `{PROJECT_ID}.{DATASET}.stock`
        WHERE StockID IN ({codes_str})
    '''
    df = client.query(query).to_dataframe()
    return df

@st.cache_data
def get_supplier_names_by_ids(supplier_ids):
    if not supplier_ids:
        return pd.DataFrame(columns=['SupplierID', 'SupplierName'])
    ids_str = ','.join([f'"{sid}"' for sid in supplier_ids])
    query = f'''
        SELECT SupplierID, SupplierName
        FROM `{PROJECT_ID}.{DATASET}.suppliers`
        WHERE SupplierID IN ({ids_str})
    '''
    df = client.query(query).to_dataframe()
    return df

@st.cache_data
def get_weekly_sales_table(week):
    """
    Returns a DataFrame with StockID, Name (Description1), Quantity sold, and LinkQty for the given week (all branches), only for items that sold.
    """
    query = f"""
        SELECT
            REGEXP_EXTRACT(s.StockID, r'(\\d+)') AS StockID,
            st.Description1 AS Name,
            SUM(CAST(s.Quantity AS FLOAT64)) AS Quantity_Sold,
            SUM(CAST(s.LinkQty AS FLOAT64)) AS LinkQty_Sold
        FROM `{PROJECT_ID}.{DATASET}.sales` s
        JOIN `{PROJECT_ID}.{DATASET}.stock` st
          ON REGEXP_EXTRACT(s.StockID, r'(\\d+)') = st.StockID
        WHERE FORMAT_DATE('%Y-%W', PARSE_DATE('%Y-%m-%d', s.TranDate)) = @week
          AND CAST(s.Quantity AS FLOAT64) > 0
        GROUP BY StockID, st.Description1
        HAVING SUM(CAST(s.Quantity AS FLOAT64)) > 0
        ORDER BY Quantity_Sold DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('week', 'STRING', week)
        ]
    )
    df = client.query(query, job_config=job_config).to_dataframe()
    return df

@st.cache_data
def get_context_summary(display_df, show_schedule, week, branch):
    """
    Returns a string summary of the current data context, including a mapping of product names to sales for the week.
    """
    if not show_schedule:
        # Build a mapping of product names to sales quantities
        name_qty = display_df[['Item Name', 'Quantity Sold']].set_index('Item Name')['Quantity Sold'].to_dict()
        # Also include a list of all product names for fuzzy matching
        all_names = list(name_qty.keys())
        return (
            f"Weekly Sales Table for week {week} at branch {branch}.\n"
            f"Top items by quantity sold: {display_df[['Item Name', 'Quantity Sold']].head(5).to_dict(orient='records')}\n"
            f"Total items: {len(display_df)}\n"
            f"Product sales mapping: {name_qty}\n"
            f"All product names: {all_names}"
        )
    else:
        # For purchase schedule, include order qty mapping
        name_order = display_df[['Item Name', 'Order Qty']].set_index('Item Name')['Order Qty'].to_dict()
        all_names = list(name_order.keys())
        return (
            f"Purchase Schedule for branch {branch}.\n"
            f"Top recommended orders: {display_df[['Item Name', 'Order Qty']].head(5).to_dict(orient='records')}\n"
            f"Total items: {len(display_df)}\n"
            f"Product order mapping: {name_order}\n"
            f"All product names: {all_names}"
        )

@st.cache_data
def get_ai_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(prompt).text

# Streamlit UI
st.set_page_config(page_title='Procurement Demo', layout='wide')
st.title('Procurement Recommendation Demo')

with st.sidebar:
    if 'last_refresh' not in st.session_state:
        from datetime import datetime
        st.session_state['last_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if st.button('🔄 Refresh Data', use_container_width=True):
        st.cache_data.clear()
        from datetime import datetime
        st.session_state['last_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.rerun()
    st.markdown(f"<small>Last data refresh: <b>{st.session_state['last_refresh']}</b></small>", unsafe_allow_html=True)
    st.header('Select Parameters')
    # Initialize show_schedule before any access
    if 'show_schedule' not in st.session_state:
        st.session_state['show_schedule'] = False

    branches = get_branches()
    branch = st.selectbox('Branch', branches)
    weeks = get_weeks()
    # Only show week selection if not in Purchase Schedule view
    if not st.session_state['show_schedule']:
        week = st.selectbox('Sales Week (YYYY-WW)', weeks)
    else:
        # Keep week variable defined for downstream logic
        week = weeks[0] if weeks else None

    def toggle_schedule():
        st.session_state['show_schedule'] = not st.session_state['show_schedule']

    toggle_label = 'Show Weekly Sales Report' if st.session_state['show_schedule'] else 'Create Purchase Schedule'
    st.button(toggle_label, key='toggle_button', use_container_width=True, on_click=toggle_schedule)

# Main layout: left sidebar, main data area, right AI chat
main_col, ai_col = st.columns([3, 1.5], gap="large")

# Apply background color to the entire AI column
st.markdown(
    """
    <style>
    /* Target the second column (AI column) root */
    section.main > div > div > div:nth-child(2) {
        background: #eaf0fb !important;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(60, 100, 180, 0.07);
        min-height: 700px;
        padding-top: 1.5em;
        padding-bottom: 1.5em;
    }
    /* Target the first column (main table area) root */
    section.main > div > div > div:nth-child(1) {
        background: #f8fafc !important;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(60, 100, 180, 0.04);
        min-height: 700px;
        padding-top: 1.5em;
        padding-bottom: 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with main_col:
    if branch and week:
        if not st.session_state['show_schedule']:
            st.success('**Currently viewing: Weekly Sales Table**')
            st.subheader(f'Weekly Sales Table (All Branches) for Week: {week}')
            weekly_sales_df = get_weekly_sales_table(week)
            item_details_df = get_item_details_by_stockid(weekly_sales_df['StockID'].unique().tolist())
            supplier_ids = item_details_df['SupplierID'].dropna().unique().tolist()
            supplier_names_df = get_supplier_names_by_ids(supplier_ids)
            weekly_sales_df = weekly_sales_df.merge(item_details_df, on='StockID', how='left')
            weekly_sales_df = weekly_sales_df.merge(supplier_names_df, on='SupplierID', how='left')
            group_cols = ['SupplierName', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand']
            display_cols = [
                'SupplierName', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand',
                'StockID', 'Name', 'Quantity_Sold', 'LinkQty_Sold'
            ]
            display_df = weekly_sales_df[display_cols].rename(columns={
                'Name': 'Item Name',
                'Quantity_Sold': 'Quantity Sold',
                'LinkQty_Sold': 'LinkQty'
            })
            gb = GridOptionsBuilder.from_dataframe(display_df)
            gb.configure_default_column(groupable=True)
            gb.configure_column('SupplierName', rowGroup=True, hide=True)
            gb.configure_column('Cat0', rowGroup=True, hide=True)
            gb.configure_column('Cat1', rowGroup=True, hide=True)
            gb.configure_column('Cat2', rowGroup=True, hide=True)
            gb.configure_column('Cat3', rowGroup=True, hide=True)
            gb.configure_column('Cat4', rowGroup=True, hide=True)
            gb.configure_column('Brand', rowGroup=True, hide=True)
            gb.configure_side_bar()
            gb.configure_grid_options(domLayout='normal')
            grid_options = gb.build()
            AgGrid(
                display_df,
                gridOptions=grid_options,
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True,
                height=600,
            )
        else:
            st.info('**Currently viewing: Purchase Schedule**')
            st.subheader('Recommended Purchase Schedule for Next Week')
            st.caption('Based on average sales of the last 4 weeks minus current stock on hand (negative stock treated as zero).')
            week_index = weeks.index(week)
            prev_weeks = weeks[week_index+1:week_index+5] if week_index+5 <= len(weeks) else weeks[week_index+1:]
            if len(prev_weeks) < 1:
                st.warning('Not enough historical data to calculate running average.')
                display_df = None
            else:
                prev_sales = []
                for w in prev_weeks:
                    df = get_sales_by_stockid(branch, w)
                    df = df.rename(columns={'total_qty': w})
                    prev_sales.append(df.set_index('StockID'))
                if prev_sales:
                    sales_hist = pd.concat(prev_sales, axis=1).fillna(0)
                    sales_hist['avg_sales'] = sales_hist.mean(axis=1)
                    stock_onhand_df = get_stock_onhand_by_stockid(branch)
                    stock_onhand_df['ONHAND'] = pd.to_numeric(stock_onhand_df['ONHAND'], errors='coerce').fillna(0)
                    stock_onhand_df['ONHAND'] = stock_onhand_df['ONHAND'].clip(lower=0)
                    schedule = sales_hist.reset_index().merge(stock_onhand_df, on='StockID', how='left')
                    schedule['ONHAND'] = schedule['ONHAND'].fillna(0)
                    schedule['RecommendedOrder'] = (schedule['avg_sales'] - schedule['ONHAND']).clip(lower=0)
                    item_details_df = get_item_details_by_stockid(schedule['StockID'].unique().tolist())
                    schedule = schedule.merge(item_details_df, on='StockID', how='left')
                    supplier_ids = schedule['SupplierID'].dropna().unique().tolist()
                    supplier_names_df = get_supplier_names_by_ids(supplier_ids)
                    schedule = schedule.merge(supplier_names_df, on='SupplierID', how='left')
                    group_cols = ['SupplierName', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand']
                    schedule = schedule.sort_values(group_cols + ['Description1'])
                    display_cols = [
                        'SupplierName', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand',
                        'StockID', 'Description1', 'avg_sales', 'ONHAND', 'RecommendedOrder'
                    ]
                    display_df = schedule[display_cols].rename(columns={
                        'Description1': 'Item Name',
                        'avg_sales': 'Avg Weekly Sales',
                        'ONHAND': 'Stock On Hand',
                        'RecommendedOrder': 'Order Qty'
                    })
                    gb = GridOptionsBuilder.from_dataframe(display_df)
                    gb.configure_default_column(groupable=True)
                    gb.configure_column('SupplierName', rowGroup=True, hide=True)
                    gb.configure_column('Cat0', rowGroup=True, hide=True)
                    gb.configure_column('Cat1', rowGroup=True, hide=True)
                    gb.configure_column('Cat2', rowGroup=True, hide=True)
                    gb.configure_column('Cat3', rowGroup=True, hide=True)
                    gb.configure_column('Cat4', rowGroup=True, hide=True)
                    gb.configure_column('Brand', rowGroup=True, hide=True)
                    gb.configure_side_bar()
                    gb.configure_grid_options(domLayout='normal')
                    grid_options = gb.build()
                    AgGrid(
                        display_df,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,
                        allow_unsafe_jscode=True,
                        height=600,
                    )
                else:
                    display_df = None
    else:
        st.info('Please select a branch and week to view data.')

with ai_col:
    st.markdown(
        '<span style="font-size:1.2em;font-weight:600;white-space:nowrap;">💬 Data Assistant</span>',
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if 'display_df' in locals() and display_df is not None:
        context_summary = get_context_summary(display_df, st.session_state['show_schedule'], week, branch)

        # Fixed height, scrollable chat history container
        chat_height = 400  # px, adjust as needed
        with st.container(height=chat_height, border=True):
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"], avatar=msg.get("avatar")):
                    st.markdown(msg["content"])

        # Chat input always at the bottom of the column
        user_input = st.chat_input("Ask about the data above...", key="data_chat_input")
        if user_input:
            # Load Gemini API key from environment variable (set in .env file)
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            prompt = (
                "You are a helpful data assistant. "
                "Answer the user's question in clear, natural language, using only the data provided below. "
                "If the answer is not in the data, say you don't know. "
                "If the user asks about a product by name (e.g. 'Tastic Rice'), match it to the closest product name in the product sales mapping (using substring or fuzzy match if needed). "
                "If the user asks about a generic product (e.g. 'Tastic Rice'), show all matching products and their sales. "
                "If the user asks about a specific product (e.g. 'Tastic 10kg'), show just that product's sales. "
                f"Data context:\n{context_summary}\n"
                f"User question: {user_input}"
            )
            response = get_ai_response(prompt, GEMINI_API_KEY)
            st.session_state["chat_history"].append({"role": "user", "content": user_input, "avatar": "🧑"})
            st.session_state["chat_history"].append({"role": "assistant", "content": response, "avatar": "💡"})
            st.rerun()
    else:
        st.info("No data available for chat.")
