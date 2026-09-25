import subprocess

from accra_language import (
    AccraBuildError,
    AccraInstallError,
    AccraRunError,
    Config,
    Language,
    LanguageSpec,
)


class Python3(Language):
    def __init__(self):
        super().__init__(LanguageSpec("python3", "3"))

        self.minor_version: str = "0"

    def detect_language(self, config: Config | None = None) -> bool:
        cfg = config or self.spec.config

        result = subprocess.run(
            ["vermin", "-f", "parsable", cfg.cwd],
            check=False,
            capture_output=True,
            text=True,
            **cfg.dump_model(),
        )

        if result.returncode != 0:
            return False

        lines = result.stdout.splitlines()
        if not lines:
            return False

        summary = [x for x in lines[-1].strip().split(":") if x]
        py3_version = summary[-1].strip("~")

        if py3_version.startswith("!"):
            return False

        self.minor_version = py3_version.split(".")[1] or self.minor_version

        return True

    def install(self, config: Config | None = None) -> AccraInstallError | None:
        cfg = config or self.spec.config

        result = subprocess.run(
            ["pyenv", "install", self.version + "." + self.minor_version],
            check=False,
            capture_output=True,
            text=True,
            **cfg.dump_model(),
        )

        if result.returncode != 0:
            return AccraInstallError(
                message=f"could not install {self.name} {self.version}"
            )

        return None

    def build(self, config: Config | None = None) -> AccraBuildError | None:
        return self.env_manager.build(config)

    def run_program(
        self, program: str, args: [str], config: Config | None = None
    ) -> AccraRunError | None:
        return self.env_manager.run(program, args, config)
