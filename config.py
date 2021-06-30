import json
import os
from pathlib import Path


class Config:
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_HTTP_PORT = os.getenv('RABBITMQ_HTTP_PORT', '16672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')

    RABBITMQ_SAMPLE_INBOUND_QUEUE = os.getenv('RABBITMQ_QUEUE', 'supportTool.caseProcessor.sample')

    RABBITMQ_EVENT_EXCHANGE = os.getenv('RABBITMQ_EVENT_EXCHANGE', 'events')

    RABBITMQ_REFUSAL_QUEUE = os.getenv('RABBITMQ_REFUSAL_QUEUE', 'events.caseProcessor.refusal')
    RABBITMQ_INVALID_ADDRESS_QUEUE = os.getenv('RABBITMQ_INVALID_ADDRESS_QUEUE', 'events.caseProcessor.invalidAddress')
    RABBITMQ_SURVEY_LAUNCHED_ROUTING_KEY = os.getenv('RABBITMQ_SURVEY_LAUNCHED_ROUTING_KEY',
                                                     'events.caseProcessor.surveyLaunched')

    RABBITMQ_RH_OUTBOUND_UAC_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_UAC_QUEUE', 'events.rh.uacUpdate')
    RABBITMQ_RH_OUTBOUND_CASE_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_CASE_QUEUE', 'events.rh.caseUpdate')

    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST_CASE = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '6432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_CASE_CERTIFICATES = os.getenv('DB_CASE_CERTIFICATES', '')

    EXCEPTIONMANAGER_CONNECTION_HOST = os.getenv('EXCEPTIONMANAGER_CONNECTION_HOST', 'localhost')
    EXCEPTIONMANAGER_CONNECTION_PORT = os.getenv('EXCEPTIONMANAGER_CONNECTION_PORT', '8666')
    EXCEPTION_MANAGER_URL = f'http://{EXCEPTIONMANAGER_CONNECTION_HOST}:{EXCEPTIONMANAGER_CONNECTION_PORT}'

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_rsa')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'dummy_secret')

    SUPPLIER_CONFIG_JSON_PATH = Path(
        os.getenv('SUPPLIER_CONFIG_JSON_PATH') or Path(__file__).parent.joinpath('dummy_supplier_config.json'))
    SUPPLIERS_CONFIG = json.loads(
        SUPPLIER_CONFIG_JSON_PATH.read_text())\
        if SUPPLIER_CONFIG_JSON_PATH and SUPPLIER_CONFIG_JSON_PATH.exists() else None

    RECEIPT_TOPIC_PROJECT = os.getenv('RECEIPT_TOPIC_PROJECT', 'project')
    RECEIPT_TOPIC_ID = os.getenv('RECEIPT_TOPIC_ID', 'eq-submission-topic')

    PROTOCOL = os.getenv('PROTOCOL', 'http')

    CASEAPI_SERVICE_HOST = os.getenv('CASEAPI_SERVICE_HOST', 'localhost')
    CASEAPI_SERVICE_PORT = os.getenv('CASEAPI_SERVICE_PORT', '8161')
    CASEAPI_SERVICE = f'{PROTOCOL}://{CASEAPI_SERVICE_HOST}:{CASEAPI_SERVICE_PORT}'
    CASE_API_CASE_URL = f'{CASEAPI_SERVICE}/cases/'
