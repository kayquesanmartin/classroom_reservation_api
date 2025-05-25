import os
import requests
from flask import current_app
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

class APIClientBase:
    @classmethod
    def _create_session(cls):
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @classmethod
    def _make_request(cls, method, url, **kwargs):
        session = cls._create_session()
        try:
            response = session.request(
                method,
                url,
                timeout=5,  # 5 segundos para conexão e leitura
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            raise

class SemesterAPIClient(APIClientBase):
    @staticmethod
    def get_semesters():
        url = f"{current_app.config['SEMESTER_API_URL']}/semesters"
        response = SemesterAPIClient._make_request('GET', url)
        return response.json()

    @staticmethod
    def get_turma(turma_id):
        """Método específico para buscar uma turma pelo ID"""
        url = f"{current_app.config['SEMESTER_API_URL']}/turmas/{turma_id}"
        try:
            response = SemesterAPIClient._make_request('GET', url)
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

class ActivitiesAPIClient:
    @staticmethod
    def get_activities():
        url = f"{current_app.config['ACTIVITIES_API_URL']}/activities"
        response = ActivitiesAPIClient._make_request(
            'GET',
            url
        )
        return response.json()

    @staticmethod
    def create_activity(data):
        url = f"{current_app.config['ACTIVITIES_API_URL']}/activities"
        response = ActivitiesAPIClient._make_request(
            'POST',
            url,
            json=data
        )
        return response.json()