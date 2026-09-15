from utils.save_file_parser import parse_player_save_file


class ResourceService:
    def create_resource_plan(self, target_name: str, target_quantity: int, file_bytes, file_path: str):
        return parse_player_save_file(file_bytes, file_path)