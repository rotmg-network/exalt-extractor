def assert_path_exists(path: str) -> bool:
    if not exists(path):
        try:
            mkdir(path)
        except Exception as e:
            logger.error(f"Failed creating path '{path}': {e}")
            return False
    return True
