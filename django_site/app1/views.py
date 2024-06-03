import os
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from .models import Trade, Author, TradeImage
from .json_validators import ValidateTradeJson, ValidateEditTradeJson
from .serializers import TradeSerializer, TradeImageSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist

def read_json(text):
    try:
        return json.loads(text)
    except:
        return bad_request()

def bad_request():
    return JsonResponse({"message": "Bad request"}, status=400)

# /
def index(request):
    return 

# TRADE
def trades(request, id=None):
    if request.method == "GET":
        if id:  return get_trade(id)
        else:   return get_trades()
    
    if request.method == "POST":
        return create_trade(request)
    
    if request.method == "PUT":
        if id: return edit_trade(id, request)
    
    return bad_request()

# TRADE IMAGE
def trade_images(request, trade_id=None, image_id=None):
    if request.method == "POST":
        return create_image(request, trade_id)
    
    if request.method == "DELETE":
        return delete_image(request, trade_id, image_id)
    
    return bad_request()

# GET /trades/<int:id>
def get_trade(id):
    trade = Trade.objects.get(pk=id)
    response_data = TradeSerializer.FullSerialize(trade)
    return JsonResponse({"data": response_data}, status=200)

# GET /trades
def get_trades():
    trades = Trade.objects.filter(status=Trade.TradeStatus.OPEN)
    response_data = TradeSerializer.SimpleSerializeList(trades)
    return JsonResponse({"data": response_data}, status=200)

# PUT /trades/<int:id>
def edit_trade(id, request):
    json_data = read_json(request.body)

    trade = Trade.objects.get(pk=id)

    # Провести валидацию JSON
    validation_result = ValidateEditTradeJson(json_data)

    # Если все плохо - возвращаем ошибку + список полей в которых ошибки.
    if not validation_result.is_valid():
        return JsonResponse({"message": "Json Validation Error", "errors": validation_result.errors}, status=400)

    try:
        for request_field in json_data:
            setattr(trade, request_field, json_data[request_field])
    except Exception as ex:
        return JsonResponse({"message": "Model Validation Error", "errors": [str(ex)]}, status=400)

    # Валидация модели
    try:
        trade.full_clean()
    except ValidationError as ex:
        return JsonResponse({"message": "Model Validation Error", "errors": ex.message_dict}, status=400)
    
    trade.update_date = timezone.now()
    trade.save()

    response_data = TradeSerializer.FullSerialize(trade)
    return JsonResponse(response_data, status=200)

# POST /trades
def create_trade(request):
    # Попытаться прочитать JSON
    json_data = read_json(request.body)

    # Провести валидацию JSON
    validation_result = ValidateTradeJson(json_data)

    # Если все плохо - возвращаем ошибку + список полей в которых ошибки.
    if not validation_result.is_valid():
        return JsonResponse({"message": "Json Validation Error", "errors": validation_result.errors}, status=400)

    # Пытаемся найти автора
    try:
        author = Author.objects.get(pk=json_data['author_id'])
    except ObjectDoesNotExist as ex:
        return JsonResponse({"message": "Model Validation Error", "errors": {"author_id": ["Author does not exist"]}}, status=400)

    # Создаем объект
    new_trade = Trade(
        create_date=timezone.now(),
        update_date=timezone.now(),
        author=author,
        title=json_data['title'],
        text=json_data['text'],
        status=json_data['status']
    )

    # Валидация модели
    try:
        new_trade.full_clean()
    except ValidationError as ex:
        return JsonResponse({"message": "Model Validation Error", "errors": ex.message_dict}, status=400)

    # Сохраняем
    new_trade.save()

    response_data = TradeSerializer.FullSerialize(new_trade)
    return JsonResponse(response_data, status=200)

def validate_image(file):
    valid_extensions = ['.jpeg', '.jpg', '.png', '.gif']
    filename, extension = os.path.splitext(file.name)

    if extension not in valid_extensions:
        raise Exception("invalid file format: " + file.name)

# POST /trade/<trade_id>/images
def create_image(request, trade_id):
    # Валидация запроса: количество файлов, их расширения.
    files = []
    
    try:
        for filename in request.FILES:
            file = request.FILES[filename]
            validate_image(file)
            files.append(file)
        if len(files) == 0:
            raise Exception("no files upload")
    except Exception as ex:
        return JsonResponse({"message": "File Upload Error", "errors": [str(ex)]}, status=400)

    
    # Попытка создать объекты в базе и загрузить изображения
    trade = Trade.objects.get(pk=trade_id)
    author = trade.author
    saved = []

    for file in files:
        trade_image = TradeImage(
            create_date = timezone.now(),
            update_date = timezone.now(),
            author = author,
            trade = trade,
        )

        # нейминг лучше поменять
        trade_image.image.save(file.name, file)
        trade_image.save()

        saved.append(trade_image)

    return JsonResponse({"data": TradeImageSerializer.SerializeList(saved)}, status=200)

def delete_image(request, trade_id, image_id):
    trade = Trade.objects.get(pk=trade_id)
    trade_image = TradeImage.objects.get(pk=image_id)

    if not trade:
        return JsonResponse({"message": "Trade Does Not Exist"}, status=400)

    if not trade_image:
        return JsonResponse({"message": "Trade Image Does Not Exist"}, status=400)
    
    try:
        trade_image.delete()
    except:
        return JsonResponse({"message": "Unknown error"}, status=400)
    
    return JsonResponse({"message": "Image deleted"}, status=200)