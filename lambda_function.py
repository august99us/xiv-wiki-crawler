import boto3
# I really dont like how these imports look, but i think now is not the time to work on it...
# i'll find something i like later
from Documents.wiki_document_retriever import WikiDocumentRetriever
from Diffs.dynamo_recent_changes_logger import DynamoRecentChangesLogger
from Changes.s3_change_indexer import S3WikiChangeIndexer
from wiki_changes_diff_calculator import WikiChangesDiffCalculator

# Replace the boto3 calls with instantiating these objects for local testing
from Facades.dynamo_facade import DynamoFacade
from Facades.s3_facade import S3Facade

def lambda_handler(event, context):
    # Instantiate objects

    s3_client = boto3.client('s3')
    bucket_name = "xiv-wiki-index"
    dynamo_client = boto3.resource('dynamodb')
    recent_changes_table_name = "FFXIVWikiRecentChangesLog"
    recent_changes_table = dynamo_client.Table(recent_changes_table_name)

    document_retriever = WikiDocumentRetriever()
    change_indexer = S3WikiChangeIndexer(s3_client, bucket_name, document_retriever)
    recent_changes_logger = DynamoRecentChangesLogger(recent_changes_table)
    wiki_changes_diff_calc = WikiChangesDiffCalculator(recent_changes_logger, change_indexer)

    wiki_changes_diff_calc.index_changes()
