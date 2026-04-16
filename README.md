# UserAgentSpoofer

**UserAgentSpoofer** is a Flask-based web application designed to send multiple HTTP requests to specified URLs while rotating User-Agent strings. This tool is primarily intended for security testing, allowing users to evaluate how Web Application Firewalls (WAF) and bot detection solutions handle varying request headers.

## How It Works

The core objective of this project is to simulate organic-looking traffic by ensuring that no two consecutive requests necessarily share the same identity. 

* **User-Agent Rotation**: For every request sent, the application randomly selects a User-Agent from a comprehensive list of common browser and crawler strings (e.g., Chrome, Safari, Firefox, Googlebot).
* **Traffic Simulation**: By using the Python `random` library to select these agents, the traffic appears more like it is originating from multiple different users and devices.
* **Request Throttling**: The application implements a 1-second delay between requests to a specific URL to maintain a steady, non-bursty flow of traffic.

## Features

* **Multi-URL Support**: Add multiple target URLs to a queue for testing.
* **Customizable Volume**: Specify the exact number of requests to be sent to each URL.
* **Live Results**: View the status code, User-Agent used, and success/failure message for every individual request directly in the browser.

## How to Use

### 1. Installation
First, ensure you have the necessary dependencies installed using `uv` or `pip`:
```bash
uv add -r requirements.txt
# OR
pip install -r requirements.txt
```

### 2. Run the Application
Start the Flask server:
```bash
bash flask-cmd.sh
# OR
python app.py
```

### 3. Send Requests
1.  Open your browser and navigate to the local server (usually `http://127.0.0.1:5000`).
2.  **Add URLs**: Enter the target URL in the input field and click the **Add** button. You can repeat this for multiple URLs.
3.  **Set Quantity**: Enter the number of requests you wish to send in the "Number of Requests" field.
4.  **Start Testing**: Click the **Start** button. The application will display a loading spinner while requests are being processed.
5.  **Review Results**: Once complete, a detailed breakdown for each URL and request will appear in the "Results" section.

## Project Structure

* `app.py`: The main Flask backend handling the request logic and User-Agent rotation.
* `templates/index.html`: The web interface for managing URLs and viewing results.
* `static/`: Contains UI assets like the loading spinner and favicon.