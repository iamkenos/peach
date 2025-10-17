from behave.model import Feature

from peach.fixtures.constants.tags import Tags

from .. import Hook


class BeforeFeature(Hook):
    def __init__(self, feature: Feature):
        super().__init__()
        self.feature = feature

    def __prefix_name_with_brand(self) -> None:
        """Prefixes the feature name with the resolved BRAND environment variable."""
        if Tags.NO_BRAND not in self.feature.tags and bool(self._ctx.env.brand):
            self.feature.name = f"[{self._ctx.env.brand}] {self.feature.name}"

    def run(self):
        self.__prefix_name_with_brand()
