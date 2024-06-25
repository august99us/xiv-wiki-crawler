from abc import ABCMetaclass

# I am not a fan of how these interfaces work... i guess the problem was there
# was really no explicit typing to begin with...
class ChangeIndexerInterface(metaclass=ABCMetaclass):
    """
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'index_change') and 
                callable(subclass.index_change))

    def index_change(self, change) -> None:
        return NotImplemented
