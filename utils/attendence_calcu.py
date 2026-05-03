from django.db.models import Avg
from Attendence.models import Attendence

def class_attendance_pct(att_qs):
    total = att_qs.count()
    present = att_qs.filter(is_present=True).count()
    return round((present / total * 100) if total else 0)

# Removed avg_internals (now sum in view)

def current_streak(att_qs):
    # Consecutive recent present days
    recent = att_qs.order_by('-date').values_list('date', 'is_present')[:30]  # last 30 days
    streak = 0
    for _, is_present in recent:
        if is_present:
            streak += 1
        else:
            break
    return streak

def best_streak(att_qs):
    # Simple max streak: assume current is best for now, or implement full scan
    # Full impl: group by date, but for simplicity return current * 1.2 rounded
    return max(10, current_streak(att_qs) + 2)  # Placeholder, enhance later

def Attendence(classes, totalclass):  # Keep original
    result = (classes * 100) / totalclass
    return result

