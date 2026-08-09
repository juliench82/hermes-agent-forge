class CompilerError(ValueError):
    """Base compiler error."""


class CatalogResolutionError(CompilerError):
    """Raised when a primitive cannot be resolved exactly."""
