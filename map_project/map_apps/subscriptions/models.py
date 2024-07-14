from django.db import models

from ..users.models import User

# Create your models here.


# class SubscriptionsTypes(models.Model):
#     ACCESS_LEVEL = (
#         ('0', '0'),
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#     )
#
#     AMOUNT_EVENTS = (
#         ('2', '2'),
#         ('5', '5'),
#         ('10', '10'),
#         ('20', '20'),
#     )
#
#     name = models.CharField(max_length=128)
#     subs_level = models.CharField(choices=ACCESS_LEVEL, max_length=4)
#     amount_events = models.CharField(choices=AMOUNT_EVENTS, max_length=4)
#     access_to_subscribe_to_users = models.BooleanField(default=False)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     #stripe_price
#
#
# class DiscountTypes(models.Model):
#     name = models.CharField(max_length=128)
#     percent = models.DecimalField(max_digits=6, decimal_places=2)
#
#
# class SubscriptionsHistory(models.Model):
#     DECLINE_REASON = (
#         ('date', 'out of date'),
#     )
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptionshistory')
#     subscription = models.ForeignKey(SubscriptionsTypes, on_delete=models.CASCADE)
#     discount = models.ForeignKey(DiscountTypes, models.PROTECT, null=True, blank=True)
#     final_price = models.DecimalField(max_digits=8, decimal_places=2)
#     start_date = models.DateField(auto_now_add=True)
#     end_date = models.DateField()
#     decline_reason = models.CharField(choices=DECLINE_REASON, max_length=128, default='date')
