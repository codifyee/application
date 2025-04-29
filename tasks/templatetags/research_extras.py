from django import template

register = template.Library()

@register.filter
def count_completed_sections(section_data):
    """Count the number of completed sections in the research task."""
    if not section_data:
        return 0
    return sum(1 for section in section_data.values() if section.get('status') == 'completed') 