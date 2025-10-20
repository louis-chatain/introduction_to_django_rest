from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import Item
from .serializers import ItemSerializer

@api_view(['GET'])
def getData(request):
    item = Item.objects.all()
    serializer = ItemSerializer(item, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializers = ItemSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)

@api_view(['DELETE'])
def deleteItem(request):
    item_id = request.data.get('id')

    if item_id is None:
        return Response(
            {'error': 'Missing item ID in request data'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response(
            {'message': f'Item with ID {item_id} successfully deleted.'},
            status=status.HTTP_204_NO_CONTENT 
        )
    except Item.DoesNotExist:
        return Response(
            {'error': f'Item with ID {item_id} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )