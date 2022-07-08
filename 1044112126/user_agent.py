from .debug import DebugService


class UserAgentService:
    def __init__(self, debug_service: DebugService, anki_version: str):
        self._debug_service = debug_service
        self._anki_version = anki_version

    def user_agent(self) -> str:
        amboss = self._debug_service.get_for_machine().get("amboss", {})
        anki = self._debug_service.get_for_machine().get("anki", {})
        return (
            f"""AMBOSS Anki add-on (AMBOSS v{amboss.get("version")}; Anki v{self._anki_version}); """
            + "; ".join(
                f"{k}: {v}"
                for k, v in {
                    "Python": anki.get("python"),
                    "PyQt": anki.get("pyqt"),
                    "Platform": anki.get("platform"),
                    "AnkiBuild": anki.get("version"),
                    "Flavor": anki.get("flavor"),
                    "Language": amboss.get("language"),
                    "Stage": amboss.get("stage"),
                    "Channel": amboss.get("channel"),
                }.items()
            )
        )
