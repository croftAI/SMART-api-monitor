from pathlib import Path
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class ModelConfig:
    type: str
    parameters: Dict[str, Any]
    training: Dict[str, Any]


class MLConfigurationManager:
    def __init__(self, config_path: str = "config/ml_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _validate_config(self):
        """Validate configuration structure and required fields."""
        required_sections = ['model_registry', 'models', 'ensemble', 'performance_monitoring']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")

        # Validate model configurations
        for model_name, model_config in self.config['models'].items():
            required_model_fields = ['type', 'parameters', 'training']
            for field in required_model_fields:
                if field not in model_config:
                    raise ValueError(f"Missing required field '{field}' in model config: {model_name}")

    def get_model_config(self, model_name: str) -> ModelConfig:
        """Get configuration for a specific model."""
        if model_name not in self.config['models']:
            raise KeyError(f"Model configuration not found: {model_name}")

        model_config = self.config['models'][model_name]
        return ModelConfig(
            type=model_config['type'],
            parameters=model_config['parameters'],
            training=model_config['training']
        )

    def get_ensemble_weights(self) -> Dict[str, float]:
        """Get ensemble model weights."""
        return self.config['ensemble']['weights']

    def get_performance_thresholds(self) -> Dict[str, float]:
        """Get performance monitoring thresholds."""
        return {
            metric['type']: metric['threshold']
            for metric in self.config['performance_monitoring']['metrics']
        }

    def update_model_parameter(self, model_name: str, parameter: str, value: Any):
        """Update a specific model parameter."""
        if model_name not in self.config['models']:
            raise KeyError(f"Model configuration not found: {model_name}")

        if parameter not in self.config['models'][model_name]['parameters']:
            raise KeyError(f"Parameter not found: {parameter}")

        self.config['models'][model_name]['parameters'][parameter] = value
        self._save_config()

    def _save_config(self):
        """Save current configuration back to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def export_model_config(self, model_name: str, export_path: Optional[str] = None) -> str:
        """Export model configuration to JSON format."""
        model_config = self.get_model_config(model_name)
        config_dict = {
            'name': model_name,
            'type': model_config.type,
            'parameters': model_config.parameters,
            'training': model_config.training
        }

        if export_path:
            with open(export_path, 'w') as f:
                json.dump(config_dict, f, indent=2)

        return json.dumps(config_dict, indent=2)


# Example usage in model initialization
class ModelInitializer:
    def __init__(self, config_manager: MLConfigurationManager):
        self.config_manager = config_manager

    def initialize_prophet_model(self):
        config = self.config_manager.get_model_config('prophet')
        return Prophet(**config.parameters)

    def initialize_lstm_model(self):
        config = self.config_manager.get_model_config('lstm')
        return self._build_lstm_model(config.parameters)

    def _build_lstm_model(self, parameters):
        model = Sequential()
        for layer in parameters['layers']:
            if layer['type'] == 'LSTM':
                model.add(LSTM(
                    units=layer['units'],
                    activation=layer['activation'],
                    return_sequences=layer.get('return_sequences', False)
                ))
            elif layer['type'] == 'Dense':
                model.add(Dense(
                    units=layer['units'],
                    activation=layer['activation']
                ))
        return model