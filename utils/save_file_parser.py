import json
from typing import BinaryIO


def parse_player_save_file(
    file: BinaryIO,
    filename: str,
) -> dict:
    _validate_extension(filename)

    data = _load_json(file)

    properties = data.get("Properties")

    if not isinstance(properties, list):
        raise ValueError(
            "Invalid save structure: Properties not found"
        )

    recipes = _get_unlocked_recipes(properties)
    inventory = _get_inventory(properties)
    
    return {
        "recipes": recipes,
        "inventory": inventory,
    }


def _load_json(file: BinaryIO) -> dict:
    try:
        data = json.loads(file)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON file") from e
    return data


def _validate_extension(filename: str) -> None:
    if not filename.endswith(".sav.json"):
        raise ValueError("Invalid file extension")


def _find_property_by_prefix(
    data: object,
    prefix: str,
) -> dict | None:

    if isinstance(data, dict):
        name = data.get("Name")

        if (
            isinstance(name, str)
            and name.startswith(prefix)
        ):
            return data

        for value in data.values():
            result = _find_property_by_prefix(
                value,
                prefix,
            )

            if result is not None:
                return result

    elif isinstance(data, list):
        for item in data:
            result = _find_property_by_prefix(
                item,
                prefix,
            )

            if result is not None:
                return result

    return None


def _get_unlocked_recipes(
    properties: list,
) -> list[str]:
    recipes_property = _find_property_by_prefix(
        properties,
        "RecipesUnlock_",
    )
    if recipes_property is None:
        raise ValueError(
            "RecipesUnlock property not found"
        )
    value = recipes_property.get("Value")
    recipes = value.get("Items")
    return recipes


def _get_inventory(properties: list) -> list[dict]:
    inventory_property = _find_property_by_prefix(
        properties,
        "Inventory_",
    )

    if inventory_property is None:
        raise ValueError("Inventory property not found")

    items = inventory_property["Value"]["Items"]

    inventory = []

    for item in items:
        item_properties = item["Value"]

        name = _get_item_name(item_properties)
        quantity = _get_item_quantity(item_properties)

        inventory.append({
            name: quantity
        })

    return inventory


def _get_item_name(
    item_properties: list,
) -> str:

    item_data_table = _find_property_by_prefix(
        item_properties,
        "ItemDataTable_",
    )

    if item_data_table is None:
        raise ValueError(
            "ItemDataTable property not found"
        )

    value = item_data_table.get("Value")

    if not isinstance(value, dict):
        raise ValueError(
            "Invalid ItemDataTable property"
        )

    values = value.get("Value")

    if not isinstance(values, list):
        raise ValueError(
            "Invalid ItemDataTable value"
        )

    row_name = next(
        (
            prop
            for prop in values
            if (
                isinstance(prop, dict)
                and prop.get("Name") == "RowName"
            )
        ),
        None,
    )

    if row_name is None:
        raise ValueError(
            "RowName property not found"
        )

    name = row_name.get("Value")

    if not isinstance(name, str):
        raise ValueError(
            "Invalid item name"
        )

    return name


def _get_item_quantity(
    item_properties: list,
) -> int:

    changeable_data = _find_property_by_prefix(
        item_properties,
        "ChangeableData_",
    )
    if changeable_data is None:
        raise ValueError(
            "ChangeableData property not found"
        )
    value = changeable_data.get("Value")
    values = value.get("Value")
    current_stack = _find_property_by_prefix(
        values,
        "CurrentStack_",
    )
    quantity = current_stack.get("Value")

    return quantity