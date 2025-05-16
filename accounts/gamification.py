from .models import User

def award_points(user, points, reason):
    """Award points to user with a reason"""
    user.points += points
    user.save()
    # Could add to a PointsHistory model if you want to track
    return f"Earned {points} points for {reason}!"