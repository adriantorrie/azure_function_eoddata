import os

# read the queue message and write to stdout
input = open(os.environ['eoddata_control_payload']).read()
message = "Python script processed queue message '{0}'".format(input)
print(message)