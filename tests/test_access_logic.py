def test_user_already_member():
    current_members = ["skylar", "alex"]

    username = "skylar"

    already_member = username in current_members

    assert already_member is True

def test_user_not_already_member():
    current_members = ["skylar", "alex"]

    username = "zayn"

    already_member = username in current_members

    assert already_member is False

def test_access_change_needed():
    current_members = ["skylar", "alex"]
    username = "zayn"

    access_change_needed = username not in current_members

    assert access_change_needed is True