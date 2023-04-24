from datetime import datetime, timedelta
from typing import List

def get_week_start(start_date_str: str, date_format: str) -> datetime:
      start_date = datetime.strptime(start_date_str, date_format)
      return start_date - timedelta(days=((start_date.weekday())))

def get_week_dates(start_date_str: str, date_format: str = "%m/%d/%Y") -> List[str]:
        start_of_week = get_week_start(start_date_str, date_format)
        date_strs = []
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            date_strs.append(date.strftime(date_format))
        return date_strs