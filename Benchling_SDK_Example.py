import benchling_sdk

from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(url="https://hoang.benchling.com", auth_method=ApiKeyAuth("sk_VMLKo01dD4IHOkFnKRrurrK63zVnt"))

# example of entries
example_entry = benchling.entries.get_entry_by_id(entry_id = "etr_oBoL9u5Q")

# You can print some of the fields directly if you dont want the entire API return. Although it doesnt have the identifier
print(example_entry.api_url, example_entry.archive_record)