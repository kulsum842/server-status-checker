# Server Status Checker

This Python project monitors the availability, response time, and port status of a server. It uses `logging` for event recording and `schedule` for scheduling checks at regular intervals.

## Features

- **Uptime Monitoring**: Checks if a server is reachable on a specified port.
- **Response Time Monitoring**: Measures the response time of a website.
- **Port Monitoring**: Checks if a specific port on a server is open.
- **Alerting**: Sends email notifications using SMTP when issues are detected.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kulsum842/server-status-checker.git
   cd server-status-checker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Modify `server_monitor.py` with your server details and email credentials:

```python
# Example usage in server_monitor.py

host = 'example.com'
url = 'https://example.com'
port = 80
to_email = 'recipient@example.com'
from_email = 'sender@example.com'
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'

schedule_checks(15, host, url, port, to_email, from_email, smtp_server, smtp_port, smtp_username, smtp_password)
```

Adjust `schedule_checks` interval and parameters according to your monitoring needs.

## Configuration

Ensure your email provider allows SMTP access and adjust security settings accordingly.

## Logging

All events are logged to `server_monitor.log` for easy debugging and monitoring.
