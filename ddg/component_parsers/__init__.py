from .general_parser import GeneralParser
from .ad_parser import AdParser
from .unknown_parser import UnknownParser

CMPT_PARSERS = {
    "general": GeneralParser,
    "ad": AdParser,
    "unknown": UnknownParser,
}