from cryptography.hazmat.primitives.asymmetric import rsa


from conf import *

ENVIRONMENT = 'TEST'
INFLUXDB_DISABLED = True

# Disable auth for unit tests
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = []
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = []

ENGINE_RPC_URL = "http://INTENTIONALLY_DISCONNECTED:9999"
INTERNAL_URL = "http://INTENTIONALLY_DISCONNECTED:9999"
PROFILES_URL = "DISABLED"
PROFILES_ENABLED = False

SUBSCRIBE_EVENTS = False

for name, logger in LOGGING['loggers'].items():
    logger['handlers'] = [h for h in logger.get('handlers', []) if h != 'elasticsearch']
    if logger.get('level') == 'DEBUG':
        logger['level'] = 'INFO'

JWT_AUTH['JWT_PRIVATE_KEY'] = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
JWT_AUTH['JWT_PUBLIC_KEY'] = JWT_AUTH['JWT_PRIVATE_KEY'].public_key()