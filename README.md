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

- Python 3.12.4

Install the dependencies with:

```bash
pip install pandas pm4py matplotlib
```

### Installation

1. Clone the repository:

```bash
git clone [https://github.com/username/vle-process-mining-api.git](https://github.com/AkiraTorres/moodle-spm-api.git)
cd vle-process-mining-api
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

### Usage



#### 2. Start the API

Run the server to start the API:

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `[http://localhost:5000](http://localhost:8000)`.

#### 3. API Endpoints

### Example: Process Mining Analysis

Once logs are uploaded, you can use the `/discover-patterns` endpoint to extract patterns. The API will return insights such as frequent action sequences, loops, and other common behaviors among students.

### Configuration


- **Algorithm Parameters**: You can adjust the thresholds and filtering parameters via the API endpoints to customize the pattern discovery process.
- Preprocessing Strategies: You can select preprocessing strategies for the code that will be executed on the database, before the mining part of the process begins

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/AkiraTorres/moodle-spm-api/issues).
