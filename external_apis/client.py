import os
import requests
from flask import current_app

class SemesterAPIClient:
    @staticmethod
    def get_semesters():
        url = f"{current_app.config['SEMESTER_API_URL']}/semesters"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

class ActivitiesAPIClient:
    @staticmethod
    def get_activities():
        url = f"{current_app.config['ACTIVITIES_API_URL']}/activities"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_activity(data):
        url = f"{current_app.config['ACTIVITIES_API_URL']}/activities"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()