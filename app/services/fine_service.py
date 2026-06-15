from datetime import datetime


def calculate_fine(due_date):

    if not due_date:
        return 0

    now = datetime.utcnow()

    if now <= due_date:
        return 0

    overdue_days = (now - due_date).days

    return overdue_days * 5