import json

def handler(event, context):
  print('request: {}'.format(json.dumps(event)))
  return {
    'statusCode': 200,
    'headers': {
      'Content-Type': 'text/plain'
    },
    'body': 'V2. Hello, CDK ! You have hit {}\n'.format(event['path'])

  }

  # return {
  #   'body': 'Oops',
  #   'statusCode': '500'
  # }