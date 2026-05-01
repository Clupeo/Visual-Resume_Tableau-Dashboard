"""Google Sheets Export Module - Handles exporting pandas DataFrames to Google Sheets."""

import logging
from pathlib import Path
from typing import Dict, Optional
import pandas as pd
from datetime import datetime, date

# Google Sheets API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleSheetsExporter:
    """Handles exporting data to Google Sheets using Service Account authentication."""
    
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    
    def __init__(self):
        """Initialize Google Sheets exporter."""
        self.sheet_id = Config.GOOGLE_SHEETS_ID
        self.credentials_path = Config.GOOGLE_CREDENTIALS_PATH
        self.service = None
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate using Google Service Account.
        
        Returns:
            bool: True if authentication successful
        """
        if not GOOGLE_SHEETS_AVAILABLE:
            logger.warning("❌ Google Sheets API libraries not installed. Skipping Google Sheets export.")
            return False
        
        if not self.sheet_id:
            logger.warning("⚠️  GOOGLE_SHEETS_ID not configured. Skipping Google Sheets export.")
            return False
        
        try:
            # Check if credentials file exists
            creds_file = Path(self.credentials_path)
            if not creds_file.exists():
                logger.warning(f"⚠️  Credentials file not found: {self.credentials_path}")
                logger.warning("   Follow README.md (Google Sheets Integration) to get credentials.json")
                return False
            
            # Load credentials from service account JSON
            credentials = Credentials.from_service_account_file(
                str(creds_file),
                scopes=self.SCOPES
            )
            
            # Build Google Sheets service
            self.service = build("sheets", "v4", credentials=credentials)
            self.authenticated = True
            logger.info("✅ Google Sheets authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Google Sheets authentication failed: {e}")
            return False
    
    def _serialize_value(self, value):
        """
        Serialize a value for JSON/Google Sheets compatibility.
        Handles dates, datetimes, booleans, etc.
        
        Args:
            value: The value to serialize
            
        Returns:
            Serialized value suitable for Google Sheets
        """
        # Try to check for NaN only on scalar values
        if pd.api.types.is_scalar(value):
            try:
                if pd.isna(value):
                    return None
            except (TypeError, ValueError):
                pass
        
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value
        else:
            return str(value)
    
    def write_dataframes_to_sheets(self, dataframes: Dict[str, pd.DataFrame]) -> bool:
        """
        Write multiple DataFrames to Google Sheets, one per sheet.
        
        Args:
            dataframes: Dict mapping view names to DataFrames
                        e.g., {"portfolio_view": df_portfolio, "timeline_view": df_timeline}
        
        Returns:
            bool: True if export successful
        """
        if not self.authenticated:
            return False
        
        try:
            # Get current sheet list
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            existing_sheets = {sheet["properties"]["title"]: sheet["properties"]["sheetId"] 
                              for sheet in sheet_metadata.get("sheets", [])}
            
            requests = []
            data_updates = []
            
            for view_name, df in dataframes.items():
                sheet_id_num = existing_sheets.get(view_name)
                
                # If sheet doesn't exist, create it
                if sheet_id_num is None:
                    request = {
                        "addSheet": {
                            "properties": {
                                "title": view_name,
                                "gridProperties": {
                                    "rowCount": max(1000, len(df) + 10),
                                    "columnCount": len(df.columns)
                                }
                            }
                        }
                    }
                    requests.append(request)
                    logger.info(f"📝 Creating sheet: {view_name}")
                
                # Prepare data for update
                # Convert DataFrame to list of lists with headers
                data = [df.columns.tolist()]
                for _, row in df.iterrows():
                    data.append([self._serialize_value(val) for val in row.values])
                
                data_updates.append({
                    "range": f"{view_name}!A1",
                    "values": data,
                    "majorDimension": "ROWS"
                })
                logger.info(f"✅ Prepared {view_name} for export ({len(df)} rows)")
            
            # Execute batch update (create new sheets)
            if requests:
                batch_update_request = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={"requests": requests}
                ).execute()
                logger.info(f"📝 Created {len(requests)} new sheet(s)")
            
            # Execute batch update (write data to sheets)
            if data_updates:
                update_request = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={
                        "data": data_updates,
                        "valueInputOption": "RAW"
                    }
                ).execute()
                logger.info(f"✅ Updated {len(data_updates)} sheet(s) with data")
            
            logger.info("✅ Google Sheets export completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Google Sheets export failed: {e}")
            return False
    
    def clear_sheet_data(self, sheet_name: str) -> bool:
        """
        Clear all data from a specific sheet (keep headers if present).
        
        Args:
            sheet_name: Name of the sheet to clear
            
        Returns:
            bool: True if successful
        """
        if not self.authenticated:
            return False
        
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A2:Z10000"
            ).execute()
            logger.info(f"✅ Cleared data from {sheet_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to clear {sheet_name}: {e}")
            return False
