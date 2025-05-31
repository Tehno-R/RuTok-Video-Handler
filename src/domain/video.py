from probe import ProbeInfo

class Video:
    def __init__(self, full_filename: str, uniq_id: str):
        name_and_extension = full_filename.split(".")
        self._name = name_and_extension[0]
        self._container = name_and_extension[1]
        self._uid = uniq_id
        self._probe = None

    def set_probe(self, probe: dict):
        self._probe = ProbeInfo(probe=probe)

    def get_probe(self) -> ProbeInfo:
        return self._probe

    def get_uid_name(self):
        return self._uid

    def get_origin_name(self):
        return f"{self._name}.{self._container}"

    def get_origin_name_for_preview(self):
        return f"{self._name}.jpeg"
