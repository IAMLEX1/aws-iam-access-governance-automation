import boto3

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

response = identitystore.list_users(
    IdentityStoreId=identity_store_id
)

for user in response["Users"]:
    print(
        user.get("UserName"),
        "-",
        user.get("DisplayName"),
        "-",
        user.get("UserId")
    )