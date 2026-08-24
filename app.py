# =====================================================================
# IMPORTING REQUIRED LIBRARIES
# =====================================================================
import streamlit as st          
import pandas as pd             
import requests                 
import plotly.express as px  
import datetime   
import os                       
from dotenv import load_dotenv  

# Load the secret environment variables from the .env file
load_dotenv()

# =====================================================================
# MODULE 1: DATA FETCHING (API CONNECTION)
# =====================================================================
@st.cache_data
def fetch_data(selected_date):
    API_URL = os.getenv("SUPABASE_API_URL")
    API_KEY = os.getenv("SUPABASE_API_KEY")
    
    if not API_URL or not API_KEY:
        st.error("API credentials missing! Please check your .env file.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {"report_date": selected_date}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()[0] 
        df_daily = pd.DataFrame(data.get("daily_metrics", []))
        df_monthly = pd.DataFrame(data.get("monthly_metrics", []))
        df_kpi = pd.DataFrame(data.get("kpi_cards", []))
        df_leaderboard = pd.DataFrame(data.get("leaderboard_metrics", []))
        df_customers = pd.DataFrame(data.get("customer_metrics", [])) 
        return df_daily, df_monthly, df_kpi, df_leaderboard, df_customers
    else:
        st.error(f"Failed to fetch data. Status: {response.status_code}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# =====================================================================
# MODULE 2: DATA CLEANING
# =====================================================================
def clean_data(df_daily, df_monthly, df_leaderboard, df_customers):
    df_daily['order_date'] = pd.to_datetime(df_daily['order_date'])
    df_daily = df_daily.sort_values('order_date')
    
    if not df_monthly.empty:
        df_monthly['date'] = pd.to_datetime(
            df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str) + '-01'
        )
        df_monthly['month_name'] = df_monthly['date'].dt.strftime('%b %Y')
        df_monthly = df_monthly.sort_values('date')
        
    df_leaderboard = df_leaderboard.sort_values(by="mtd_revenue", ascending=False).head(10)
    current_length = len(df_leaderboard)
    if current_length < 10:
        empty_rows = pd.DataFrame({
            "sales_representative": ["-"] * (10 - current_length),
            "today_sales": [0] * (10 - current_length),
            "today_revenue": [0.0] * (10 - current_length),
            "mtd_sales": [0] * (10 - current_length),
            "mtd_revenue": [0.0] * (10 - current_length)
        })
        df_leaderboard = pd.concat([df_leaderboard, empty_rows], ignore_index=True)
    df_leaderboard.insert(0, "Rank", range(1, 11))

    if not df_customers.empty:
        df_customers = df_customers.sort_values(by="amount_paid", ascending=False)
        df_customers.insert(0, "Customer Rank", range(1, len(df_customers) + 1))
        
    return df_daily, df_monthly, df_leaderboard, df_customers

# =====================================================================
# MODULE 3: DASHBOARD UI & LAYOUT
# =====================================================================
st.set_page_config(page_title="Executive Sales Dashboard", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

# --- THE ULTIMATE CSS FIX FOR CARD CONTRAST ---
st.markdown("""
<style>
/* 1. Main Background -> Base theme color */
.stApp, [data-testid="stAppViewContainer"] { 
    background-color: var(--background-color) !important; 
}

/* 2. The Cards -> Distinct Greyish Shade with a Border to separate it */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--secondary-background-color) !important;
    border: 1px solid rgba(128, 128, 128, 0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08) !important;
    padding: 5px !important;
}

/* 3. Hide Sidebar */
[data-testid="collapsedControl"] { display: none; }

/* 4. Make top header transparent so it blends perfectly */
header[data-testid="stHeader"] { background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)

col_title, col_date = st.columns([3, 1])
with col_title:
    st.title("Enterprise Sales Dashboard")

# --- TARGETED FIX 1: Create an empty placeholder where the badge should go ---
date_badge_placeholder = col_date.empty()
    
st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("##### ⚙️ Dashboard Controls")
    ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([1.5, 2, 1.5, 2, 1])
    
    with ctrl1:
        master_date = st.date_input("🌍 Master Date", datetime.date(2026, 5, 25))
        master_date_str = master_date.strftime("%Y-%m-%d")

    # --- UPDATED BADGE HTML: Stacks 'Administrator' nicely under your name! ---
    date_badge_placeholder.markdown(f"""
    <div style="background-color: var(--secondary-background-color); padding: 8px 20px; border-radius: 30px; 
                color: var(--text-color); float: right; 
                border: 1px solid rgba(128, 128, 128, 0.25);
                box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-top: 15px; display: flex; align-items: center; gap: 15px;">
        <div style="display: flex; flex-direction: column; line-height: 1.1;">
            <span style="color: #1F77B4; font-weight: bold; font-size: 15px;">👤 Arnav Singh</span>
            <span style="color: #888888; font-size: 10px; font-weight: bold; margin-top: 2px; text-transform: uppercase;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Administrator</span>
        </div>
        <span style="color: #A0A0A0; font-size: 18px;">|</span>
        <span style="font-weight: bold; font-size: 14px;">📅 {master_date.strftime('%d %b %Y')}</span>
    </div>
    """, unsafe_allow_html=True)

    df_daily, df_monthly, df_kpi, df_leaderboard, df_customers = fetch_data(master_date_str)

    if not df_daily.empty:
        df_daily, df_monthly, df_leaderboard, df_customers = clean_data(df_daily, df_monthly, df_leaderboard, df_customers)
        
        with ctrl2:
            min_date = df_daily["order_date"].min().date()
            max_date = df_daily["order_date"].max().date()
            date_range = st.date_input("📅 Chart Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
            
        with ctrl3:
            chart_metric = st.selectbox("📈 Chart Metric", ["Both (Revenue & Orders)", "Total Revenue (₹)", "Number of Orders"])
            
        with ctrl4:
            all_reps = [rep for rep in df_leaderboard["sales_representative"].tolist() if rep != "-"]
            selected_reps = st.multiselect("👥 Team Filter", all_reps, default=all_reps)
            
        with ctrl5:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            csv_data = df_daily.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Export Data", data=csv_data, file_name='daily_sales_report.csv', mime='text/csv')

        if len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df_daily["order_date"].dt.date >= start_date) & (df_daily["order_date"].dt.date <= end_date)
            df_daily_filtered = df_daily.loc[mask]
        else:
            df_daily_filtered = df_daily

        df_leaderboard_filtered = df_leaderboard[df_leaderboard["sales_representative"].isin(selected_reps)] if len(selected_reps) < len(all_reps) else df_leaderboard

        st.markdown("<br>", unsafe_allow_html=True) 

        # --- ROW 1: KPIs ---
        kpis = df_kpi.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.metric("📦 Today's Orders", f"{int(kpis['TODAY_SALES'])}")
        with col2:
            with st.container(border=True):
                st.metric("💰 Today's Revenue", f"₹ {kpis['TODAY_REVENUE']:,.2f}")
        with col3:
            with st.container(border=True):
                st.metric("📈 MTD Orders", f"{int(kpis['mtd_sales'])}")
        with col4:
            with st.container(border=True):
                st.metric("💎 MTD Revenue", f"₹ {kpis['MTD_REVENUE']:,.2f}")
            
        st.markdown("<br>", unsafe_allow_html=True) 

        # --- ROW 2: LEADERBOARD & DESTINATIONS ---
        col_table, col_dest = st.columns([2, 1])
        with col_table:
            with st.container(border=True):
                st.markdown("#### 📋 Top 10 Team Leaderboard")
                max_progress_val = int(df_leaderboard['mtd_sales'].max())
                max_progress_val = max_progress_val if max_progress_val > 0 else 1
                
                st.dataframe(
                    df_leaderboard_filtered, use_container_width=True, hide_index=True,
                    column_config={
                        "Rank": st.column_config.NumberColumn("Rank", width="small"),
                        "sales_representative": st.column_config.TextColumn("Sales Rep", width="medium"),
                        "today_sales": st.column_config.NumberColumn("Today's Orders"),
                        "today_revenue": st.column_config.NumberColumn("Today's Rev", format="₹ %.2f"),
                        "mtd_revenue": st.column_config.NumberColumn("MTD Rev", format="₹ %.2f"),
                        "mtd_sales": st.column_config.ProgressColumn("MTD Target", format="%f", min_value=0, max_value=max_progress_val),
                    }
                )

        with col_dest:
            with st.container(border=True): 
                st.markdown("#### ✈️ Top Destinations")
                if not df_customers.empty and "destination" in df_customers.columns:
                    real_destinations = df_customers.groupby("destination")["customer_id"].count().reset_index()
                    real_destinations.columns = ["Destination", "Orders"]
                    real_destinations = real_destinations.sort_values("Orders", ascending=False).head(10)
                    
                    st.dataframe(
                        real_destinations, use_container_width=True, hide_index=True,
                        column_config={
                            "Destination": st.column_config.TextColumn("Country"),
                            "Orders": st.column_config.NumberColumn("SIMs Sold")
                        }
                    )
                else:
                    st.info("No destination data found.")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- ROW 3: CHARTS ---
        if chart_metric == "Both (Revenue & Orders)":
            y_axis_daily = ["total_revenue", "no_of_sales"]
            daily_colors = ["#FF7F0E", "#1F77B4"] # Orange and Blue
            title_metric = "Revenue & Orders"
            y_title_primary = "Total Revenue (₹)"
        elif chart_metric == "Total Revenue (₹)":
            y_axis_daily = "total_revenue"
            daily_colors = ["#FF7F0E"]
            title_metric = "Total Revenue"
            y_title_primary = "Total Revenue (₹)"
        else:
            y_axis_daily = "no_of_sales"
            daily_colors = ["#1F77B4"]
            title_metric = "Number of Orders"
            y_title_primary = "Number of Orders"

        y_axis_monthly = "no_of_sales"

        col_daily, col_monthly = st.columns(2)

        with col_daily:
            with st.container(border=True):
                st.markdown(f"#### 📊 Daily Performance ({title_metric})")
                
                fig_daily = px.line(df_daily_filtered, x="order_date", y=y_axis_daily, markers=True, color_discrete_sequence=daily_colors)
                fig_daily.update_traces(line=dict(width=2), marker=dict(size=6))
                
                if chart_metric == "Both (Revenue & Orders)":
                    fig_daily.update_traces(yaxis="y2", selector=dict(name="no_of_sales"))
                    fig_daily.update_layout(
                        yaxis2=dict(title="Number of Orders", overlaying="y", side="right", showgrid=False),
                        legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    fig_daily.for_each_trace(lambda t: t.update(name="Revenue (₹)" if t.name=="total_revenue" else "Orders"))

                fig_daily.update_xaxes(showgrid=False, title="Date", tickformat="%d-%m", tickangle=-90, tickmode="array", tickvals=df_daily_filtered["order_date"])
                fig_daily.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", title=y_title_primary)
                fig_daily.update_layout(height=320, hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_daily, use_container_width=True)

        with col_monthly:
            with st.container(border=True):
                st.markdown(f"#### 📅 Monthly Performance (Orders)")
                fig_monthly = px.line(df_monthly, x="date", y=y_axis_monthly, markers=True, color_discrete_sequence=["#1F77B4"])
                fig_monthly.update_traces(line=dict(width=2), marker=dict(size=6))
                fig_monthly.update_xaxes(showgrid=False, title="Month", tickformat="%b %y", tickmode="array", tickvals=df_monthly["date"])
                fig_monthly.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", title="Total Orders")
                fig_monthly.update_layout(height=320, hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_monthly, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- ROW 4: CUSTOMER TABLE & PIE CHART ---
        col_cust, col_pie = st.columns([2.5, 1.5])
        
        with col_cust:
            with st.container(border=True):
                st.markdown("#### 👥 Highest Paying Customers")
                if not df_customers.empty:
                    st.dataframe(
                        df_customers,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Customer Rank": st.column_config.NumberColumn("Rank", width="small"),
                            "customer_id": st.column_config.TextColumn("ID", width="small"),
                            "customer_name": st.column_config.TextColumn("Customer Name", width="medium"),
                            "sim_purchased": st.column_config.TextColumn("Product type", width="medium"),
                            "destination": st.column_config.TextColumn("Destination", width="small"),
                            "amount_paid": st.column_config.NumberColumn("Revenue", format="₹ %.2f", width="small")
                        }
                    )
                else:
                    st.info("No customer transaction data found for this date.")

        with col_pie:
            with st.container(border=True):
                st.markdown("#### 🍩 Revenue Share by Team")
                df_pie = df_leaderboard_filtered[df_leaderboard_filtered["sales_representative"] != "-"]
                
                if not df_pie.empty:
                    fig_pie = px.pie(
                        df_pie,
                        names="sales_representative",
                        values="mtd_revenue",
                        hole=0.45,
                        color_discrete_sequence=px.colors.qualitative.Vivid
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
                    fig_pie.update_layout(height=365, margin=dict(t=10, b=10, l=10, r=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No data available for revenue share.")

    else:
        st.warning("No data available for this date. Please select a different date.")