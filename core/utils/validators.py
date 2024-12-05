from typing import Any, Dict, List, Optional
import re

class Validator:
    @staticmethod
    def validate_metric_data(data: Dict) -> bool:
        required_fields = ['timestamp', 'value', 'metric_type']
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_api_name(api_name: str) -> bool:
        pattern = r'^[a-zA-Z0-9-_]+$'
        return bool(re.match(pattern, api_name))

    @staticmethod
    def validate_threshold(threshold: float) -> bool:
        return isinstance(threshold, (int, float)) and threshold > 0

    @staticmethod
    def validate_timerange(start: str, end: str) -> bool:
        try:
            from datetime import datetime
            datetime.fromisoformat(start)
            datetime.fromisoformat(end)
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_input(value: str) -> str:
        return re.sub(r'[^\w\s-]', '', value)