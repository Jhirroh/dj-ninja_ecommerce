from ninja import Router

from .models import Order
from .schema import OrderOut

app = Router()


@app.get("/orders/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    return Order.objects.get(user=request.user, id=order_id)


@app.post("/payout/{order_id}", response=OrderOut)
def payout_order(request, order_id: int):
    order = Order.objects.get(user=request.user, id=order_id)
    order.is_paid = True
    order.date_paid = datetime.now()
    order.save()
    return order
