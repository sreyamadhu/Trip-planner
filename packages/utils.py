def serialize_destination(destination):
    if destination is None:
        return None

    return destination.to_dict()