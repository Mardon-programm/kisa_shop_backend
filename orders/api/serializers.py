from rest_framework import serializers
from orders.models import Order, OrderItem, OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_name', 'product_sku', 'color_name', 'size_name', 
                  'quantity', 'price_rub', 'price_kgs', 'total_rub', 'total_kgs')


class OrderListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'customer_name', 'customer_phone', 'status', 
                  'status_display', 'total', 'currency', 'items_count', 'created_at')
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user', 'status', 'status_display',
                  'customer_name', 'customer_phone', 'customer_email',
                  'delivery_address', 'delivery_method', 'delivery_cost',
                  'subtotal', 'total', 'currency',
                  'payment_method', 'payment_id', 'paid_at',
                  'manager_notes', 'customer_notes',
                  'items', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('customer_name', 'customer_phone', 'customer_email',
                  'delivery_address', 'delivery_method', 'delivery_cost',
                  'payment_method', 'currency', 'items', 'customer_notes')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        import uuid
        validated_data['order_number'] = f'KISA-{uuid.uuid4().hex[:8].upper()}'
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.subtotal = sum(item.total_rub for item in order.items.all())
        order.total = order.subtotal + order.delivery_cost
        order.save()
        return order