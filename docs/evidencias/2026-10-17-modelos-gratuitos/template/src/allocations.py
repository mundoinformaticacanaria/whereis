def split_cents(total, count):
    """Split an amount into count shares."""
    if total < 0 or count <= 0:
        raise ValueError("invalid allocation")
    return [total // count] * count
