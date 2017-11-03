import json
import logging
import datetime
import subprocess
from tangerine import TangerineClient, DictionaryBasedSecretProvider
from tangerine.exceptions import UnsupportedAccountTypeForDownload


FROM = datetime.date(2017, 10, 13)
TO = datetime.date(2017, 11, 2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    output = subprocess.check_output(['gpg', '-d', 'tangerine.json.gpg'])
    secret_provider = DictionaryBasedSecretProvider(json.loads(output))
    client = TangerineClient(secret_provider)
    with client.login():
        accounts = client.list_accounts()
        for acct in accounts:
            try:
                acct_details = client.get_account(acct['number'])
            except UnsupportedAccountTypeForDownload as e:
                print(e)
            else:
                print(client.download_ofx(acct, FROM, TO))