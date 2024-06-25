class S3WikiChangeIndexer:
    """
    """

    def __init__(self, s3_instance, bucket_name, document_retriever):
        self.s3 = s3_instance
        self.bucket_name = bucket_name
        self.document_retriever = document_retriever

    def index_change(self, change) -> None:
        object = self.s3.Object(self.bucket_name, change.article_link)
        wiki_content = self.document_retriever.retrieve_document(change.article_link)
        object.put(Body = wiki_content)
