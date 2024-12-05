from typing import Dict, Any
import json
from pathlib import Path


class StateManager:
    def __init__(self, state_file: str = "state.json"):
        self.state_file = Path(state_file)
        self.state: Dict[str, Any] = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from persistent storage."""
        if not self.state_file.exists():
            return {}

        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_state(self):
        """Save current state to persistent storage."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def update_api_state(self, api_name: str, state_data: Dict):
        """Update state for specific API."""
        if api_name not in self.state:
            self.state[api_name] = {}

        self.state[api_name].update(state_data)
        self.save_state()