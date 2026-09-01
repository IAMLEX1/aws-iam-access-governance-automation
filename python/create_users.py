import boto3

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

users_to_create = [
    {
        "UserName": "skylar",
        "DisplayName": "Skylar",
        "Name": {
            "GivenName": "Skylar",
            "FamilyName": "Test"
        }
    },
    {
        "UserName": "zayn",
        "DisplayName": "Zayn",
        "Name": {
            "GivenName": "Zayn",
            "FamilyName": "Test"
        }
    }
]

for user in users_to_create:
    response = identitystore.create_user(
        IdentityStoreId=identity_store_id,
        UserName=user["UserName"],
        DisplayName=user["DisplayName"],
        Name=user["Name"]
    )

    print(
        "Created user:",
        user["UserName"],
        "- UserId:",
        response["UserId"]
    )