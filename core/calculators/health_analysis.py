import pandas as pd
import streamlit as st

def calculate_health_metrics(filtered_data):
    # Resample data and calculate event metrics
    health_analysis_data = filtered_data.set_index('api_start_time')
    event_metrics = health_analysis_data.groupby('api_source').resample('5min').agg(
        events_per_5min=('event_count', 'sum'),
        avg_response_time_per_5min=('total_response_time', 'mean'),
        avg_error_rate_per_5min=('error_rate', 'mean')
    ).reset_index()

    # Normalize metrics for health score calculation
    event_metrics['normalized_response_time'] = (
        (event_metrics['avg_response_time_per_5min'] - event_metrics['avg_response_time_per_5min'].min()) /
        (event_metrics['avg_response_time_per_5min'].max() - event_metrics['avg_response_time_per_5min'].min())
    ).fillna(0)
    event_metrics['normalized_error_rate'] = (
        (event_metrics['avg_error_rate_per_5min'] - event_metrics['avg_error_rate_per_5min'].min()) /
        (event_metrics['avg_error_rate_per_5min'].max() - event_metrics['avg_error_rate_per_5min'].min())
    ).fillna(0)
    event_metrics['normalized_spike_count'] = (
        (event_metrics['events_per_5min'] - event_metrics['events_per_5min'].min()) /
        (event_metrics['events_per_5min'].max() - event_metrics['events_per_5min'].min())
    ).fillna(0)

    # Weighting for health score
    w_response_time = 0.5
    w_error_rate = 0.3
    w_spike_count = 0.2

    event_metrics['health_score'] = 1 - (
        w_response_time * event_metrics['normalized_response_time'] +
        w_error_rate * event_metrics['normalized_error_rate'] +
        w_spike_count * event_metrics['normalized_spike_count']
    )

    # Aggregate health scores
    aggregated_scores = event_metrics.groupby('api_source', as_index=False).agg(
        avg_health_score=('health_score', 'mean'),
        avg_response_time=('avg_response_time_per_5min', 'mean'),
        avg_error_rate=('avg_error_rate_per_5min', 'mean'),
        avg_events_per_5min=('events_per_5min', 'mean')
    )

    # Add status column based on health score threshold
    aggregated_scores['status'] = aggregated_scores['avg_health_score'].apply(
        lambda x: 'Critical' if x < 0.5 else 'Healthy'
    )

    # Debugging: Check aggregated scores
    st.write("Debugging: Aggregated Scores")
    st.dataframe(aggregated_scores)

    return event_metrics, aggregated_scores
