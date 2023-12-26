from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get JSON data from the POST request
    data = request.json
    print("Data received from Zapier:", data)
    
    # Process your data here or save it to your database
    
    # Respond with a message or with the processed result
    return jsonify({"status": "success", "message": "Data received"})

if __name__ == '__main__':
    # Run the server on all interfaces on port 5000
    app.run(host='0.0.0.0', port=5002)