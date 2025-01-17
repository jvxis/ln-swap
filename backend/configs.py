from os.path import expanduser
from os import environ, makedirs

PATH = expanduser("~/vinci")

makedirs(f"{PATH}/data", exist_ok=True)

# API configuration.
API_HOST = environ.get("API_HOST", "0.0.0.0")
API_PORT = int(environ.get("API_PORT", 1536))

# Mirrors configuration.
MIRRORS_CLEAR_URL = environ.get("MIRRORS_CLEAR_URL", "").split(",")
if (MIRRORS_CLEAR_URL) and not (MIRRORS_CLEAR_URL[0]):
    MIRRORS_CLEAR_URL = []

MIRRORS_TOR_URL = environ.get("MIRRORS_TOR_URL", "").split(",")
if (MIRRORS_TOR_URL) and not (MIRRORS_TOR_URL[0]):
    MIRRORS_TOR_URL = []

# Lightning configuration.
INVOICE_EXPIRE = int(environ.get("INVOICE_EXPIRE", (60 * 15)))

# Lnd configuration.
LND_HOST = environ.get("LND_HOST", "https://127.0.0.1:8080")
LND_MACAROON = environ.get("LND_MACAROON")
LND_CERTIFICATE = environ.get("LND_CERTIFICATE", False)

# Redis configuration.
REDIS_HOST = environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = environ.get("REDIS_PORT", 6379)
REDIS_PASS = environ.get("REDIS_PASS", "")

# Swap configuration.
SWAP_SERVICE_FEERATE = float(environ.get("SWAP_SERVICE_FEERATE", 20))
SWAP_MAX_AMOUNT = int(environ.get("SWAP_MAX_AMOUNT", 100000000))
SWAP_MIN_AMOUNT = int(environ.get("SWAP_MIN_AMOUNT", 100000))

# Lnbits configuration.
LNBITS_HOST = environ.get("LNBITS_HOST", "https://legend.lnbits.com/api")
LNBITS_BASE_URL = environ.get("LNBITS_BASE_URL", "https://www.lnbits.com")
LNBITS_WEBHOOK_URL = environ.get("LNBITS_WEBHOOK_URL", f"http://127.0.0.1:{API_PORT}/api/v1/lnbits/webhook")

LNBITS_MAIN_WALLET_ADMIN_KEY = environ["LNBITS_MAIN_WALLET_ADMIN_KEY"]
LNBITS_MAIN_WALLET_INVOICE_KEY = environ["LNBITS_MAIN_WALLET_INVOICE_KEY"]
