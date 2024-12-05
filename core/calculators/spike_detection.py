import pandas as pd

def perform_spike_analysis(data):
    """
    Perform spike detection by resampling event data.
    """
    # Ensure 'api_start_time' is properly set as index
    data['api_start_time'] = pd.to_datetime(data['api_start_time'], errors='coerce')
    data = data.set_index('api_start_time')

    # Resample and calculate metrics
    event_counts = data.groupby('api_source').resample('5min').agg(
        events_per_5min=('event_count', 'sum')
    ).reset_index()

    # Calculate thresholds for spikes
    event_thresholds = event_counts.groupby('api_source')['events_per_5min'].quantile(0.95).reset_index()
    event_thresholds.rename(columns={'events_per_5min': 'event_threshold'}, inplace=True)

    # Merge thresholds with event counts
    event_counts = event_counts.merge(event_thresholds, on='api_source')
    event_counts['is_spike'] = event_counts['events_per_5min'] > event_counts['event_threshold']

    return event_counts, event_thresholds
