from flask import Flask, render_template, request, jsonify
import requests
import time
import random

app = Flask(__name__)

# A list of common user agents to rotate through.
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckgo-help/faq-about-our-crawler)",
    "PostmanRuntime/7.30.1",
    "python-requests/2.28.1",
    # Non-browser / scripts / scrapers
    "curl/7.88.1",
    "Wget/1.21.3 (linux-gnu)",
    "python-requests/2.28.1",
    "python-urllib3/1.26.14",
    "Scrapy/2.9.0 (+https://scrapy.org)",
    "PostmanRuntime/7.32.3",
    "Go-http-client/2.0",
    "Java/11.0.19",
    "Apache-HttpClient/4.5.14 (Java/11.0.19)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
]

@app.route('/')
def index():
    """Renders the main page of the web application."""
    return render_template('index.html')

@app.route('/send_requests', methods=['POST'])
def send_requests():
    """
    Handles the request to send HTTP requests to the specified URLs.

    It receives the list of URLs and the number of requests from the form,
    then iterates through each URL, sends the specified number of requests
    with a random user agent, and returns a JSON response with the results.
    """
    try:
        # Get the list of URLs and the number of requests from the form data.
        urls = request.form.getlist('urls[]')
        num_requests_str = request.form.get('num_requests')

        # Validate the number of requests.
        try:
            num_requests = int(num_requests_str)
            if num_requests <= 0:
                return jsonify({'error': 'Number of requests must be a positive integer.'}), 400
        except ValueError:
            return jsonify({'error': 'Number of requests must be a valid integer.'}), 400
            
        # Validate that at least one URL is provided.
        if not urls:
            return jsonify({'error': 'At least one URL must be provided.'}), 400

        results = []
        # Loop through each URL and send the specified number of requests.
        for url in urls:
            print(f"\n--- Sending {num_requests} requests to {url} ---")
            url_results = []
            for i in range(num_requests):
                try:
                    # Randomly select a user agent.
                    random_user_agent = random.choice(user_agents)

                    # Set the headers with the random user agent.
                    headers = {
                        'User-Agent': random_user_agent
                    }

                    # Send the GET request.
                    response = requests.get(url, headers=headers)
                    status_code = response.status_code
                    success = "Success!" if status_code == 200 else f"Failed with status code {status_code}"
                    
                    url_results.append({
                        'request_num': i + 1,
                        'user_agent': random_user_agent,
                        'status_code': status_code,
                        'message': success
                    })

                except requests.exceptions.RequestException as e:
                    url_results.append({
                        'request_num': i + 1,
                        'user_agent': random_user_agent,
                        'status_code': 'N/A',
                        'message': f"An error occurred: {e}"
                    })

                # Sleep for 1 second between requests.
                if i < num_requests - 1:
                    time.sleep(1)

            results.append({
                'url': url,
                'requests': url_results
            })

        return jsonify({'message': 'Requests sent successfully.', 'results': results})

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)