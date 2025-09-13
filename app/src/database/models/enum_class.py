from enum import Enum


class ApprovalStatus(Enum):
     PENDING = 'pending'
     APPROVED = 'approved'
     REJECTED = 'rejected'

class OrderStatus(Enum):
     PENDING = 'pending'
     PROCESSING = 'processing'
     SHIPPED = 'shipped'
     DELIVERED = 'delivered'
     CANCELLED = 'cancelled'
