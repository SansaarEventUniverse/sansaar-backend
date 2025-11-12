import uuid
from typing import Dict, List, Optional
from django.core.exceptions import ValidationError

from domain.template import EventTemplate
from domain.event import Event


class CreateTemplateService:
    """Service for creating event templates."""
    
    def create_from_event(self, event_id: uuid.UUID, name: str, 
                         description: str, created_by: uuid.UUID) -> EventTemplate:
        """Create template from existing event."""
        try:
            event = Event.objects.get(id=event_id, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValidationError("Event not found")
        
        template_data = {
            'title': event.title,
            'description': event.description,
            'visibility': event.visibility,
            'is_all_day': event.is_all_day,
        }
        
        template = EventTemplate.objects.create(
            name=name,
            description=description,
            category='other',
            template_data=template_data,
            created_by=created_by,
        )
        
        template.validate_template_data()
        return template
    
    def create_custom(self, data: Dict) -> EventTemplate:
        """Create custom template."""
        template = EventTemplate.objects.create(**data)
        template.validate_template_data()
        return template


class ApplyTemplateService:
    """Service for applying templates to events."""
    
    def apply_to_event(self, template_id: uuid.UUID, event_data: Dict, 
                      user_id: uuid.UUID) -> Dict:
        """Apply template to event data."""
        try:
            template = EventTemplate.objects.get(id=template_id)
        except EventTemplate.DoesNotExist:
            raise ValidationError("Template not found")
        
        if not template.can_access(user_id, event_data.get('organization_id')):
            raise ValidationError("Access denied to template")
        
        # Merge template data with event data
        merged_data = template.template_data.copy()
        merged_data.update(event_data)
        
        template.increment_usage()
        
        return merged_data
    
    def preview_template(self, template_id: uuid.UUID, user_id: uuid.UUID) -> Dict:
        """Preview template data."""
        try:
            template = EventTemplate.objects.get(id=template_id)
        except EventTemplate.DoesNotExist:
            raise ValidationError("Template not found")
        
        if not template.can_access(user_id):
            raise ValidationError("Access denied to template")
        
        return template.template_data


class TemplateManagementService:
    """Service for managing templates."""
    
    def get_templates(self, user_id: uuid.UUID, org_id: Optional[uuid.UUID] = None,
                     category: Optional[str] = None) -> List[EventTemplate]:
        """Get accessible templates."""
        query = EventTemplate.objects.all()
        
        if category:
            query = query.filter(category=category)
        
        templates = []
        for template in query:
            if template.can_access(user_id, org_id):
                templates.append(template)
        
        return templates
    
    def get_featured_templates(self) -> List[EventTemplate]:
        """Get featured templates."""
        return list(EventTemplate.objects.filter(is_featured=True, visibility='public'))
    
    def update_template(self, template_id: uuid.UUID, data: Dict, 
                       user_id: uuid.UUID) -> EventTemplate:
        """Update template."""
        try:
            template = EventTemplate.objects.get(id=template_id)
        except EventTemplate.DoesNotExist:
            raise ValidationError("Template not found")
        
        if template.created_by != user_id:
            raise ValidationError("Only template creator can update")
        
        for key, value in data.items():
            setattr(template, key, value)
        
        template.save()
        return template
    
    def delete_template(self, template_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """Delete template."""
        try:
            template = EventTemplate.objects.get(id=template_id)
        except EventTemplate.DoesNotExist:
            raise ValidationError("Template not found")
        
        if template.created_by != user_id:
            raise ValidationError("Only template creator can delete")
        
        template.delete()
    
    def clone_template(self, template_id: uuid.UUID, user_id: uuid.UUID, 
                      new_name: str = None) -> EventTemplate:
        """Clone template for customization."""
        try:
            template = EventTemplate.objects.get(id=template_id)
        except EventTemplate.DoesNotExist:
            raise ValidationError("Template not found")
        
        if not template.can_access(user_id):
            raise ValidationError("Access denied to template")
        
        return template.clone_template(user_id, new_name)
