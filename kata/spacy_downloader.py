import spacy
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

os.environ["REQUESTS_CA_BUNDLE"] = "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

# Create a session and mount the SSLAdapter
session = requests.Session()
session.mount('https://', SSLAdapter())

# Use the session to download the model
url = "https://raw.githubusercontent.com/explosion/spacy-models/master/compatibility.json"
response = session.get(url)
if response.status_code == 200:
    with open("compatibility.json", "wb") as f:
        f.write(response.content)
else:
    print(f"Failed to download file: {response.status_code}")

# Now you can proceed with loading the spacy model
spacy.cli.download("en_core_web_sm")