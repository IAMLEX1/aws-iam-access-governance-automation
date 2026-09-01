import boto3
import csv

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")

instances = sso_admin.list_instances()
identity_store_id = instances["Instances"][0]["IdentityStoreId"]

groups_to_audit = [
    "Cloud-ReadOnly-Users",
    "Cloud-Admin-Users"
]

report_rows = []

users_response = identitystore.list_users(
    IdentityStoreId=identity_store_id
)

users_by_id = {}

for user in users_response["Users"]:
    users_by_id[user["UserId"]] = {
        "username": user.get("UserName", ""),
        "display_name": user.get("DisplayName", "")
    }

groups_response = identitystore.list_groups(
    IdentityStoreId=identity_store_id
)

for group_name in groups_to_audit:

    group_id = None

    for group in groups_response["Groups"]:
        if group["DisplayName"] == group_name:
            group_id = group["GroupId"]
            break

    if group_id is None:
        print(f"SKIPPED: Group not found: {group_name}")
        continue

    memberships = identitystore.list_group_memberships(
        IdentityStoreId=identity_store_id,
        GroupId=group_id
    )

    for membership in memberships["GroupMemberships"]:
        user_id = membership["MemberId"]["UserId"]

        user_info = users_by_id.get(
            user_id,
            {
                "username": "UNKNOWN",
                "display_name": "UNKNOWN"
            }
        )

        report_rows.append({
            "username": user_info["username"],
            "display_name": user_info["display_name"],
            "group": group_name
        })

with open("../reports/access_governance_report.csv", "w", newline="") as csvfile:

    fieldnames = [
        "username",
        "display_name",
        "group"
    ]

    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(report_rows)

print("Access governance report created")
print(f"Users reported: {len(report_rows)}")
print("File: ../reports/access_governance_report.csv")