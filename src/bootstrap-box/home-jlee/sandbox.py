#!/usr/bin/python3
# encoding=utf-8
# =============================================================================
# Begin Imports
# -----------------------------------------------------------------------------
# builtin
try:
  import sys
except KeyboardInterrupt as e:
  print("KeyboardInterrupt: %s" % str(repr(e)))
  print("Script terminated by Control-C")
  print("bye!")
  exit(1)
# builtin
import os
import json
import re
import traceback
from pprint import pprint

# Internal
from csisutil import sessionfactory, postgreslog, noticeutilcntrl
from stopwatch import StopWatch


# Third-Party
import boto3

# -----------------------------------------------------------------------------
# End Imports
# =============================================================================
# =============================================================================
# Begin VARIABLE DEFINITIONS
# -----------------------------------------------------------------------------

account_number='084135731370'
region = 'us-east-1'

admin_email = 'Joshua.Lee1@verizon.com'

# regular expression for email address verification
email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'



__curdir__ = os.path.abspath(os.path.dirname(__file__))
__author__ = 'Josh Lee'
__created__ = '11:52 AM - 16 Feb, 2020'
__copyright__ = 'Verizon Wireless'
__version__ = '0.15'

# XXX::TODO::GET`ER DONE!
# __version__ = 0.1 --> creation
# __version__ = 0.2 --> it works
# __version__ = 0.3 --> clean it up
# __version__ = 0.4 --> document what has been cleaned up
# __version__ = 0.5 --> document everything else
# __version__ = 0.6 --> test everything we can, try to break it with bad input
# __version__ = 0.7 --> apply bug fixes
# __version__ = 0.8 --> document bug fixes, apply spell checking and cleanup to
#                        documentation.
# __version__ = 0.9 --> run importnanny, and ensure it is properly copyrighted!
# __version__ = 0.9? -> ready for release, just needs packaged up 
# this is where confusion sets in, I still need to finish / complete jhelp, and
# learn how to auto-build man-pages from the --help options
# __version__ = 1.0 --> release with setup.py / installation files.

# -----------------------------------------------------------------------------
# End VARIABLE DEFINITIONS
# =============================================================================
# =============================================================================
# Begin Class Helpers
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# End Class Helpers
# =============================================================================
# =============================================================================
# Begin HELPER Functions
# -----------------------------------------------------------------------------



def validate_email(addy, regex=email_regex):
  """
    obvious,...
  """
  if(re.search(regex, str(addy).strip())): return str(addy).strip()
  return None


#log_obj = dict(ownerEmail=None)

"""
global_table = client.describe_global_table()
pprint(global_table)

global_table_settings = client.describe_global_table_settings()
"""

#print( validate_email(log_obj.get('ownerEmail', None)) or admin_email)
#sys.exit()

_key_vsads = []
def tags_for_key(kms_client, key_id, table_name, marker=None):
  # I *DO NOT* like doing this like this, but you cannot pass an empty
  # string, NOR can you pass a None (NoneType) in, I've already tried it, and
  # it causes an error, you actually must call it one way, or another, which
  # makes it intrinsicly more difficult, but at least this is recursive,
  # without a for statement, or a while statement.
  """
  This function will return a list of all tags (dicts) that are named 'VSAD'
  regardless of case.  

  kms_client (instance) : an active boto3.client('kms') instnace
  key_id (string) : The ID of the KMS Key we are inspecting.
  table_name (string) : The name of the DynamoDB table we are inspecting.
  marker (string) : A pointer for the pagenator, for looping through pages of
    records.

  Returns: list of dicts
  """
  global _key_vsads
  if marker is None:
    try:
      key_tags_response = kms_client.list_resource_tags(KeyId=key_id)
      ktags = key_tags_response['Tags']
    except Exception as e:
      raise AwsCliError(e)
      return 1
    else:
      marker = key_tags_response.get('NextMarker', None)

      if not len(ktags):
        raise MissingVsadError("KMS Key, KeyId: %s is not tagged, " \
          "and therefore, we already know that the VSAD tag is missing." \
          "Deleteing DynamoDB table '%s'." % (key['KeyId'], table_name))
      else:
        pprint(ktags)
        return
        vsad_list = [tag for tag in ktags if tag['TagKey'].lower() == 'vsad' ]
        if vsad_list:
          _key_vsads.append(vsad_list)
  if marker:
    return tags_for_key(kms_client, key_id, table_name, marker)
  else:
    return _key_vsads

# -----------------------------------------------------------------------------
# End HELPER Functions
# =============================================================================
# =============================================================================
# Begin MAIN PROGRAM FUNCTIONS
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# End MAIN PROGRAM FUNCTIONS
# =============================================================================
# =============================================================================
# Begin MAIN 
# -----------------------------------------------------------------------------
table_name = 'test_users'

def main(account_number=account_number, region=region):
  global table_name
  t=StopWatch(True)

  session_factory = sessionfactory.api(
      'VZSecDynamoDBRemediation',  # Shows up in CloudTrail logs
      account_id=account_number,
      role_to_assume='Vz-Sec_R'
  )
  sts_session = session_factory.create_session(region=region)

  kms_client = sts_session.client('kms')
  
  key_tags_response = \
  kms_client.list_resource_tags(KeyId='db7f1efe-71f7-4d32-9386-44fcc13ec5e3')

  ktags = key_tags_response['Tags']
  pprint("Look here:")
  pprint(ktags)
  print('-'*80)
  sys.exit()


  #tags = tags_for_key(kms_client, "b9cd0855-ffc4-4563-994e-3ae18d11306c",
  tags = tags_for_key(kms_client, "db7f1efe-71f7-4d32-9386-44fcc13ec5e3",
    table_name)

  keys = kms_client.list_keys()
  pprint(keys)
  return 0
  aliases = kms_client.list_aliases()
  pprint(aliases)
  return 0

  missing_targets = [a for a in aliases['Aliases'] if 'TargetKeyId' not in
  a.keys()]

  it_is_in_one=False
  for m in missing_targets:
    for k in keys['Keys']:
      if k['KeyId'] in m['AliasArn']:
        it_is_in_one=True
    if not it_is_in_one:
      print("alias without key!")
      pprint(m)
    it_is_in_one=False

  return
  for key in keys['Keys']:
    if key['KeyId'] == '278d8932-ba1f-4b53-b099-59d3362ddbf2':
      print("it is in the keys list.")

  return
  pprint(aliases)
  pprint("Key count: %s, alias count: %s" % (len(keys['Keys']),
    len(aliases['Aliases'])))
  return 0
  pprint(aliases)
  return 0
  tags = tags_for_key(kms_client, 'eba9adc6-3db8-4b71-9dca-4c31a830684c')

  pprint(tags)
  sys.exit()
# -----------------------------------------------------------------------------
# End MAIN 
# =============================================================================
  

if __name__ == '__main__':
  """

  Main function included to create test data for non-lambda debugging.

  """
  try:
    sys.exit(main(account_number, region))
  except Exception as e:
    print("An error has occured.\n")
    print(repr(e))
    type_,value_,traceback_ = sys.exc_info()
    print("type: %s" % type_)
    print("type2: %s" %type(e))
    print("value: %s" % value_)
    for tb_line in traceback.format_tb(traceback_):
      print(tb_line)
    print(str(e))
    sys.exit(1)


