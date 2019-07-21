import pytesseract
import PIL.Image
import io
import os
import json
from base64 import b64decode

LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
print("LAMBDA_TASK_ROOT ", LAMBDA_TASK_ROOT)
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT


def lambda_handler(event, context):
  print("Event Passed to Handler: " + json.dumps(event))
  
  if 'body' not in event or len(event['body']) ==0 :
    return {
      'statusCode': 400,
      'headers': {'Content-Type': 'application/json'},
      'body': json.dumps({'reco': "bad request"})
    }

  try:
    image_base64 = event['body']
    binary = b64decode(image_base64)
    image = PIL.Image.open(io.BytesIO(binary))
    text = pytesseract.image_to_string(image, config='--psm 6')
  except:
    return {
      'statusCode': 500,
      'headers': {'Content-Type': 'application/json'},
      'body': json.dumps({'reco': "server internal error"})
    }
    
  return {
      'statusCode': 200,
      'headers': {'Content-Type': 'application/json'},
      'body': json.dumps({'reco': text})
  }
