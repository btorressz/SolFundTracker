import csv
import os
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd

class DataLogger:
    """Data logger for funding rate and price data."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_csv_filename(self, date: datetime = None) -> str:
        """
        Generate CSV filename based on date.
        
        Args:
            date: Date for filename, defaults to current date
            
        Returns:
            str: CSV filename
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y-%m-%d")
        return os.path.join(self.data_dir, f"funding_data_{date_str}.csv")
    
    def log_data(self, data_point: Dict[str, Any]):
        """
        Log data point to CSV file.
        
        Args:
            data_point: Dictionary containing data to log
        """
        try:
            filename = self.get_csv_filename()
            file_exists = os.path.exists(filename)
            
            # Prepare data for CSV
            csv_data = {
                'timestamp': data_point['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'spot_price': data_point['spot_price'],
                'perp_price': data_point['perp_price'],
                'funding_rate': data_point['funding_rate'],
                'price_divergence': data_point['price_divergence']
            }
            
            # Write to CSV
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'spot_price', 'perp_price', 'funding_rate', 'price_divergence']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(csv_data)
                
        except Exception as e:
            # Log error but don't break the application
            print(f"Error logging data: {str(e)}")
    
    def load_historical_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Load historical data from CSV files.
        
        Args:
            days: Number of days to load
            
        Returns:
            List of data points
        """
        try:
            data_points = []
            
            # Get list of CSV files to load
            current_date = datetime.now()
            for i in range(days):
                date = current_date - pd.Timedelta(days=i)
                filename = self.get_csv_filename(date)
                
                if os.path.exists(filename):
                    df = pd.read_csv(filename)
                    
                    for _, row in df.iterrows():
                        data_point = {
                            'timestamp': pd.to_datetime(row['timestamp']),
                            'spot_price': float(row['spot_price']),
                            'perp_price': float(row['perp_price']),
                            'funding_rate': float(row['funding_rate']),
                            'price_divergence': float(row['price_divergence'])
                        }
                        data_points.append(data_point)
            
            # Sort by timestamp
            data_points.sort(key=lambda x: x['timestamp'])
            
            return data_points
            
        except Exception as e:
            print(f"Error loading historical data: {str(e)}")
            return []
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary of logged data.
        
        Returns:
            Dictionary with data summary
        """
        try:
            # Get all CSV files
            csv_files = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith("funding_data_") and filename.endswith(".csv"):
                    csv_files.append(os.path.join(self.data_dir, filename))
            
            if not csv_files:
                return {"total_files": 0, "total_records": 0}
            
            total_records = 0
            date_range = {"start": None, "end": None}
            
            for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                total_records += len(df)
                
                if len(df) > 0:
                    file_start = pd.to_datetime(df['timestamp'].iloc[0])
                    file_end = pd.to_datetime(df['timestamp'].iloc[-1])
                    
                    if date_range["start"] is None or file_start < date_range["start"]:
                        date_range["start"] = file_start
                    
                    if date_range["end"] is None or file_end > date_range["end"]:
                        date_range["end"] = file_end
            
            return {
                "total_files": len(csv_files),
                "total_records": total_records,
                "date_range": date_range
            }
            
        except Exception as e:
            print(f"Error getting data summary: {str(e)}")
            return {"error": str(e)}
    
    def export_data(self, start_date: datetime = None, end_date: datetime = None) -> str:
        """
        Export data to a single CSV file.
        
        Args:
            start_date: Start date for export
            end_date: End date for export
            
        Returns:
            str: Path to exported file
        """
        try:
            # Load all data
            all_data = self.load_historical_data(days=365)  # Load up to 1 year
            
            if not all_data:
                return None
            
            # Filter by date range if specified
            if start_date or end_date:
                filtered_data = []
                for data_point in all_data:
                    timestamp = data_point['timestamp']
                    
                    if start_date and timestamp < start_date:
                        continue
                    if end_date and timestamp > end_date:
                        continue
                    
                    filtered_data.append(data_point)
                
                all_data = filtered_data
            
            # Create export filename
            export_filename = os.path.join(
                self.data_dir, 
                f"funding_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            # Write to CSV
            if all_data:
                df = pd.DataFrame(all_data)
                df.to_csv(export_filename, index=False)
                return export_filename
            
            return None
            
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return None
