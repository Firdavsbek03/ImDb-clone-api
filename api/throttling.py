from rest_framework.throttling import UserRateThrottle


class ReviewListViewThrottle(UserRateThrottle):
    scope = 'review-list'


class ReviewCreateViewThrottle(UserRateThrottle):
    scope = 'review-create'
