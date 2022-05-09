import hmac
import hashlib
import base64


# These values are required to calculate the signature. Do not change them.
DATE = "11111111"
SERVICE = "ses"
MESSAGE = "SendRawEmail"
TERMINAL = "aws4_request"
VERSION = 0x04


def run(
    SESRegion,
    AWSSecretAccessKey=None,
    env={},
):
    """
    Generate a Sig4 based SMTP password from a provided secret access key
    Used with SES to send emails via SMTP
    """

    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    signature = sign(("AWS4" + AWSSecretAccessKey).encode("utf-8"), DATE)
    signature = sign(signature, SESRegion)
    signature = sign(signature, SERVICE)
    signature = sign(signature, TERMINAL)
    signature = sign(signature, MESSAGE)
    signature_and_version = bytes([VERSION]) + signature
    smtp_password = base64.b64encode(signature_and_version)

    return {
        "Properties": {
            "smtp_password": smtp_password.decode("utf-8"),
        }
    }
