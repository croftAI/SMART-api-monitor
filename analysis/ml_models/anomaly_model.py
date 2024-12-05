import pandas as pd
from datetime import datetime, timedelta

class AnomalyDetectionSystem:
    def __init__(self):
        self.orchestrator = MLModelOrchestrator()
        self.feature_store = {}
        self.predictions = {}

    def process_metric(self, metric_name: str, timestamp: datetime, value: float):
        """Process new metric data point"""
        # Store feature
        if metric_name not in self.feature_store:
            self.feature_store[metric_name] = []
        self.feature_store[metric_name].append({
            'timestamp': timestamp,
            'value': value
        })

        # Generate predictions and detect anomalies
        self.analyze_metric(metric_name)

    def analyze_metric(self, metric_name: str):
        """Analyze metric using multiple models"""
        data = pd.DataFrame(self.feature_store[metric_name])

        # Prophet Analysis
        prophet_prediction = self._prophet_forecast(data)

        # Isolation Forest Analysis
        isolation_forest_prediction = self._isolation_forest_detect(data)

        # LSTM Analysis
        lstm_prediction = self._lstm_predict(data)

        # Ensemble results
        anomaly_score = self._ensemble_predictions(
            prophet_prediction,
            isolation_forest_prediction,
            lstm_prediction
        )

        return anomaly_score

    def _prophet_forecast(self, data: pd.DataFrame):
        """Generate forecast using Prophet"""
        model = self.orchestrator.registry.models['prophet']['instance']

        # Prepare data for Prophet
        prophet_data = data.rename(columns={
            'timestamp': 'ds',
            'value': 'y'
        })

        # Fit and predict
        model.fit(prophet_data)
        future = model.make_future_dataframe(periods=1, freq='5min')
        forecast = model.predict(future)

        return forecast.tail(1)['yhat'].values[0]

    def _isolation_forest_detect(self, data: pd.DataFrame):
        """Detect anomalies using Isolation Forest"""
        model = self.orchestrator.registry.models['isolation_forest']['instance']

        # Reshape data for Isolation Forest
        X = data['value'].values.reshape(-1, 1)

        # Fit and predict
        prediction = model.fit_predict(X)
        return prediction[-1]

    def _lstm_predict(self, data: pd.DataFrame):
        """Generate prediction using LSTM"""
        model = self.orchestrator.registry.models['lstm']['instance']

        # Prepare sequences for LSTM
        sequence_length = 60
        if len(data) < sequence_length:
            return None

        values = data['value'].values
        sequence = values[-sequence_length:].reshape(1, sequence_length, 1)

        # Generate prediction
        prediction = model.predict(sequence)
        return prediction[0][0]

    def _ensemble_predictions(self, prophet_pred, isolation_pred, lstm_pred):
        """Combine predictions from different models"""
        # Weight the predictions
        weights = {
            'prophet': 0.4,
            'isolation_forest': 0.3,
            'lstm': 0.3
        }

        anomaly_score = (
                prophet_pred * weights['prophet'] +
                isolation_pred * weights['isolation_forest'] +
                (lstm_pred if lstm_pred is not None else 0) * weights['lstm']
        )

        return anomaly_score