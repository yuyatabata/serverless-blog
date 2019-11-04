from datetime import datetime #モデル作成時点の時刻をセット
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,NumberAttribute,UTCDateTimeAttribute
from flask_blog.lib.utils import is_production
import os

#ORマッパーのモデル
class Entry(Model):
    class Meta:
        table_name = "serverless_blog_entries"#dynamoDBで動かすテーブル名
        region = "us-east-1"
        if is_production():
            aws_access_key_id = os.environ.get('SERVERLESS_AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.environ.get('SERVERLESS_AWS_SECRET_KEY')
        else:
            aws_access_key_id = "AWS_ACCESS_KEY_ID"
            aws_secret_access_key = "AWS_SECRET_ACCESS_KEY"
            host = "http://localhost:8000"
    id = NumberAttribute(hash_key=True, null=False)#hash_keyをもとにデータベースを検索。nullを許可しない設定。
    title = UnicodeAttribute(null=True)
    text = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=datetime.now)#datetime
