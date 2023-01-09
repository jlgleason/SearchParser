from .general_parser import GeneralParser
from .ad_parser import AdParser
from .shopping_ads_parser import ShoppingAdsParser
from .unknown_parser import UnknownParser

CMPT_PARSERS = {
    "general": GeneralParser,
    "ad": AdParser,
    "shopping_ads": ShoppingAdsParser,
    "unknown": UnknownParser,
}