
# 🧮 SolFundTracker - Synthetic Perpetuals Funding Rate Tracker

## 📖 Overview
This project is a **Streamlit-based web application** that tracks synthetic perpetual funding rates for SOL (Solana) cryptocurrency. It fetches real-time SOL prices from the **Jupiter API** and generates synthetic perpetual contract prices with configurable **noise** and **trend bias** to simulate funding rate calculations. The application provides **real-time visualization** of funding rates, price divergence, and historical data logging.

---

## 🏗️ System Architecture

The application follows a **modular Python architecture** with clear separation of concerns:

- **Frontend**: Streamlit web interface with real-time data visualization  
- **Data Sources**: Jupiter API for live SOL price feeds  
- **Synthetic Data Generation**: Custom algorithms for perpetual price simulation  
- **Data Persistence**: CSV-based logging system for historical data  
- **Visualization**: Plotly charts for interactive data presentation

---

## 🧩 Key Components

### 🔧 Core Modules
- `app.py` – Main Streamlit application with UI components and real-time updates  
- `jupiter_api.py` – Jupiter API client for fetching SOL spot prices  
- `funding_calculator.py` – Synthetic perpetual price generation and funding rate calculations  
- `data_logger.py` – CSV-based data persistence layer

### 🧱 Data Models
The application works with the following data structure:
- Timestamp  
- Spot price (from Jupiter API)  
- Perpetual price (synthetically generated)  
- Funding rate (calculated)  
- Price divergence percentage  

---

## 🖥️ User Interface
- Real-time metrics dashboard with colorful gradient styling  
- Interactive controls for **noise level** and **trend bias** adjustment  
- Live charts showing **funding rates** and **price movements over time**  
- Historical data display and export capabilities  

---

## 🔄 Data Flow
1. **Price Fetching**: Jupiter API provides real-time SOL spot prices  
2. **Synthetic Generation**: `FundingCalculator` generates perpetual prices with configurable parameters  
3. **Rate Calculation**: Funding rates are computed based on price divergence  
4. **Data Logging**: All data points are stored in daily CSV files  
5. **Visualization**: Real-time charts updated via Streamlit's auto-refresh mechanism  

---

## 📦 External Dependencies

### 🛰️ APIs
- **Jupiter API**: Primary data source for SOL spot prices  
  - Endpoint: `https://api.jup.ag/price/v2`

### 🐍 Python Libraries
- `streamlit` – Web application framework  
- `plotly` – Interactive charting and visualization  
- `pandas` – Data manipulation and analysis  
- `numpy` – Numerical computations for price generation  
- `requests` – HTTP client for API calls

---

## 🎨 Frontend Color Palette

### 🟦 Primary Blues (Headers & Text)
- **Dark Blue**: `#1e3c72`
- **Medium Blue**: `#2a5298`
- **Light Blue**: `#4169E1`
- **Accent Blue**: `#33b5e5`

  ### 🌄 Background Gradients
- **Main Background**:  
  `linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)`
- **Sidebar Background**:  
  `linear-gradient(180deg, #a8edea 0%, #fed6e3 100%)`
- **Card Background**:  
  `linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)`

  ### 📈 Chart Colors
- **Primary Line (Coral Red)**: `#FF6B6B`
- **Secondary Line (Teal)**: `#4ECDC4`
- **Accent Line (Golden Yellow)**: `#FFD93D`
- **Purple Accent (Medium Orchid)**: `#BA55D3`



## 🧾 License

This project is licensed under the MIT License.  

---


## 📸 Screenshots

![SolFundTracker Screenshot](https://github.com/btorressz/SolFundTracker/blob/main/solfundtrackerscreenshot.jpg)

---



