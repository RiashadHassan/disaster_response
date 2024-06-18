def get_slug_full_name(instance):
    if instance.first_name:
        return f"{instance.first_name} {instance.last_name}".strip()
    else:
        first_part_email = instance.email.split("@")[0]
        return f"{first_part_email}".strip()


def get_event_id(
    created_at=None, event_type=None, severity_level=None, risk_level=None
):
    pass
