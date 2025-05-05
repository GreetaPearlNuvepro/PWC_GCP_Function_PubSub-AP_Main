import base64 
def process_analysis_results(event, context): 
    """Cloud Function triggered by messages published to Pub/Sub topic.""" 
    # Extract message data 
    message_data = event['data'] 
    # Decode the base64-encoded message 
    decoded_message = base64.b64decode(message_data).decode('utf-8') 
     
    # Print the decoded analysis results 
    print("Received analysis results:", decoded_message) 