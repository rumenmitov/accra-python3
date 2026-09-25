from accra_language import (
    AccraError,
    Config,
    Language,
    LanguageSpec,
)

from . import utils


class Python3(Language):
    def __init__(self):
        super().__init__(LanguageSpec("python3", "3"))

    def detect(self, config: Config | None = None) -> bool:
        cfg = config or self.config

        result: set[str] | AccraError = utils.get_supported_python_versions_from_code(
            cfg
        )
        match result:
            case set():
                return bool(result)

            case AccraError():
                return result
