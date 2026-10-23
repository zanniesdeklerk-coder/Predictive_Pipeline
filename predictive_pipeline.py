"""
Nexus Analytics Production Line Data Pipeline.
Author: Software Engineering Consultant
Description: Processes manufacturing telemetry data for predictive maintenance tracking.
"""

import os
import math


def calculate_mean(data_list):
    """Calculates the arithmetic mean of a numeric list, ignoring None values."""
    valid_data = [x for x in data_list if x is not None]
    if not valid_data:
        return 0.0
    return sum(valid_data) / len(valid_data)


def calculate_std_dev(data_list, mean):
    """Calculates the standard deviation of a numeric list, ignoring None values."""
    valid_data = [x for x in data_list if x is not None]
    if len(valid_data) <= 1:
        return 0.0
    variance = sum((x - mean) ** 2 for x in valid_data) / (len(valid_data) - 1)
    return math.sqrt(variance)


def clean_telemetry_data(raw_records):
    """
    Cleans raw sensor data using forward-fill for missing timestamps
    and mean substitution for missing sensor metrics.
    """
    cleaned_records = []

    # Calculate global averages for imputation fallback
    temp_mean = calculate_mean([r.get('temperature') for r in raw_records])
    vib_mean = calculate_mean([r.get('vibration') for r in raw_records])

    for i, record in enumerate(raw_records):
        cleaned = record.copy()

        # Handle timestamp continuity
        if cleaned.get('timestamp') is None and i > 0:
            cleaned['timestamp'] = cleaned_records[i - 1]['timestamp'] + 3600
        elif cleaned.get('timestamp') is None:
            cleaned['timestamp'] = 0

        # Handle missing sensor metrics via mean imputation
        if cleaned.get('temperature') is None:
            cleaned['temperature'] = temp_mean
        if cleaned.get('vibration') is None:
            cleaned['vibration'] = vib_mean

        cleaned_records.append(cleaned)

    return cleaned_records


def process_moving_averages(records, window_size=3):
    """Calculates local moving averages for smoothing operational transients."""
    smoothed_records = []
    for i in range(len(records)):
        start_idx = max(0, i - window_size + 1)
        sub_set = records[start_idx:i + 1]

        temp_window = [r['temperature'] for r in sub_set]
        vib_window = [r['vibration'] for r in sub_set]

        rec_copy = records[i].copy()
        rec_copy['moving_avg_temp'] = calculate_mean(temp_window)
        rec_copy['moving_avg_vib'] = calculate_mean(vib_window)
        smoothed_records.append(rec_copy)

    return smoothed_records


def evaluate_threshold_anomalies(records, temp_limit=85.0, vib_limit=4.5):
    """Applies engineering rule constraints to identify asset health flags."""
    flagged_records = []
    for record in records:
        rec_copy = record.copy()
        status = "OPERATIONAL"

        if rec_copy['moving_avg_temp'] > temp_limit or rec_copy['moving_avg_vib'] > vib_limit:
            status = "CRITICAL_MAINTENANCE_REQUIRED"
        elif rec_copy['moving_avg_temp'] > (temp_limit * 0.85) or rec_copy['moving_avg_vib'] > (vib_limit * 0.85):
            status = "WARNING_HIGH_STRESS"

        rec_copy['asset_status'] = status
        flagged_records.append(rec_copy)

    return flagged_records


if __name__ == "__main__":
    # Mock industrial asset data input stream
    raw_telemetry_stream = [
        {"timestamp": 1710000000, "temperature": 62.4, "vibration": 2.1},
        {"timestamp": 1710003600, "temperature": None, "vibration": 2.3},  # Missing temp
        {"timestamp": None, "temperature": 68.1, "vibration": 3.2},  # Missing time
        {"timestamp": 1710010800, "temperature": 88.5, "vibration": 4.9},  # High stress spike
        {"timestamp": 1710014400, "temperature": 86.2, "vibration": 4.6}  # Confirmed failure state
    ]

    print("--- Executing Telemetry Pipeline Execution ---")
    cleaned = clean_telemetry_data(raw_telemetry_stream)
    smoothed = process_moving_averages(cleaned)
    analyzed_output = evaluate_threshold_anomalies(smoothed)

    for row in analyzed_output:
        print(f"Time: {row['timestamp']} | Temp: {row['temperature']:.1f}°C | "
              f"SmoothVib: {row['moving_avg_vib']:.2f} mm/s | Status: {row['asset_status']}")
