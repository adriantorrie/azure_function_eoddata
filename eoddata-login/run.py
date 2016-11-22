import json
import os
import sys
import xml.etree.cElementTree as etree
import requests as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'lib')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'env/Lib/site-packages')))

# webservice url
ws = 'http://ws.eoddata.com/data.asmx'

# returning xml responses prefixed with this namespace
xmlns = 'http://ws.eoddata.com/Data'

# read the queue message and write to stdout
payload_in = open(os.environ['input']).read()
message = "Python script processed queue message '{0}'".format(payload_in)
print(message)

# making requests through a session
session = r.Session()
url = '/'.join((WS, 'Login'))
kwargs = {
    'Username': open(os.environ['eoddata_username']).read(),
    'Password': open(os.environ['eoddata_password']).read()}
return_data = None
start = time.time()

try:
    
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


        return_data = {"Token": token}
        print (message)

except Exception as e:
    raise e


# Output the response to the client
payload_out = open(os.environ['output'], 'w')
payload_out.write(return_data)