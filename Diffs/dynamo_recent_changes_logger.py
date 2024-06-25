from datetime import datetime, timedelta

class DynamoRecentChangesLogger:
    """
    An implementation of the recent changes logger interface that uses DynamoDB to store
    and lookup the recently seen changes. Uses a 10 day TTL to automatically clean up older
    changes that are likely less useful
    """
    time_to_live = timedelta(days = 10)

    def __init__(self, dynamo_table_instance):
        self.table = dynamo_table_instance

    def lookup_new_changes(self, changes_list: list) -> list:
        fresh_changes = []
        # TODO: it likely doesn't matter for the scale that i am working with,
        # but this part could be parallelized w/ retry and exponential backoff
        # for better efficiency.
        for change in changes_list:
            response = self.table.get_item(
                Key={
                    'date_time': change.date_time,
                    'article_name': change.article_name
                }
            )
            if 'Item' not in response:
                fresh_changes.append(change)
        return fresh_changes

    def record_processed_change(self, change) -> None:
        self.table.put_item(
            Item={
                'date_time': change.date_time,
                'article_name': change.article_name,
                'article_link': change.article_link,
                'expire_at': (datetime.now() + self.time_to_live).timestamp()
            },
        )
