from abc import ABCMetaclass

class ChangeIndexerInterface(metaclass=ABCMetaclass):
	"""
	"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'index_change') and 
                callable(subclass.index_change))

    def index_change(self, change) -> None:
        return NotImplemented
