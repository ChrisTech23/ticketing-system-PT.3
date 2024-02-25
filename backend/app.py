from flask import Flask, request, jsonify  # Import necessary Flask modules
from flask_cors import CORS
from dynamodb import create_ticket, get_ticket_by_ticket_id, update_ticket, delete_ticket, dynamodb_item_to_json

app = Flask(__name__)  # Initialize Flask application
CORS(app)

@app.route('/')
def hello():
    return 'Hello, Flask is running!'

@app.route('/create-ticket', methods=['POST'])
def create_ticket_route():
    if request.method == 'POST':
        ticket_id = request.json.get('id')
        ticket_name = request.json.get('ticket_name')
        ticket_description = request.json.get('ticket_description')

        # Check if the task creation parameters are provided
        if ticket_id and ticket_name and ticket_description:
            response = create_ticket(ticket_id, ticket_name, ticket_description)
            return jsonify({'message': 'Ticket created successfully', 'response': response})
        else:
            return jsonify({'error': 'Missing Ticket creation parameters'}), 400  # Bad request
        
@app.route('/get-ticket/<ticket_id>', methods=['GET'])
def get_ticket_route(ticket_id):
    # Your existing logic to fetch the task
    ticket = get_ticket_by_ticket_id(ticket_id)  # This fetches the raw DynamoDB item
    if ticket:
        ticket_json = dynamodb_item_to_json(ticket)  # Convert to plain JSON
        return jsonify({'ticket': ticket_json})
    else:
        return jsonify({'message': 'No ticket found for the ticket_id'}), 404
    
@app.route('/update-ticket/<ticket_id>', methods=['PUT'])
def update_ticket_route(ticket_id):
    # Access request data
    updated_name = request.json.get('updated_name')
    updated_description = request.json.get('updated_description')

    # Debugging: Print or log the values
    print(f"id: {ticket_id}")
    print(f"updated_name: {updated_name}")
    print(f"updated_description: {updated_description}")

    # Call update_task function
    response = update_ticket(ticket_id, updated_name, updated_description)

    if response.get('Attributes'):
        return jsonify({'message': 'ticket updated successfully'})
    else:
        return jsonify({'message': 'Failed to update ticket'})
    
@app.route('/delete-ticket/<ticket_id>', methods=['DELETE'])
def delete_ticket_route(ticket_id):
    # Call delete_task function
    deleted = delete_ticket(ticket_id)

    if deleted:
        return jsonify({'message': 'Ticket deleted successfully'})
    else:
        return jsonify({'message': 'Failed to delete ticket'})


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode
