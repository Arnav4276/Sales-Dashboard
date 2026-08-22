<div align="center">
  
  <h1 align="center">📊 Enterprise Sales Dashboard</h1>

  <p align="center">
    <strong>A modern, interactive, and comprehensive sales dashboard built with Streamlit and Plotly.</strong>
  </p>
  
  [![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
  [![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-FF6F00?logo=plotly)](https://plotly.com/)
  [![Supabase API](https://img.shields.io/badge/Data-Supabase_API-3ECF8E?logo=supabase)](https://supabase.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

<hr>

## 🚀 Overview

The **Enterprise Sales Dashboard** is a data-driven web application designed to empower sales teams and executives with real-time insights. By seamlessly integrating with a Supabase backend API, this dashboard visualizes critical metrics such as daily and monthly revenue, team performance, top destinations, and high-value customers. 

With its sleek dark-mode UI, custom CSS styling, and interactive Plotly charts, monitoring business growth has never been more intuitive.

---

## ✨ Key Features

- **🎯 Real-Time KPI Tracking**: Instantly view Today's Orders, Today's Revenue, and Month-to-Date (MTD) metrics.
- **🏆 Team Leaderboard**: Track top-performing sales representatives and their progress towards MTD targets.
- **✈️ Top Destinations**: Analyze product demand across different geographical regions/countries.
- **📈 Interactive Visualizations**: Explore trends with dynamic Daily and Monthly performance charts built with Plotly.
- **💎 Customer Insights**: Identify your highest-paying customers and their purchase details.
- **🍩 Revenue Share**: Understand contribution distribution among team members via intuitive pie charts.
- **📥 Data Export**: Easily download filtered reports as CSV files for offline analysis.
- **📅 Dynamic Filtering**: Slice and dice data using custom date ranges and team filters.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **[Streamlit](https://streamlit.io/)** | Core web framework for building the dashboard UI. |
| **[Pandas](https://pandas.pydata.org/)** | Data manipulation, cleaning, and aggregation. |
| **[Plotly Express](https://plotly.com/python/)** | Rendering interactive and responsive charts. |
| **[Requests](https://pypi.org/project/requests/)** | Handling HTTP requests to fetch live data from the API. |
| **[Python-dotenv](https://pypi.org/project/python-dotenv/)** | Secure management of environment variables. |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Sales-Dashboard.git
cd Sales-Dashboard
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of the project and add your API credentials:
```env
SUPABASE_API_URL=your_api_endpoint_url_here
SUPABASE_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
*The dashboard will automatically open in your default web browser at `http://localhost:8501`.*

---

## 📂 Project Structure

```text
Sales-Dashboard/
│
├── app.py                 # Main application script (UI and Logic)
├── requirements.txt       # Python dependencies required
├── .env                   # Environment variables (Create this file!)
├── .gitignore             # Files & folders to be ignored by Git
└── README.md              # Project documentation (You are here)
```

---

## 💡 How It Works

1. **Data Fetching**: The app makes a secure POST request to the Supabase API using the selected "Master Date".
2. **Data Processing**: Pandas handles data type conversions, sorting, and padding missing rows for the leaderboard.
3. **UI Rendering**: Streamlit dynamically builds the grid layout with custom CSS injected to enhance the contrast and visual appeal of the metric cards.
4. **Interactivity**: User inputs (Date Range, Metrics, Team Filters) trigger reactive updates across all charts and tables on the fly.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/your-username/Sales-Dashboard/issues).

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

<div align="center">
  <p>Built with ❤️ using Python & Streamlit</p>
</div>