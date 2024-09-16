import json
import os

import requests
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()


def get_access():
    url = 'https://iam-datahub.visitfinland.com/auth/realms/Datahub/protocol/openid-connect/token'

    access_data = {
        'client_id': 'datahub-api',
        'client_secret': f'{os.getenv("SECRET_KEY")}',
        'grant_type': 'password',
        'username': f'{os.getenv("USERNAME")}',
        'password': f'{os.getenv("PASSWORD")}'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=access_data, headers=headers)
        access_token = response.json().get('access_token')
        return access_token
    except Exception as e:
        return JsonResponse(f"Error getting access token: {e}", status=400)


def make_api_request(query):
    request_url = 'https://api-datahub.visitfinland.com/graphql/v1/graphql'
    access_token = get_access()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    body = {
        'query': query,
    }

    try:
        response = requests.post(request_url, headers=headers, data=json.dumps(body))
        response_data = response.json()
        return response_data
    except Exception as e:
        return JsonResponse(f"Error getting access token: {e}", status=400)


def save_data(query, filename):
    with open(filename, 'w') as f:
        data = make_api_request(query)
        json.dump(data, f)


def get_cities_data():
    query = """{
                product (where: {
                            _and: [
                                {type:{_eq:attraction}},
                                {productTags:{tag:{_eq:"hiking_walking_trekking"}}},
                                {productTargetGroups:{targetGroupId:{_eq:b2c}}}
                            ]
                            }) {
                    postalAddresses {
                        city
                    }
                    productInformations {
                        name
                    }
                }
            }"""
    save_data(query, 'cities.json')


def get_all_products_data():
    query = """ {
                product (where: {
                    _and: [
                        {type:{_eq:attraction}},
                        {productTags:{tag:{_eq:"hiking_walking_trekking"}}},
                        {productTargetGroups:{targetGroupId:{_eq:b2c}}},
                    ]}){
                    productImages {
                        filename
                        altText
                        largeUrl
                    }
                    productInformations {
                        description
                        name
                        url
                    }
                    postalAddresses {
                        location
                        postalCode
                        streetName
                        city
                    }
                    productAvailableMonths{
                        month
                    }
                    productPricings {
                        fromPrice
                        toPrice
                    }
                }
            }"""
    save_data(query, 'data.json')


get_cities_data()
get_all_products_data()
