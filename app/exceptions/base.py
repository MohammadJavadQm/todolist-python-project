"""
پایه‌ی خطاهای سفارشی اپلیکیشن
"""

class AppException(Exception):
    """کلاس پایه برای تمام خطاهای اختصاصی این اپلیکیشن."""
    pass


class ProjectNotFoundError(AppException):
    """
    خطایی که زمانی رخ می‌دهد که پروژه‌ای با شناسه مورد نظر پیدا نشود.
    """
    pass


class TaskNotFoundError(AppException):
    """
    خطایی که زمانی رخ می‌دهد که تسکی با شناسه مورد نظر پیدا نشود.
    """
    pass