import json


def lambda_handler(event, context):
    """
    AWS Lambda handler for the /recipe endpoint.
    
    Accepts POST requests with JSON body containing:
    - name: Recipe name
    - ingredients: List of ingredients
    - calories: Calorie count
    - date: Date of the recipe
    
    Returns: {"status": "ok"}
    """
    
    # Extract HTTP method and path
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('requestContext', {}).get('http', {}).get('path', '')
    
    # Route to /recipe endpoint
    if path == '/recipe' and http_method == 'POST':
        try:
            # Parse the request body
            if 'body' in event:
                body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                
                # Validate required fields
                required_fields = ['name', 'ingredients', 'calories', 'date']
                if all(field in body for field in required_fields):
                    # Process the recipe data (in a real application, you would save this to a database)
                    # For now, we just return success
                    
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'application/json'
                        },
                        'body': json.dumps({'status': 'ok'})
                    }
                else:
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json'
                        },
                        'body': json.dumps({
                            'status': 'error',
                            'message': 'Missing required fields: name, ingredients, calories, date'
                        })
                    }
            else:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'status': 'error',
                        'message': 'No body provided'
                    })
                }
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Invalid JSON'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'status': 'error',
                    'message': str(e)
                })
            }
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'status': 'error',
                'message': 'Not found'
            })
        }
