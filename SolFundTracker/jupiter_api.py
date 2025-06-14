import requests
import json
from typing import Optional
import streamlit as st

class JupiterAPI:
    """Jupiter API client for fetching SOL price data."""
    
    def __init__(self):
        self.base_url = "https://api.jup.ag/price/v2"
        self.sol_mint = "So11111111111111111111111111111111111111112"  # SOL mint address
        
    def get_sol_price(self) -> Optional[float]:
        """
        Fetch current SOL price from Jupiter API.
        
        Returns:
            float: SOL price in USD, or None if request fails
        """
        try:
            # Jupiter price API endpoint
            url = f"{self.base_url}"
            params = {
                "ids": self.sol_mint
            }
            
            # Make request with timeout
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract SOL price from response
            if "data" in data and self.sol_mint in data["data"]:
                price_data = data["data"][self.sol_mint]
                return float(price_data.get("price", 0))
            else:
                # Fallback: try alternative endpoint structure
                if isinstance(data, dict) and "price" in data:
                    return float(data["price"])
                
                st.error("Unexpected API response structure")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Jupiter API request failed: {str(e)}")
            return None
        except (ValueError, KeyError, TypeError) as e:
            st.error(f"Error parsing Jupiter API response: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error fetching SOL price: {str(e)}")
            return None
    
    def get_historical_prices(self, days: int = 7) -> Optional[list]:
        """
        Get historical price data for SOL.
        Note: This is a placeholder as Jupiter API might not provide historical data.
        
        Args:
            days: Number of days of historical data
            
        Returns:
            list: Historical price data or None if not available
        """
        # Jupiter API might not provide historical data
        # This would need to be implemented if the API supports it
        st.warning("Historical price data not available through Jupiter API")
        return None
    
    def test_connection(self) -> bool:
        """
        Test connection to Jupiter API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            price = self.get_sol_price()
            return price is not None
        except Exception:
            return False
