from ninja_extra import (
    NinjaExtraAPI, Router, route, api_controller
)

from .models import Order
from .schema import OrderOut


@api_controller("/orders", tags=["Orders"])
class OrderController:
    @route.get("/{order_id}", response=OrderOut)
    def get_order(self, order_id: int):
        return Order.objects.get(user=self.request.user, id=order_id)

    @route.post("/payout/{order_id}", response=OrderOut)
    def payout_order(self, order_id: int):
        order = Order.objects.get(user=self.request.user, id=order_id)
        order.is_paid = True
        order.date_paid = datetime.now()
        order.save()
        return order


