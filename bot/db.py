def add_waifu_to_user(user_id, username, waifu_data):
    waifu_col.update_one(
        {"user_id": user_id},
        {
            "$set": {"username": username},
            "$push": {"waifus": waifu_data}
        },
        upsert=True
    )