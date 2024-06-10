from abc import ABCMetaclass

class RecentChangesLoggerInterface(metaclass=ABCMetaclass):
	"""
	A RecentChangesLogger is an agent that keeps track of recently seen AND processed changes to a knowledge base.

	It has functionality to look up and pick out changes that have not yet been seen from a list of
	changes, and functionality to commit changes to the log
	"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'lookup_new_changes') and 
                callable(subclass.lookup_new_changes) and 
                hasattr(subclass, 'record_processed_change') and 
                callable(subclass.record_processed_change))

    def lookup_new_changes(self, changes_list: list) -> list:
    	return NotImplemented

    def record_processed_change(self, change) -> None:
    	return NotImplemented