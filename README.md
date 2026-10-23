# Predictive_Pipeline_Problem_Email
We require you to develop a robust, production-ready Python data pipeline that reads a raw dataset, cleans missing entries, engineers statistical features, isolates out-of-bounds metrics, and outputs a formatted engineering summary.
# Production Line Predictive Maintenance Data Pipeline

## Project Overview
This repository contains a production-ready, pure-Python data processing pipeline designed for industrial telemetry anomaly detection. The system ingests raw manufacturing sensor logs, handles missing data points, applies mathematical smoothing algorithms to eliminate signal noise, and uses an engineering rule engine to flag assets requiring immediate maintenance. 

## Technical Architecture
The pipeline processes incoming data through three distinct functional layers:
1. **Data Quality Layer:** Uses linear time reconstruction and mean value substitution to fix missing timestamps and sensor dropouts.
2. **Signal Conditioning Layer:** Implements a discrete moving-window average to damp temporary, non-damaging mechanical vibration spikes.
3. **Rule Engine Evaluation Layer:** Evaluates calculated averages against thermal and physical boundaries to output unambiguous asset operational states (`OPERATIONAL`, `WARNING_HIGH_STRESS`, `CRITICAL_MAINTENANCE_REQUIRED`).

## File Structure
- `predictive_pipeline.py`: Main python execution script containing data cleaning and analytical engines.
- `README.md`: Project integration guidelines.

## Execution Instructions
Run the data pipeline directly from a terminal using standard Python 3.x:
```bash
python predictive_pipeline.py
```

## Input/Output Specification
### Sample Raw Input Format
```json
{"timestamp": 1710000000, "temperature": 62.4, "vibration": 2.1}
{"timestamp": 1710003600, "temperature": null, "vibration": 2.3}
```
### Sample Processed Console Output
```text
Time: 1710000000 | Temp: 62.4°C | SmoothVib: 2.10 mm/s | Status: OPERATIONAL
Time: 1710014400 | Temp: 86.2°C | SmoothVib: 4.60 mm/s | Status: CRITICAL_MAINTENANCE_REQUIRED
```
