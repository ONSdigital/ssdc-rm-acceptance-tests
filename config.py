import json
import os
from pathlib import Path


class Config:
    EVENT_SCHEMA_VERSION = "v0.2_RELEASE"

    PUBSUB_PROJECT = os.getenv('PUBSUB_PROJECT', 'shared-project')
    PUBSUB_RECEIPT_TOPIC = os.getenv('PUBSUB_RECEIPT_TOPIC', 'event_receipt')
    PUBSUB_REFUSAL_TOPIC = os.getenv('PUBSUB_REFUSAL_TOPIC', 'event_refusal')
    PUBSUB_INVALID_CASE_TOPIC = os.getenv('PUBSUB_INVALID_CASE_TOPIC',
                                          'event_invalid-case')
    PUBSUB_PRINT_FULFILMENT_TOPIC = os.getenv('PUBSUB_PRINT_FULFILMENT_TOPIC', 'event_print-fulfilment')
    PUBSUB_SURVEY_LAUNCH_TOPIC = os.getenv('PUBSUB_SURVEY_LAUNCH_TOPIC',
                                           'event_survey-launch')
    PUBSUB_UAC_AUTHENTICATION_TOPIC = os.getenv('PUBSUB_UAC_AUTHENTICATION_TOPIC',
                                                'event_uac-authentication')
    PUBSUB_DEACTIVATE_UAC_TOPIC = os.getenv('PUBSUB_DEACTIVATE_UAC_TOPIC', 'event_deactivate-uac')
    PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC = os.getenv('PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC',
                                                     'event_update-sample-sensitive')
    PUBSUB_OUTBOUND_UAC_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_UAC_SUBSCRIPTION', 'event_uac-update_rh')
    PUBSUB_OUTBOUND_CASE_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_CASE_SUBSCRIPTION', 'event_case-update_rh')

    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST_CASE = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '6432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_CASE_CERTIFICATES = os.getenv('DB_CASE_CERTIFICATES', '')

    EXCEPTIONMANAGER_CONNECTION_HOST = os.getenv('EXCEPTIONMANAGER_CONNECTION_HOST', 'localhost')
    EXCEPTIONMANAGER_CONNECTION_PORT = os.getenv('EXCEPTIONMANAGER_CONNECTION_PORT', '8666')
    EXCEPTION_MANAGER_URL = f'http://{EXCEPTIONMANAGER_CONNECTION_HOST}:{EXCEPTIONMANAGER_CONNECTION_PORT}'

    SUPPORT_TOOL_HOST = os.getenv('SUPPORT_TOOL_HOST', 'localhost')
    SUPPORT_TOOL_PORT = os.getenv('SUPPORT_TOOL_PORT', '9999')
    SUPPORT_TOOL_API = f'http://{SUPPORT_TOOL_HOST}:{SUPPORT_TOOL_PORT}/api'

    NOTIFY_SERVICE_HOST = os.getenv('NOTIFY_SERVICE_HOST', 'localhost')
    NOTIFY_SERVICE_PORT = os.getenv('NOTIFY_SERVICE_PORT', '8162')
    NOTIFY_SERVICE_API = f'http://{NOTIFY_SERVICE_HOST}:{NOTIFY_SERVICE_PORT}/'

    NOTIFY_STUB_HOST = os.getenv('NOTIFY_STUB_HOST', 'localhost')
    NOTIFY_STUB_PORT = os.getenv('NOTIFY_STUB_PORT', '8917')
    NOTIFY_STUB_SERVICE = f'http://{NOTIFY_STUB_HOST}:{NOTIFY_STUB_PORT}'

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_rsa')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'dummy_secret')

    SUPPLIER_CONFIG_JSON_PATH = Path(
        os.getenv('SUPPLIER_CONFIG_JSON_PATH') or Path(__file__).parent.joinpath('dummy_supplier_config.json'))
    SUPPLIERS_CONFIG = json.loads(
        SUPPLIER_CONFIG_JSON_PATH.read_text()) \
        if SUPPLIER_CONFIG_JSON_PATH and SUPPLIER_CONFIG_JSON_PATH.exists() else None

    PROTOCOL = os.getenv('PROTOCOL', 'http')

    CASEAPI_SERVICE_HOST = os.getenv('CASEAPI_SERVICE_HOST', 'localhost')
    CASEAPI_SERVICE_PORT = os.getenv('CASEAPI_SERVICE_PORT', '8161')
    CASEAPI_SERVICE = f'{PROTOCOL}://{CASEAPI_SERVICE_HOST}:{CASEAPI_SERVICE_PORT}'
    CASE_API_CASE_URL = f'{CASEAPI_SERVICE}/cases/'

    RESOURCE_FILE_PATH = Path(os.getenv('RESOURCE_FILE_PATH') or Path(__file__).parent.joinpath('resources'))
