import boto3

USER_NAME = "zayn"
OLD_GROUP = "Cloud-ReadOnly-Users"
NEW_GROUP = "Cloud-Admin-Users"

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

# Find the user
users_response = identitystore.list_users(
    IdentityStoreId=identity_store_id
)

user_id = None

for user in users_response["Users"]:
    if user["UserName"] == USER_NAME:
        user_id = user["UserId"]
        break


# Find both groups
groups_response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

old_group_id = None
new_group_id = None

for group in groups_response["Groups"]:
    if group["DisplayName"] == OLD_GROUP:
        old_group_id = group["GroupId"]

    if group["DisplayName"] == NEW_GROUP:
        new_group_id = group["GroupId"]

if user_id is None:
    raise Exception(f"User not found: {USER_NAME}")

if old_group_id is None:
    raise Exception(f"Old group not found: {OLD_GROUP}")

if new_group_id is None:
    raise Exception(f"New group not found: {NEW_GROUP}")  

memberships = identitystore.list_group_memberships(
    IdentityStoreId=identity_store_id,
    GroupId=old_group_id
)

membership_id = None

for membership in memberships["GroupMemberships"]:
    if membership["MemberId"]["UserId"] == user_id:
        membership_id = membership["MembershipId"]
        break  
if membership_id is None:
    raise Exception(f"{USER_NAME} is not a member of {OLD_GROUP}")

identitystore.delete_group_membership(
    IdentityStoreId=identity_store_id,
    MembershipId=membership_id
)
identitystore.create_group_membership(
    IdentityStoreId=identity_store_id,
    GroupId=new_group_id,
    MemberId={
        "UserId": user_id
    }
)

print(f"Moved {USER_NAME} from {OLD_GROUP} to {NEW_GROUP}")