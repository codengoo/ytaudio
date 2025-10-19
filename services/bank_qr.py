import requests


def generate_bank_qr(bank_code: str, account_number: str, account_name: str = "", amount: int = None):
    """
    Sinh link ảnh QR chuyển khoản VietQR (png)
    """

    base_url = f"https://img.vietqr.io/image/{bank_code}-{account_number}-qr_only.png"
    params = {}
    if account_name:
        params["accountName"] = account_name
    if amount:
        params["amount"] = amount

    resp = requests.Request("GET", base_url, params=params).prepare()
    return resp.url

def get_bank_qr_discord_id(discord_id: str):
    generate_bank_qr("", "", "")