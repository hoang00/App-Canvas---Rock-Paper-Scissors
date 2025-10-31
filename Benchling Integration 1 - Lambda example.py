import os
import json
import logging
import benchling_sdk

from benchling_sdk.benchling import Benchling

from benchling_sdk.auth.api_key_auth import ApiKeyAuth
# from benchling_sdk.benchling import assay_runs

# set up authmethod

benchling = Benchling(url="https://hoang.benchling.com", auth_method = ApiKeyAuth("sk_VMLKo01dD4IHOkFnKRrurrK63zVnt"))

# Extract relevant details from the event
assay_run_id = '988b6cb2-b452-465d-a6bc-bcd800e3891c'

# Initialize Benchling API client
api_key = os.getenv('sk_VMLKo01dD4IHOkFnKRrurrK63zVnt')
client = Benchling(url="https://hoang.benchling.com", auth_method = ApiKeyAuth('sk_VMLKo01dD4IHOkFnKRrurrK63zVnt'))
# Retrieve the Assay Run object
assay_run = client.assay_runs.get_by_id(assay_run_id)

field1_value = getattr(assay_run.fields.get('entity_1'), 'display_value', "")
field2_value = getattr(assay_run.fields.get('entity_2'), 'display_value', "")

# Concatenate the values
concatenated_value = f"{field1_value}{field2_value}"
print(concatenated_value)

# # Update the Assay Run's field3 with the concatenated value
# assay_run.fields['concatenated_result'] = concatenated_value

# # Save the updated Assay Run object
# client.assay_runs.update(assay_run_id, assay_run)
