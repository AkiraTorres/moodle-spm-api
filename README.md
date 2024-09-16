# Process Mining API for Student Activity Logs

This API implements a process mining algorithm designed to identify patterns in student activity logs from virtual learning environments (VLEs). The goal is to extract insights about learning behaviors, optimize course design, and identify potential improvements in student engagement.

## Features

- **Process Mining**: Detect frequent patterns in student activities.
- **Activity Logs**: Analyze actions such as logins, submissions, and content access.
- **Pattern Identification**: Generate visual representations and statistics about student behavior patterns.
- **Customizable Parameters**: Define timeframes, types of actions, and thresholds for pattern recognition.
- **Export Results**: Export discovered patterns as JSON, CSV, or visual diagrams.

## Getting Started

### Prerequisites

- Python 3.8+
- `pandas`, `pm4py`, and `matplotlib` libraries.

Install the dependencies with:

```bash
pip install pandas pm4py matplotlib
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/username/vle-process-mining-api.git
cd vle-process-mining-api
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

### Usage

#### 1. Load Student Logs
To begin analyzing logs, prepare your dataset in a CSV format with columns such as `student_id`, `action`, `timestamp`, and `course_id`.

Example:

```csv
student_id, action, timestamp, course_id
1, login, 2023-01-01 10:00:00, CS101
1, view_content, 2023-01-01 10:05:00, CS101
2, submit_assignment, 2023-01-01 11:00:00, CS101
...
```

#### 2. Start the API

Run the server to start the API:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

#### 3. API Endpoints

- **Upload Logs**: Upload the activity logs in CSV format.

  **POST** `/upload`
  - Body: CSV file containing student logs.
  
  Example:
  ```bash
  curl -F "file=@student_logs.csv" http://localhost:5000/upload
  ```

- **Discover Patterns**: Run the process mining algorithm on the logs.

  **GET** `/discover-patterns`
  - Query Parameters:
    - `course_id` (optional): Filter by specific course.
    - `threshold` (optional): Minimum occurrence of a pattern to be identified.
    
  Example:
  ```bash
  curl "http://localhost:5000/discover-patterns?course_id=CS101&threshold=5"
  ```

- **Export Results**: Export the identified patterns.

  **GET** `/export-results`
  - Query Parameters:
    - `format`: Output format (`json`, `csv`, or `diagram`).
    
  Example:
  ```bash
  curl "http://localhost:5000/export-results?format=json"
  ```

### Example: Process Mining Analysis

Once logs are uploaded, you can use the `/discover-patterns` endpoint to extract patterns. The API will return insights such as frequent action sequences, loops, and other common behaviors among students.

### Configuration

- **Log Structure**: Ensure that your log files follow the structure `student_id, action, timestamp, course_id` to allow the algorithm to parse events properly.
- **Algorithm Parameters**: You can adjust the thresholds and filtering parameters via the API endpoints to customize the pattern discovery process.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/username/vle-process-mining-api/issues).
