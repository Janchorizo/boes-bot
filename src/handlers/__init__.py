from .day_handler import DayHandler
from .day_input_handler import DayInputHandler
from .search_handler import SearchHandler
from .suscription_handler import SuscriptionHandler
from .menu_handler import MenuHandler
from .help_handler import HelpHandler

handlers = [
    DayHandler(),
    DayInputHandler(),
    SearchHandler(),
    SuscriptionHandler(),
    MenuHandler(),
    HelpHandler(),
]