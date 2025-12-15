from django.contrib import admin
from .models import (
    UserProfile,
    SkinAnalysis,
    Product,
    Order,
    OrderItem,
    ForumPost,
    ForumComment,
    MpesaPayment
)

admin.site.register(UserProfile)
admin.site.register(SkinAnalysis)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ForumPost)
admin.site.register(ForumComment)
admin.site.register(MpesaPayment)