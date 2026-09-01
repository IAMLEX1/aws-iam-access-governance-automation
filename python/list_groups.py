import boto3

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()

identity_store_id = instances["Instances"][0]["IdentityStoreId"]

response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

for group in response["Groups"]:
    print(group["DisplayName"], "-", group["GroupId"])