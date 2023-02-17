import json
import os
from distutils.util import strtobool
from pathlib import Path

from jwcrypto import jwk


class Config:
    EVENT_SCHEMA_VERSION = "0.5.0"

    RESOURCE_FILE_PATH = Path(os.getenv('RESOURCE_FILE_PATH') or Path(__file__).parent.joinpath('resources'))

    PUBSUB_PROJECT = os.getenv('PUBSUB_PROJECT', 'our-project')

    PUBSUB_RECEIPT_TOPIC = os.getenv('PUBSUB_RECEIPT_TOPIC', 'event_receipt')
    PUBSUB_REFUSAL_TOPIC = os.getenv('PUBSUB_REFUSAL_TOPIC', 'event_refusal')
    PUBSUB_INVALID_CASE_TOPIC = os.getenv('PUBSUB_INVALID_CASE_TOPIC',
                                          'event_invalid-case')
    PUBSUB_PRINT_FULFILMENT_TOPIC = os.getenv('PUBSUB_PRINT_FULFILMENT_TOPIC', 'event_print-fulfilment')
    PUBSUB_EQ_LAUNCH_TOPIC = os.getenv('PUBSUB_EQ_LAUNCH_TOPIC',
                                       'event_eq-launch')
    PUBSUB_UAC_AUTHENTICATION_TOPIC = os.getenv('PUBSUB_UAC_AUTHENTICATION_TOPIC',
                                                'event_uac-authentication')
    PUBSUB_DEACTIVATE_UAC_TOPIC = os.getenv('PUBSUB_DEACTIVATE_UAC_TOPIC', 'event_deactivate-uac')
    PUBSUB_UPDATE_SAMPLE_TOPIC = os.getenv('PUBSUB_UPDATE_SAMPLE_TOPIC', 'event_update-sample')
    PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC = os.getenv('PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC',
                                                     'event_update-sample-sensitive')
    PUBSUB_OUTBOUND_UAC_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_UAC_SUBSCRIPTION', 'event_uac-update_rh_at')
    PUBSUB_OUTBOUND_CASE_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_CASE_SUBSCRIPTION', 'event_case-update_rh_at')
    PUBSUB_OUTBOUND_SURVEY_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_SURVEY_SUBSCRIPTION', 'event_survey-update_rh_at')
    PUBSUB_OUTBOUND_COLLECTION_EXERCISE_SUBSCRIPTION = os.getenv('PUBSUB_OUTBOUND_COLLECTION_EXERCISE_SUBSCRIPTION',
                                                                 'event_collection-exercise-update_rh_at')
    PUBSUB_NEW_CASE_TOPIC = os.getenv('PUBSUB_NEW_CASE_TOPIC', 'event_new-case')
    PUBSUB_CLOUD_TASK_QUEUE_AT_SUBSCRIPTION = os.getenv('PUBSUB_CLOUD_TASK_QUEUE_AT_SUBSCRIPTION',
                                                        'cloud_task_queue_at')
    PUBSUB_NIFI_INTERNAL_PRINT_NOTIFICATION_SUBSCRIPTION = os.getenv(
        'PUBSUB_NIFI_INTERNAL_PRINT_NOTIFICATION_SUBSCRIPTION', 'export_file_nifi_notification')
    PUBSUB_DEFAULT_PULL_TIMEOUT = int(os.getenv('PUBSUB_DEFAULT_PULL_TIMEOUT', 120))

    DB_USERNAME = os.getenv('DB_USERNAME', 'appuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST_CASE = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '6432')
    DB_NAME = os.getenv('DB_NAME', 'rm')
    DB_CASE_CERTIFICATES = os.getenv('DB_CASE_CERTIFICATES', '')

    EXCEPTIONMANAGER_CONNECTION_HOST = os.getenv('EXCEPTIONMANAGER_CONNECTION_HOST', 'localhost')
    EXCEPTIONMANAGER_CONNECTION_PORT = os.getenv('EXCEPTIONMANAGER_CONNECTION_PORT', '8666')
    EXCEPTION_MANAGER_URL = f'http://{EXCEPTIONMANAGER_CONNECTION_HOST}:{EXCEPTIONMANAGER_CONNECTION_PORT}'

    SUPPORT_TOOL_HOST = os.getenv('SUPPORT_TOOL_HOST', 'localhost')
    SUPPORT_TOOL_PORT = os.getenv('SUPPORT_TOOL_PORT', '9999')
    SUPPORT_TOOL_API = f'http://{SUPPORT_TOOL_HOST}:{SUPPORT_TOOL_PORT}/api'
    SUPPORT_TOOL_URL = f'http://{SUPPORT_TOOL_HOST}:{SUPPORT_TOOL_PORT}'

    NOTIFY_SERVICE_HOST = os.getenv('NOTIFY_SERVICE_HOST', 'localhost')
    NOTIFY_SERVICE_PORT = os.getenv('NOTIFY_SERVICE_PORT', '8162')
    NOTIFY_SERVICE_API = f'http://{NOTIFY_SERVICE_HOST}:{NOTIFY_SERVICE_PORT}/'

    NOTIFY_STUB_HOST = os.getenv('NOTIFY_STUB_HOST', 'localhost')
    NOTIFY_STUB_PORT = os.getenv('NOTIFY_STUB_PORT', '8917')
    NOTIFY_STUB_SERVICE = f'http://{NOTIFY_STUB_HOST}:{NOTIFY_STUB_PORT}'

    EXPORT_FILE_DESTINATION_CONFIG_JSON_PATH = Path(
        os.getenv('EXPORT_FILE_DESTINATION_CONFIG_JSON_PATH') or Path(__file__).parent.joinpath(
            'dummy_export_file_destination_config.json'))
    EXPORT_FILE_DESTINATIONS_CONFIG = json.loads(
        EXPORT_FILE_DESTINATION_CONFIG_JSON_PATH.read_text()) \
        if EXPORT_FILE_DESTINATION_CONFIG_JSON_PATH and EXPORT_FILE_DESTINATION_CONFIG_JSON_PATH.exists() else None
    FILE_UPLOAD_DESTINATION = os.getenv('FILE_UPLOAD_DESTINATION', str(Path.home().joinpath('Documents/export_files')))
    FILE_UPLOAD_MODE = os.getenv('FILE_UPLOAD_MODE', 'LOCAL')
    OUR_EXPORT_FILE_DECRYPTION_KEY = os.getenv(
        'OUR_EXPORT_FILE_DECRYPTION_KEY',
        str(RESOURCE_FILE_PATH.joinpath('dummy_keys',
                                        'dummy-key-ssdc-rm-private.asc'))
    )
    OUR_EXPORT_FILE_DECRYPTION_KEY_PASSPHRASE = os.getenv('OUR_EXPORT_FILE_DECRYPTION_KEY_PASSPHRASE', 'test')

    PROTOCOL = os.getenv('PROTOCOL', 'http')

    CASEAPI_SERVICE_HOST = os.getenv('CASEAPI_SERVICE_HOST', 'localhost')
    CASEAPI_SERVICE_PORT = os.getenv('CASEAPI_SERVICE_PORT', '8161')
    CASEAPI_SERVICE = f'{PROTOCOL}://{CASEAPI_SERVICE_HOST}:{CASEAPI_SERVICE_PORT}'
    CASE_API_CASE_URL = f'{CASEAPI_SERVICE}/cases/'

    RH_UI_HOST = os.getenv('RH_UI_HOST', 'localhost')
    RH_UI_PORT = os.getenv('RH_UI_PORT', '9092')
    RH_UI_URL = f'{PROTOCOL}://{RH_UI_HOST}:{RH_UI_PORT}/'

    EQ_DECRYPTION_JSON_FILE = Path(os.getenv('EQ_JSON_FILE') or RESOURCE_FILE_PATH.joinpath('dummy_keys',
                                                                                            'eq-decrypt-keys.json'))
    JWT_DICT = json.load(open(EQ_DECRYPTION_JSON_FILE))
    EQ_DECRYPTION_KEY = jwk.JWK.from_pem(JWT_DICT['jwePrivateKey']['value'].encode())
    EQ_VERIFICATION_KEY = jwk.JWK.from_pem(JWT_DICT['jwsPublicKey']['value'].encode())

    SAMPLE_LOAD_ORIGINATING_USER = os.getenv('ORIGINATING_USER', 'dummy@fake-email.com')

    CODE_GUIDE_MARKDOWN_FILE_PATH = Path(
        os.getenv('CODE_GUIDE_MARKDOWN_FILE_PATH') or Path(__file__).parent.joinpath('CODE_GUIDE.md'))

    HEADLESS = strtobool(os.getenv('HEADLESS', 'True'))
    SAMPLE_FILES_PATH = RESOURCE_FILE_PATH.joinpath('sample_files')
    EQ_LAUNCH_SETTINGS_FILE_PATH = RESOURCE_FILE_PATH.joinpath('eq_launch_settings')

    EQ_FLUSH_STUB_URL = os.getenv('EQ_FLUSH_STUB_URL', 'http://eq-stub')
