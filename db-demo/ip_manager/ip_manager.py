"""
IP Management for this project (avoid hardcoded ip in settings)
"""


class IPManager:
    """
    IPManager for ip management
    avoid hardcoded ip
    """

    def __init__(self):
        self.ip = {
            'ES_DEBUG': ['152', '136', '231', '113'],
            'MODEL': ['152', '136', '231', '113'],
        }
        self.port = {
            'ES_DEBUG': '32005',
            'MODEL': '31001',
        }

    def get_address(self, item):
        """

        Args:
            item: item name(str) for the ip

        Returns:
            the corresponding ip and port as a whole string
        """
        return '.'.join(self.ip[item]) + ':' + self.port[item]


ip_manager = IPManager()
