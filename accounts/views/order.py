from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ..models.order import Order
from ..serializers.order import OrderSerializer
from ..models.order import Order, OrderSubscription
from ..models.master_distributor import MasterDistributor
from ..models.distributor import Distributor
from ..models.subscription import Subscription

@extend_schema(tags=['Order'])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='pending')
    def get_pending_orders(self, request):
        pending_orders = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='new')
    def place_order(self, request):
        data = request.data
        master_distributor_id = data.get('master_distributor_id')
        distributor_id = data.get('distributor_id')
        subscriptions = data.get('subscriptions', [])
        discount=data.get('discount', 0)
        total_price=data.get('total', 0)
        subtotal_price=data.get('subtotal', 0)
     
        order = Order.objects.create(
            master_distributor_id=MasterDistributor.objects.get(id=master_distributor_id) if master_distributor_id else None,
            distributor_id=Distributor.objects.get(id=distributor_id) if distributor_id else None,
            status='pending',
            discount=discount,
            total=total_price,
            subtotal=subtotal_price,
        )

        for sub in subscriptions:
            subscription_id = sub.get('subscription_id')
            quantity = sub.get('quantity', 1)
            OrderSubscription.objects.create(
                order=order,
                subscription=Subscription.objects.get(id=subscription_id),
                quantity=quantity
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)