# coding:utf-8

from requests import Session
from logging import basicConfig, INFO
from requests.auth import HTTPDigestAuth

from json import dumps, loads


class ElasticSearchFields(Session):
    search_one_doc_api = "http://{}/{}/_search?size=1"
    fields_mapping_api = "http://{}/{}/_mapping/{}"

    def __init__(self, host, index_or_template="_all", username=None, password=None):
        super(ElasticSearchFields, self).__init__()
        self._fields = []
        self.type = self._doc = None
        self.headers.update({"Content-Type": "application/json"})
        self.host = host
        self.index = index_or_template
        if username or password:
            self.auth = (username, password)
        self.doc_uri = self.search_one_doc_api.format(self.host, self.index)

    @property
    def doc(self):
        if not self._doc:
            response = self.get(self.doc_uri)
            assert response.status_code == 200, "本次请求不成功!\t{}".format(self.doc_uri)
            hits = loads(response.content).get("hits", {}).get("hits", [])
            self._doc = hits[0] if hits else {}
        return self._doc

    @property
    def fields_mapping_uri(self):
        assert self.doc, "该索引下没有任何数据."
        self.type = self.doc["_type"]
        return self.fields_mapping_api.format(self.host, self.index, self.type)

    @property
    def fields_mapping(self):
        if not self._fields:
            response = loads(self.get(self.fields_mapping_uri).content)
            self._fields = response.values()[0]["mappings"][self.type]["properties"]
        return self._fields

    @staticmethod
    def field_format(self, ):
        pass


type_mapping = {
    "long": "number",
    "float": "number",
    "date": "date",
    "keyword": "string",
    "text": "string",

}


def convert(es_fields):
    result = {}
    for field, item in imp.fields_mapping.iteritems():
        last_type = item["type"]
        type = type_mapping.get(last_type, "string")
        unit = "index" if type == "number" else "dimension"
        result.setdefault(unit, []).append({
            "field": field,
            "type": type_mapping.get(type, type),
            "last_type": type,
            "label": field
        })
    return result


if __name__ == '__main__':
    basicConfig(level=INFO, format="[%(levelname)s - %(asctime)s]: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    with ElasticSearchFields("hi-prod-33:9200", "taobao_item_info_monthly_test_2017-02-01_50025004", "test",
                             "test123") as imp:
        print dumps(convert(imp.fields_mapping), indent=4)

        #
        # print dumps(
        #     [{"field": field, "type": type, "label": field} for
        #      field, type in imp.fields_mapping], indent=4)
