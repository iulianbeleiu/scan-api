from django.contrib.auth import get_user_model


def sample_user():
    """Create sample user"""
    return get_user_model().objects.create(
        email='test@test.com',
        password='test123'
    )
