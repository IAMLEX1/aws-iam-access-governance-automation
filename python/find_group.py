import boto3

GROUP_NAME = "Cloud-ReadOnly-Users"

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

for group in response["Groups"]:
    if group["DisplayName"] == GROUP_NAME:
        print("Found group:", group["DisplayName"])
        print("Group ID:", group["GroupId"])
        break
else:
    print("Group not found:", GROUP_NAME)