import boto3
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

def initialize_dynamodb_client():
    # Initialize DynamoDB client using environment variables
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )
    return dynamodb

def list_tables():
    # Initialize DynamoDB client
    dynamodb = initialize_dynamodb_client()

    # List DynamoDB tables
    response = dynamodb.list_tables()
    return response['TableNames']

# ... (previous code remains unchanged)

def create_ticket(ticket_id, ticket_name, ticket_description):
    dynamodb = initialize_dynamodb_client()
    table_name = "tickets"

    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                'id': {'S': ticket_id},
                'ticket_name': {'S': ticket_name},
                'ticket_description': {'S': ticket_description}
                # Add other attributes as needed based on your schema
            }
        )
        return response
    except dynamodb.exceptions.ClientError as e:
        # Handle any potential errors, log them, and potentially return a specific error message
        print(f"Error creating ticket: {e}")
        return {"error": "Failed to create ticket"}
    
    # Assuming this function is in your dynamodb_interactions.py or a similar file
def dynamodb_item_to_json(item):
    # Check if the item is empty or already in JSON format (not containing DynamoDB data type annotations)
    if not item or all(not isinstance(value, dict) for value in item.values()):
        print("Item already in JSON format or empty:", item)
        return item
    
    # Initialize an empty dictionary for the JSON data
    json_data = {}
    
    # Process each key-value pair in the item
    for key, value in item.items():
        print(f"Processing key: {key}, Value: {value}")  # Debugging line to show the process
        if 'S' in value:
            json_data[key] = value['S']  # Handle string data type
        elif 'N' in value:
            json_data[key] = str(value['N'])  # Handle number data type, convert to string for JSON compatibility
        elif 'BOOL' in value:
            json_data[key] = value['BOOL']  # Handle boolean data type
        # Add handling for other DynamoDB data types ('L', 'M', etc.) here as needed
    
    print("Transformed JSON Data:", json_data)  # Debugging line to show the transformed JSON data
    return json_data

# Modify the get_task_by_task_id function to use this conversion:
def get_ticket_by_ticket_id(ticket_id):
    dynamodb = initialize_dynamodb_client()
    table_name = "tickets"  # Make sure this matches your actual table name
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {'S': ticket_id}
        }
    )
    item = response.get('Item', None)
    if item:
        return dynamodb_item_to_json(item)
    return {}  # Return an empty dict if the task was not found

def update_ticket(ticket_id, updated_name, updated_description):
    # Initialize DynamoDB client
    dynamodb = initialize_dynamodb_client()

    # Define your DynamoDB table name for tasks
    table_name = "tickets"  # Replace with your actual table name

    # Update task details in DynamoDB
    response = dynamodb.update_item(
        TableName=table_name,
        Key={'id': {'S': ticket_id}},
        UpdateExpression='SET ticket_name = :name, ticket_description = :desc',
        ExpressionAttributeValues={
            ':name': {'S': updated_name},
            ':desc': {'S': updated_description}
        },
        ReturnValues='UPDATED_NEW'
    )
    return response

def delete_ticket(ticket_id):

    # Initialize DynamoDB client
    dynamodb = initialize_dynamodb_client()

    # Define your DynamoDB table name for tasks
    table_name = "tickets"

    # Delete the task from DynamoDB
    response = dynamodb.delete_item(
        TableName=table_name,
        Key={
            'id': {'S': ticket_id}
        }
    )

    # Check if the deletion was successful
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return True
    else:
        return False

# Entry point of the script
if __name__ == "__main__":
    tables = list_tables()
    print("List of DynamoDB tables:", tables)