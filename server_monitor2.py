
import socket 
import requests 
import time 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import schedule

"""
Logging

Logging is the process of recording information about events that occur in a software application. 
It involves writing messages to a log file or another logging system, which can then be used to monitor, debug, and understand the behavior of the application.

"""
# Configure logging
logging.basicConfig(filename='server_monitor.log',level=logging.INFO,format='%(asctime)s %(message)s')



"""
Uptime Monitoring

Checks whether a specified host(server) is reachable on a given port within a specified timeout period. It returns true if the server is up and reachable, and false otherwise.

"""


def check_uptime(host, port=80, timeout=5):
    """
    host : (str) the hostname or ip address of the server to check.
    port : (int) the port number on the host to connect to. Default is 80(common for http)
    timeout : (int) the maximum time (in seconds) to wait for the connection attempt before timing out. Default is 5 seconds.
    returns: (bool) True if the connection to the server is successful and false otherwise
    """
    try:
        # set the default timeout for socket operations
        socket.setdefaulttimeout(timeout)

        # create a new socket using IPv4 and TCP
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # sttempt to connect to the host on the specified port
        sock.connect((host,port))

        return True # if the connection was successful
    
    except socket.error as ex:

        # print the error message if the connection fails
        # print(f"Uptime check failed for {host}:{port} - {ex}")
        
        logging.error(f"Uptime check failed for {host}:{port} - {ex}")
        return False #if the connection failed

"""
Response Time Monitoring
"""


def check_response_time(url,timeout=5):
    """
    url : (str) the url of the website to check
    timeout : (int) timeout for the http rquest in seconds(default is 5)

    returns : (float) the response time in seconds and none if there is an error

    raises : requests.RequestException if there is any problem with the http request
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:

        # Record the start time before making the request
        start_time=time.time()

        # Send an HTTP GET request to the URL
        response=requests.get(url,headers=headers,timeout=timeout)
        
        # Raise an HTTP Error for bad status codes (4xx Client Errors or 5xx Server Errors)
        response.raise_for_status() #raises an error for bad status codes
        
        # Record the end time after receiving the response
        end_time=time.time()

        # Calculate and return the response time in seconds
        return end_time-start_time
    
    except requests.RequestException as ex:

        # Print an error message if there's an exception
        # print(f"Response time check failed for {url}-{ex}")
        
        logging.error(f"Response time check failed for {url} - {ex}") 
        return None # check Failed 


"""
Port Monitoring

checks if a port on a host is open by attempting a connection

"""

def check_port(host,port,timeout=5):
    """

    returns : (bool) true if the port is open and accessible, otherwise false
    """
    try:

        # set timeout for the connection attempt
        socket.setdefaulttimeout(timeout)

        #create a socket
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        #try to connect the host and port
        sock.connect((host,port))

        return True #port is open
    
    except socket.error as ex:

        #print error message if connection fails
        # print(f"Port check failed for {host}:{port}-{ex}")

        logging.error(f"Port check failed for {host}:{port} - {ex}")
        return False #port is closed or inaccessible
    

"""
Alerting
sends an emails using smtp
"""  

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_username, smtp_password):
    """

    subject : (str) the subject or title of the email
    body : (str) the main content of the mail
    to_email :(str) the recipient's mail address
    from_email : (str)the sender's email address
    smtp_server : (str)smtp server address ex: gmail.com
    smtp_port : (int) smtp server port number (ex: 587 for tls)
    smtp_username : (str)the username for authenticating with the smtp server
    smtp_password :(str)the password for authenticating with the smtp server

    returns : prints status messages whether the email is sent or not
    """

    #cretes new email message container
    msg=MIMEMultipart()

    #sets from,to,subject field of the email
    msg['From']=from_email
    msg['To']=to_email
    msg['Subject']=subject

    # Attach the plain text body of the email
    msg.attach(MIMEText(body,'plain'))

    try:
        #connect to smtp server
        server= smtplib.SMTP(smtp_server,smtp_port)

        #start a secure tls connection
        server.starttls()

        #log in to smtp server
        server.login(smtp_username,smtp_password)

        text=msg.as_string() #conver the message to string format
        server.sendmail(from_email,to_email,text) #send the email
        
        #close the connection
        server.quit()

        #print(f"Email sent to {to_email}") #success
        logging.info(f"Email sent to {to_email} with subject: {subject}")

    except Exception as ex:
        # print(f"Failed to send email - {ex}") #failed
        logging.error(f"Failed to send email - {ex}")


"""
*Monitoring the server*

monitor the server's availability, response time and port status. if any issues will be detected then it will send an email notification to the appropriate person.
"""

def monitor_server(host,url,port,to_email,from_email,smtp_server,smtp_port,smtp_username,smtp_password):
    
    logging.info(f"Starting server check for {host}")

    #try to establish a connection to a server.if false, then it means the server is down. so it will send an email indicating that the server is down.
    if not check_uptime(host,port):
        send_email("Server Down",f"The server {host} is down",to_email,from_email,smtp_server,smtp_port,smtp_username,smtp_password)
    
    
    #if true then, we check the response time
    else:
        response_time=check_response_time(url)

        if response_time is None or response_time>5:
            send_email("Slow Response",f"The server {host} is responding slowly. Response time : {response_time} seconds.", to_email,from_email,smtp_server,smtp_port,smtp_username,smtp_password)
        
        #if reponse time<5 then we check the port is open or closed
        if not check_port(host,port):
            send_email("Port Closed",f"The port {port} on server {host} is closed",to_email,from_email,smtp_server,smtp_port,smtp_username,smtp_password)


"""
Scheduling

Scheduling allows your server status checker to run checks at regular intervals
ensuring continuous monitoring without the need for manual execution.

This is useful for continuously monitoring a server to ensure its availability, check its response time, and verify the status of a specific port.
"""

def schedule_checks(interval, host, url, port, to_email, from_email, smtp_server, smtp_port, smtp_username, smtp_password):
    """
    interval : time intervl in minutes at which the monitor_server function should be run
    """
    
    #schedule the function to run every "interval" minutes
    schedule.every(interval).minutes.do(monitor_server,host,url, port, to_email, from_email, smtp_server, smtp_port, smtp_username, smtp_password)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        """
        the while loop : continuously checks and executes the scheduled tasks
        run_pending checks if any scheduled tasks are due to run, if it is due then it runs it
        time.sleep pauses the loop for 1 second before it starts over, it prevents the loop from running too fast and using up all the computer's processingpower
        """