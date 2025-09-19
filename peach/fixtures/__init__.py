from peach.plugins.context.types import Context


class Fixture(Context):
    def __init__(self):
        self._ctx: Context
        """
        The `behave` context extended with custom props and methods.
        
        This is dynamically bound on runtime as part of framework setup.
        
        See `extend` function on `plugins.context` module.
        """
