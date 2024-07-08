
# Server Monitoring in Python

This Python script monitors server uptime, response times of web URLs, and checks port accessibility. It sends email alerts using SMTP in case of issues such as downtime, slow response times, or closed ports.

## Features

- **Uptime Monitoring:** Checks if a server is reachable using socket connections.
- **Response Time Monitoring:** Measures response times of web URLs using the requests library.
- **Port Monitoring:** Verifies port accessibility using socket connections.
- **Email Alerts:** Sends notifications via SMTP when issues are detected.

## Usage

1. **Installation:**
   - Clone the repository:
     ```
     git clone https://github.com/your-username/server-monitoring-python.git
     ```
2. **Configuration:**
   - Edit the `monitor_server.py` script to customize host, URL, port, email settings, SMTP server, and credentials.

3. **Run the Script:**
   - Execute the script:
     ```
     python monitor_server.py
     ```

4. **Example:**
   - Monitor 'example.com' for uptime, response time, and port 80 status:
     ```python
     host = 'example.com'
     url = 'https://example.com'
     port = 80
     to_email = 'your-email@example.com'
     from_email = 'your-email@example.com'
     smtp_server = 'smtp.example.com'
     smtp_port = 587
     smtp_username = 'your-username'
     smtp_password = 'your-password'

     monitor_server(host, url, port, to_email, from_email, smtp_server, smtp_port, smtp_username, smtp_password)
     ```

### Notes:

- Ensure Python and necessary dependencies (`requests`, `smtplib`) are installed.
- Customize email settings and monitoring parameters according to your requirements.
