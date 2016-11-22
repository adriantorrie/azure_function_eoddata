import os
payload_in = open(os.environ['input']).read()
payload_out = open(os.environ['output'], 'w')
username = os.environ['eoddata_username']
password = os.environ['eoddata_password']

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'env/Lib/site-packages')))

import time
import xml.etree.cElementTree as etree
import requests
import eoddata

try:
    # webservice call
    ws_call = 'Login'

    # vars to control making a login request through a session and place
    # a token in return_data
    url = '/'.join((eoddata.WS_URL, ws_call))
    kwargs = {
        'Username': username,
        'Password': password}
    session = requests.Session()

    # read the ingress queue message and write to stdout
    message = "Python script processed queue message '{0}'".format(payload_in)
    print(message)

    start = time.time()
    resp = session.get(url, params=kwargs)
    root = etree.fromstring(resp.content)
    resp_message = root.get('Message')

    if resp_message == 'Login Successful':
        logged_in = True
        token = root.get('Token')
        data_format_code = root.get('DataFormat')
        data_format_include_header = root.get('Header')
        data_format_include_suffix = root.get('Suffix')

        login_resp = '{}'.format(resp_message)
        format_resp = '{} (Format: {})'.format(
            login_resp,
            data_format_code)
        header_resp = '{} (Headers: {})'.format(
            format_resp,
            data_format_include_header)
        suffix_resp = '{} (Suffixes: {})'.format(
            header_resp,
            data_format_include_suffix)
        message = '{} (Login Time: {:.3f}s)'.format(
            suffix_resp,
            int(time.time() - start))

        # write to stdout the outcome of the successful login request
        print(message)

        # Output the response to the client
        payload_out.write(token)

except Exception as e:
    raise e
