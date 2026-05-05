def class_attendance_pct(att_qs):
    total = att_qs.count()
    present = att_qs.filter(is_present=True).count()
    return round((present / total * 100) if total else 0)

def current_streak(att_qs):
    rows = att_qs.order_by('-date', '-id').values('date', 'is_present')

    streak = 0
    current_date = None
    date_has_present = False

    for row in rows:
        if current_date is None:
            current_date = row['date']

        if row['date'] != current_date:
            if not date_has_present:
                return streak
            streak += 1
            current_date = row['date']
            date_has_present = False

        date_has_present = date_has_present or row['is_present']

    if current_date is not None:
        if not date_has_present:
            return streak
        streak += 1

    return streak

def best_streak(att_qs):
    rows = att_qs.order_by('date', 'id').values('date', 'is_present')

    best = 0
    running = 0
    current_date = None
    date_has_present = False

    for row in rows:
        if current_date is None:
            current_date = row['date']

        if row['date'] != current_date:
            if date_has_present:
                running += 1
                best = max(best, running)
            else:
                running = 0
            current_date = row['date']
            date_has_present = False

        date_has_present = date_has_present or row['is_present']

    if current_date is not None:
        if date_has_present:
            running += 1
            best = max(best, running)
        else:
            running = 0

    return best

def Attendence(classes, totalclass):  # Keep original
    result = (classes * 100) / totalclass
    return result

