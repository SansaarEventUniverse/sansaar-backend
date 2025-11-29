import uuid
from decimal import Decimal
from typing import Dict, Any
from django.core.exceptions import ValidationError

from domain.group_booking import GroupBooking, BulkDiscount


class GroupBookingService:
    """Service for managing group bookings."""
    
    def create_booking(self, data: Dict[str, Any]) -> GroupBooking:
        """Create a new group booking."""
        booking = GroupBooking.objects.create(
            event_id=data['event_id'],
            organizer_id=data['organizer_id'],
            group_name=data['group_name'],
            min_participants=data['min_participants'],
            max_participants=data['max_participants']
        )
        return booking
    
    def join_booking(self, booking_id: uuid.UUID, user_id: uuid.UUID) -> Dict[str, Any]:
        """Join a group booking."""
        try:
            booking = GroupBooking.objects.get(id=booking_id)
        except GroupBooking.DoesNotExist:
            raise ValidationError("Group booking not found")
        
        booking.add_participant()
        
        return {
            'booking_id': str(booking.id),
            'current_participants': booking.current_participants,
            'status': booking.status
        }


class BulkDiscountService:
    """Service for managing bulk discounts."""
    
    def create_discount(self, data: Dict[str, Any]) -> BulkDiscount:
        """Create a bulk discount."""
        discount = BulkDiscount.objects.create(
            event_id=data['event_id'],
            min_quantity=data['min_quantity'],
            discount_type=data['discount_type'],
            discount_value=data['discount_value']
        )
        return discount
    
    def get_applicable_discount(self, event_id: uuid.UUID, quantity: int) -> BulkDiscount:
        """Get applicable discount for quantity."""
        try:
            return BulkDiscount.objects.filter(
                event_id=event_id,
                min_quantity__lte=quantity,
                is_active=True
            ).order_by('-min_quantity').first()
        except BulkDiscount.DoesNotExist:
            return None


class GroupPaymentService:
    """Service for processing group payments."""
    
    def calculate_group_total(self, booking_id: uuid.UUID, base_price: Decimal) -> Dict[str, Any]:
        """Calculate total for group booking with discounts."""
        try:
            booking = GroupBooking.objects.get(id=booking_id)
        except GroupBooking.DoesNotExist:
            raise ValidationError("Group booking not found")
        
        quantity = booking.current_participants
        total = base_price * quantity
        
        discount_service = BulkDiscountService()
        discount = discount_service.get_applicable_discount(booking.event_id, quantity)
        
        if discount:
            discounted_total = discount.apply_discount(quantity, total)
            discount_amount = total - discounted_total
        else:
            discounted_total = total
            discount_amount = Decimal('0.00')
        
        return {
            'booking_id': str(booking.id),
            'quantity': quantity,
            'base_total': str(total),
            'discount_amount': str(discount_amount),
            'final_total': str(discounted_total)
        }
