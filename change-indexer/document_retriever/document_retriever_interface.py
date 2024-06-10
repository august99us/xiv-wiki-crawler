from abc import ABCMetaclass

class DocumentRetrieverInterface(metaclass=ABCMetaclass):
	"""
	"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'retrieve_document') and 
                callable(subclass.retrieve_document))

    def retrieve_document(self, link) -> str:
        return NotImplemented
