import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import lambda_handler


def test_recipe_endpoint_success():
    """Test successful POST to /recipe endpoint"""
    event = {
        'requestContext': {
            'http': {
                'method': 'POST',
                'path': '/recipe'
            }
        },
        'body': json.dumps({
            'name': 'Test Recipe',
            'ingredients': ['ingredient1', 'ingredient2'],
            'calories': 500,
            'date': '2025-10-20'
        })
    }
    
    response = lambda_handler(event, {})
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['status'] == 'ok'
    print("✓ Test successful POST to /recipe endpoint passed")


def test_recipe_endpoint_missing_fields():
    """Test POST to /recipe endpoint with missing fields"""
    event = {
        'requestContext': {
            'http': {
                'method': 'POST',
                'path': '/recipe'
            }
        },
        'body': json.dumps({
            'name': 'Test Recipe'
            # Missing other required fields
        })
    }
    
    response = lambda_handler(event, {})
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['status'] == 'error'
    print("✓ Test POST with missing fields passed")


def test_recipe_endpoint_invalid_json():
    """Test POST to /recipe endpoint with invalid JSON"""
    event = {
        'requestContext': {
            'http': {
                'method': 'POST',
                'path': '/recipe'
            }
        },
        'body': 'invalid json'
    }
    
    response = lambda_handler(event, {})
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['status'] == 'error'
    print("✓ Test POST with invalid JSON passed")


def test_recipe_endpoint_not_found():
    """Test request to non-existent endpoint"""
    event = {
        'requestContext': {
            'http': {
                'method': 'GET',
                'path': '/notfound'
            }
        }
    }
    
    response = lambda_handler(event, {})
    
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body['status'] == 'error'
    print("✓ Test 404 not found passed")


if __name__ == '__main__':
    print("Running tests...")
    test_recipe_endpoint_success()
    test_recipe_endpoint_missing_fields()
    test_recipe_endpoint_invalid_json()
    test_recipe_endpoint_not_found()
    print("\nAll tests passed!")
