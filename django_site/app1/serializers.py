import os
from .models import Trade, TradeImage, Author
from typing import List

class TradeSerializer():
    def SimpleSerialize(trade: Trade) -> dict:
        return {
            "id": trade.pk,
            "title": trade.title,
            "create_date": trade.create_date.strftime("%d.%m.%Y %H:%M:%S")
        }
    
    def FullSerialize(trade: Trade) -> dict:
        return {
            "id": trade.pk,
            "title": trade.title,
            "text": trade.text,
            "status": trade.status,
            "author": AuthorSerializer.Serialize(trade.author),
            "create_date": trade.create_date.strftime("%d.%m.%Y %H:%M:%S"),
            "update_date": trade.update_date.strftime("%d.%m.%Y %H:%M:%S"),
            "images": TradeImageSerializer.SerializeList(trade.get_images())
        }
    
    def SimpleSerializeList(trades: List[Trade]) -> List[dict]:
        return [TradeSerializer.SimpleSerialize(trade) for trade in trades]

class AuthorSerializer():
    def Serialize(author: Author) -> dict:
        return {
            "id": author.id,
            "name": author.first_name + " " + author.last_name,
        }

class TradeImageSerializer():
    def Serialize(image: TradeImage) -> dict:
        return {
            "id": image.id,
            "name": os.path.basename(image.image.name),
            "url": image.image.url,
        }
    
    def SerializeList(images: List[TradeImage]) -> List[dict]:
        return [TradeImageSerializer.Serialize(image) for image in images]