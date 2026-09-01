import boto3

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

GROUP_NAME = "Cloud-ReadOnly-Users"

groups_response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

group_id = None

for group in groups_response["Groups"]:
    if group["DisplayName"] == GROUP_NAME:
        group_id = group["GroupId"]
        break

memberships = identitystore.list_group_memberships(
    IdentityStoreId=identity_store_id,
    GroupId=group_id
)
member_count = len(memberships["GroupMemberships"])

print("Group:", GROUP_NAME)
print("Current Members:", member_count)

if member_count == 0:
    print("Status: No users currently assigned")
else:
    print("Status: Users are currently assigned")