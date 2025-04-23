import os 
from google.cloud import vision 
from google.cloud import pubsub_v1 

# Initialize Vision API client 
vision_client = vision.ImageAnnotatorClient() 

# Initialize Pub/Sub publisher client 
publisher = pubsub_v1.PublisherClient() 

def process_image(data, context): 

    """Cloud Function triggered by image upload to Cloud Storage.""" 
    # Extract file information 
    bucket_name = data['bucket'] 
    file_name = data['name'] 
    # Perform image analysis 
    image_uri = f"gs://{bucket_name}/{file_name}" 
    image = vision.Image() 
    image.source.image_uri = image_uri 
    response = vision_client.label_detection(image=image) 
    labels = [label.description for label in response.label_annotations]    
# Publish analysis results to Pub/Sub topic 
    publish_to_pubsub(labels) 


def publish_to_pubsub(labels): 
    """Publish analysis results to Pub/Sub topic.""" 
    topic_id = 'image-analysis-results' 
    topic_path = publisher.topic_path('your-project-id', topic_id) 
    # Convert labels to string 
    message_data = ', '.join(labels).encode('utf-8') 
    # Publish message to Pub/Sub topic 
    future = publisher.publish(topic_path, data=message_data) 

    future.result() 