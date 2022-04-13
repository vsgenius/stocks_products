from rest_framework import serializers
from rest_framework.response import Response

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id','address','positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
                StockProduct(quantity=position['quantity'],
                             product_id=position['product'].id,
                             price=position['price'],stock_id=stock.id).save()
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        print(instance,positions)
        for position in positions:
                StockProduct.objects.filter(stock_id=instance.id,
                            product_id=position['product'].id).update(quantity=position['quantity'],
                             price=position['price'])
        return stock

