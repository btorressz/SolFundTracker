import numpy as np
import math
from typing import Tuple
from datetime import datetime

class FundingCalculator:
    """Calculator for synthetic perpetual funding rates."""
    
    def __init__(self):
        self.last_perp_price = None
        self.trend_momentum = 0.0  # For trend persistence
        
    def generate_perp_price(self, spot_price: float, noise_level: float, trend_bias: float) -> float:
        """
        Generate synthetic perpetual price with noise and trend bias.
        
        Args:
            spot_price: Current spot price
            noise_level: Noise level as percentage (0-5%)
            trend_bias: Trend bias as percentage (-2% to +2%)
            
        Returns:
            float: Synthetic perpetual price
        """
        try:
            # Convert percentages to decimals
            noise_factor = noise_level / 100.0
            bias_factor = trend_bias / 100.0
            
            # Generate random noise
            noise = np.random.normal(0, noise_factor)
            
            # Apply trend momentum for more realistic price movement
            momentum_decay = 0.95  # Decay factor for momentum
            self.trend_momentum = self.trend_momentum * momentum_decay + bias_factor * 0.1
            
            # Calculate perp price with noise, bias, and momentum
            price_adjustment = noise + bias_factor + self.trend_momentum
            perp_price = spot_price * (1 + price_adjustment)
            
            # Add some correlation with previous perp price for smoother movement
            if self.last_perp_price is not None:
                smoothing_factor = 0.3
                perp_price = (perp_price * (1 - smoothing_factor) + 
                             self.last_perp_price * smoothing_factor)
            
            self.last_perp_price = perp_price
            
            return max(perp_price, 0.0001)  # Ensure positive price
            
        except Exception as e:
            # Fallback to spot price if calculation fails
            return spot_price
    
    def calculate_funding_rate(self, spot_price: float, perp_price: float, 
                             funding_coefficient: float, max_funding_rate: float) -> float:
        """
        Calculate funding rate based on price divergence (Binance-style).
        
        Funding Rate = (Perp Price - Spot Price) / Spot Price * Funding Coefficient
        Capped at max_funding_rate
        
        Args:
            spot_price: Spot price
            perp_price: Perpetual price
            funding_coefficient: Multiplier for funding calculation
            max_funding_rate: Maximum funding rate (as percentage)
            
        Returns:
            float: Funding rate as percentage
        """
        try:
            if spot_price <= 0:
                return 0.0
            
            # Calculate price divergence
            price_divergence = (perp_price - spot_price) / spot_price
            
            # Apply funding coefficient
            funding_rate = price_divergence * funding_coefficient
            
            # Convert to percentage
            funding_rate_pct = funding_rate * 100
            
            # Apply maximum funding rate cap
            max_rate = max_funding_rate
            funding_rate_pct = max(-max_rate, min(max_rate, funding_rate_pct))
            
            return funding_rate_pct
            
        except Exception as e:
            return 0.0
    
    def calculate_premium_index(self, spot_price: float, perp_price: float) -> float:
        """
        Calculate premium index (price divergence percentage).
        
        Args:
            spot_price: Spot price
            perp_price: Perpetual price
            
        Returns:
            float: Premium index as percentage
        """
        try:
            if spot_price <= 0:
                return 0.0
            
            return ((perp_price - spot_price) / spot_price) * 100
            
        except Exception:
            return 0.0
    
    def estimate_hourly_funding(self, current_funding_rate: float) -> float:
        """
        Estimate 8-hour funding payment based on current funding rate.
        
        Args:
            current_funding_rate: Current funding rate percentage
            
        Returns:
            float: Estimated 8-hour funding rate
        """
        # Binance charges funding every 8 hours
        # This is a simplified estimation
        return current_funding_rate
    
    def calculate_funding_statistics(self, funding_rates: list) -> dict:
        """
        Calculate funding rate statistics.
        
        Args:
            funding_rates: List of funding rates
            
        Returns:
            dict: Statistics including mean, std, min, max, etc.
        """
        try:
            if not funding_rates:
                return {}
            
            rates = np.array(funding_rates)
            
            return {
                'mean': float(np.mean(rates)),
                'std': float(np.std(rates)),
                'min': float(np.min(rates)),
                'max': float(np.max(rates)),
                'median': float(np.median(rates)),
                'q25': float(np.percentile(rates, 25)),
                'q75': float(np.percentile(rates, 75)),
                'positive_rate_pct': float(np.sum(rates > 0) / len(rates) * 100),
                'negative_rate_pct': float(np.sum(rates < 0) / len(rates) * 100)
            }
            
        except Exception:
            return {}
