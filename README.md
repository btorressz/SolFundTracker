
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
