from configs import PATH, LNBITS_HOST, LNBITS_BASE_URL, LNBITS_MAIN_WALLET_INVOICE_KEY, LNBITS_MAIN_WALLET_ADMIN_KEY, LNBITS_WEBHOOK_URL
from os.path import exists
from lnbits import Lnbits
from json import loads, load, dump
from re import search

import requests
import logging
import sys

if not (LNBITS_MAIN_WALLET_ADMIN_KEY):
    if exists(PATH + "/data/wallet.json"):
        wallet = load(open(PATH + "/data/wallet.json"))
    else:
        wallet = {}

    if not wallet:
        try:
            location = requests.get(f"{LNBITS_BASE_URL}/wallet?nme=default", allow_redirects=False).headers["Location"]
            wallet_keys = loads(search(r"window\.wallet = ({.*});", requests.get(f"{LNBITS_BASE_URL}{location}").text).group(1))
        except:
            logging.critical("Unable to connect with Lnbits.")
            logging.critical("Exit")
            sys.exit(0)

        LNBITS_MAIN_WALLET_ADMIN_KEY = wallet_keys["adminkey"]
        LNBITS_MAIN_WALLET_INVOICE_KEY = wallet_keys["inkey"]    
        with open(PATH + "/data/wallet.json", "w") as w:
            wallet = {"LNBITS_MAIN_WALLET_ADMIN_KEY": LNBITS_MAIN_WALLET_ADMIN_KEY, "LNBITS_MAIN_WALLET_INVOICE_KEY": LNBITS_MAIN_WALLET_INVOICE_KEY}
            dump(wallet, w)
    else:
        LNBITS_MAIN_WALLET_ADMIN_KEY = wallet["LNBITS_MAIN_WALLET_ADMIN_KEY"]
        LNBITS_MAIN_WALLET_INVOICE_KEY = wallet["LNBITS_MAIN_WALLET_INVOICE_KEY"]

lnbits = Lnbits(admin_key=LNBITS_MAIN_WALLET_ADMIN_KEY, invoice_key=LNBITS_MAIN_WALLET_INVOICE_KEY, url=LNBITS_HOST)
try:
    if (lnbits.get_wallet().get("detail")):
        raise Exception("Wallet does not exist.")
except:
    logging.critical("Unable to connect with Lnbits.")
    logging.critical("Exit")
    sys.exit(0)

def create_invoice(amount: int, memo="", expiry=86400) -> dict:
    """Create a new lightning invoice containing metadata that will be used in 
    later contracts for debt settlement.
    """

    invoice = lnbits.create_invoice(amount, memo=memo, webhook=LNBITS_WEBHOOK_URL)
    if not invoice.get("payment_hash"):
        return {"message": invoice}
    
    # Get the hash payment.
    payment_hash = invoice["payment_hash"]

    # Get payment request.
    payment_request = invoice["payment_request"]
    return {"payment_hash": payment_hash, "payment_request": payment_request, "expiry": expiry}
