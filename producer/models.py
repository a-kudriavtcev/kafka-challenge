from pydantic import BaseModel, Field


class WikiUpdate(BaseModel):
    schema_name: str = Field(validation_alias="$schema")
    id: int
    type: str
    namespace: int
    title: str
    comment: str
    timestamp: int
    user: str
    bot: bool
    minor: bool
    patrolled: str
    server_url: str
    server_name: str
    server_script_path: str
    wiki: str
    parsedcomment: str
    meta_domain: str
    meta_uri: str
    meta_request_id: str
    meta_stream: str
    meta_topic: str
    meta_dt: str
    meta_partition: int
    meta_offset: int
    meta_id: str
    length_old: int
    length_new: int
    revision_old: int
    revision_new: int
