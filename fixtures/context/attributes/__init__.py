def init(ctx, prototype):
    """Initialize each prop so we don't get AttributeError when accessing these."""

    for attr in dir(prototype):
        try:
            if attr.startswith("__"):
                continue

            if not hasattr(ctx, attr):
                setattr(ctx, attr, None)
        except Exception:
            continue
