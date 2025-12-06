class DataValidationError(Exception):
    """Raised when data validation fails"""
    pass


class DataProcessingError(Exception):
    """Raised when data processing fails"""
    pass


class MappingError(Exception):
    """Raised when test data mapping fails"""
    pass
