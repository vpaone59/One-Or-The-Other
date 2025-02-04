import base64
import json
import requests


def get_minecraft_player_info(player_uuid):
    """
    Returns the full player information for a given Minecraft player UUID
    """
    try:
        response = requests.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}",
            timeout=5,
        )
        response.raise_for_status()
        player_info = response.json()
        player_skin_encoded = player_info["properties"][0]["value"]
        # Decode the Base64 encoded player skin
        player_skin_decoded = base64.b64decode(player_skin_encoded).decode("utf-8")

        player_skin_properties = json.loads(player_skin_decoded)

        player_info["skin_properties"] = player_skin_properties

        return player_info
    except requests.RequestException:
        return {"error": "Failed to retrieve player information."}
