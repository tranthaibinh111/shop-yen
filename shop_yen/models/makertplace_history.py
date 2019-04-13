from django.db import models
from .marketplace import Marketplace


class MarketplaceHistory(Marketplace):
    done_at = models.DateTimeField(auto_now_add=True)
