import boto3
import csv

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

with open("../config/joiners.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        username = row["username"]
        group_name = row["group"]

        print(f"Processing {username} -> {group_name}")

        # Find user
        users_response = identitystore.list_users(
            IdentityStoreId=identity_store_id
        )

        user_id = None

        for user in users_response["Users"]:
            if user["UserName"] == username:
                user_id = user["UserId"]
                break

        if user_id is None:
            print(f"SKIPPED: User not found: {username}")
            continue

        # Find group
        groups_response = identitystore.list_groups(
            IdentityStoreId=identity_store_id
        )

        group_id = None

        for group in groups_response["Groups"]:
            if group["DisplayName"] == group_name:
                group_id = group["GroupId"]
                break

        if group_id is None:
            print(f"SKIPPED: Group not found: {group_name}")
            continue

        # Check whether user is already a member
        memberships = identitystore.list_group_memberships(
            IdentityStoreId=identity_store_id,
            GroupId=group_id
        )

        already_member = False

        for membership in memberships["GroupMemberships"]:
            if membership["MemberId"]["UserId"] == user_id:
                already_member = True
                break

        if already_member:
            print(f"NO CHANGE: {username} is already in {group_name}")
            continue

        # Add user to group
        identitystore.create_group_membership(
            IdentityStoreId=identity_store_id,
            GroupId=group_id,
            MemberId={
                "UserId": user_id
            }
        )

        # Verify membership
        verification = identitystore.list_group_memberships(
            IdentityStoreId=identity_store_id,
            GroupId=group_id
        )

        verified = False

        for membership in verification["GroupMemberships"]:
            if membership["MemberId"]["UserId"] == user_id:
                verified = True
                break

        if verified:
            print(f"SUCCESS: Added {username} to {group_name}")
        else:
            print(f"FAILED: Could not verify {username} in {group_name}")