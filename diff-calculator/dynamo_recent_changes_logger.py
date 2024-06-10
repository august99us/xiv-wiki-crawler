from datetime import datetime, timedelta

class DynamoRecentChangesLogger:
    time_to_live = timedelta(days = 10)

	"""
	An implementation of the recent changes logger interface that uses DynamoDB to store
	and lookup the recently seen changes. Uses a 10 day TTL to automatically clean up older
	changes that are likely less useful
	"""
	def __init__(self, dynamo_table_instance):
		self.table = dynamo_table_instance

	def lookup_new_changes(self, changes_list: list) -> list:
        fresh_changes = []
		for change in changes_list:
            response = self.table.get_item(
                Key={
                'date_time': change.date_time,
                'article_name': change.article_name
                }
            )
            if not response.has_key('Item'):
                fresh_changes.append(change)
        return fresh_changes

    def record_processed_change(self, change) -> None:
        table.put_item(
            Item={
                'date_time': change.date_time,
                'article_name': change.article_name,
                'article_link': change.article_link,
                'expire_at': (datetime.now() + time_to_live).timestamp()
            },
        )
