from sso_query.query import make_query

class TestQuery:
    def test_defaults(self):
        expected_query = "foo"

        query = make_query()

        assert expected_query == query

    def test_neos(self):
        expected_query = "foo"

        query = make_query(1.3)

        assert expected_query == query