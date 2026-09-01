import boto3

USER_NAME = "zayn"
GROUP_NAME = "Cloud-ReadOnly-Users"

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

users_response = identitystore.list_users(
    IdentityStoreId=identity_store_id
)

user_id = None

for user in users_response["Users"]:
    if user["UserName"] == USER_NAME:
        user_id = user["UserId"]
        break

groups_response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

group_id = None

for group in groups_response["Groups"]:
    if group["DisplayName"] == GROUP_NAME:
        group_id = group["GroupId"]
        break 

if user_id is None:
    raise Exception(f"User not found: {USER_NAME}")

if group_id is None:
    raise Exception(f"Group not found: {GROUP_NAME}")

membership = identitystore.create_group_membership(
    IdentityStoreId=identity_store_id,
    GroupId=group_id,
    MemberId={
        "UserId": user_id
    }
)

print(f"Added {USER_NAME} to {GROUP_NAME}")