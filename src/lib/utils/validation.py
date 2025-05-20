

def fail_fast_typecheck(
    data, 
    expected_type: type, 
    label: str = "element"
):
    """
    Fail-fast type validator for sequences and mappings.

    Args:
        data (Iterable): A sequence of elements or values to check.
        expected_type (type): The required type for all elements.
        label (str): Used in the error message to identify context.

    Raises:
        TypeError: If any element is not of the expected type.
    """
    invalid_items = [
        (i, item) for i, item in enumerate(data)
        if not isinstance(item, expected_type)
    ]

    if invalid_items:
        message = ", ".join(
            f"{label} at index {i}: {item!r} ({type(item).__name__})"
            for i, item in invalid_items
        )
        raise TypeError(f"Type validation failed:\n{message}")

