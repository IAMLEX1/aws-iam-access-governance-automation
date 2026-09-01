import boto3

USER_NAME = "zayn"
GROUP_NAME = "Cloud-Admin-Users"

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

if user_id is None:
    raise Exception(f"User not found: {USER_NAME}")

groups_response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

group_id = None

for group in groups_response["Groups"]:
    if group["DisplayName"] == GROUP_NAME:
        group_id = group["GroupId"]
        break

if group_id is None:
    raise Exception(f"Group not found: {GROUP_NAME}")

memberships = identitystore.list_group_memberships(
    IdentityStoreId=identity_store_id,
    GroupId=group_id
)

membership_id = None

for membership in memberships["GroupMemberships"]:
    if membership["MemberId"]["UserId"] == user_id:
        membership_id = membership["MembershipId"]
        break

if membership_id is None:
    raise Exception(f"{USER_NAME} is not a member of {GROUP_NAME}")

identitystore.delete_group_membership(
    IdentityStoreId=identity_store_id,
    MembershipId=membership_id
)

print(f"Removed {USER_NAME} from {GROUP_NAME}")

verification = identitystore.list_group_memberships(
    IdentityStoreId=identity_store_id,
    GroupId=group_id
)

still_member = False

for membership in verification["GroupMemberships"]:
    if membership["MemberId"]["UserId"] == user_id:
        still_member = True
        break

if still_member:
    raise Exception(
        f"Offboarding failed: {USER_NAME} is still in {GROUP_NAME}"
    )

print(f"Offboarded {USER_NAME} from {GROUP_NAME}")
print("Verification: access removed successfully") 