from django import template

register = template.Library()

@register.filter
def filter_by_status(queryset, status):
    """Filter questions by status"""
    return queryset.filter(status=status)

@register.filter
def unique_students(queryset):
    """Get unique students from questions"""
    student_ids = queryset.values_list('student', flat=True).distinct()
    return student_ids
