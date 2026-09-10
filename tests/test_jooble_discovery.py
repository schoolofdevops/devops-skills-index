import unittest
import json
from unittest.mock import patch

from pipeline.discover_jooble import collect_discovery_jobs, jooble_fetcher, normalize_job


class JoobleDiscoveryTests(unittest.TestCase):
    def test_api_request_uses_documented_search_fields(self):
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self):
                return b'{"totalCount": 0, "jobs": []}'

        def fake_urlopen(request, timeout):
            captured["payload"] = json.loads(request.data)
            captured["timeout"] = timeout
            return Response()

        with patch("pipeline.discover_jooble.urllib.request.urlopen", fake_urlopen):
            jooble_fetcher("authorized-key")({"keywords": "devops", "location": "India"}, 3)

        self.assertEqual(captured["payload"], {
            "keywords": "devops",
            "location": "India",
            "page": "3",
            "ResultOnPage": "100",
            "companysearch": "false",
        })
        self.assertEqual(captured["timeout"], 60)

    def test_normalizes_a_job_without_treating_snippet_as_full_description(self):
        raw = {
            "id": 4815,
            "title": "Senior Platform Engineer",
            "location": "Pune, Maharashtra",
            "company": "Example Systems",
            "snippet": "Operate Kubernetes and Terraform platforms.",
            "source": "Example Board",
            "link": "https://example.test/jobs/4815",
            "updated": "2026-09-09T10:00:00Z",
            "type": "Full-time",
            "salary": "",
        }

        self.assertEqual(
            normalize_job(raw, "platform engineer", "India"),
            {
                "discovery_id": "jooble:4815",
                "provider_job_id": "4815",
                "title": "Senior Platform Engineer",
                "company": "Example Systems",
                "location": "Pune, Maharashtra",
                "source_provider": "jooble",
                "source_board": "Example Board",
                "source_url": "https://example.test/jobs/4815",
                "source_updated_at": "2026-09-09T10:00:00Z",
                "employment_type": "Full-time",
                "salary_text": "",
                "description_snippet": "Operate Kubernetes and Terraform platforms.",
                "description_evidence_level": "snippet_only",
                "canonical_status": "unresolved",
                "canonical_url": "",
                "discovery_query": "platform engineer",
                "discovery_location": "India",
            },
        )

    def test_deduplicates_results_returned_by_multiple_queries(self):
        responses = {
            ("devops engineer", 1): {
                "totalCount": 1,
                "jobs": [{"id": 7, "title": "DevOps Engineer", "company": "Acme"}],
            },
            ("site reliability engineer", 1): {
                "totalCount": 1,
                "jobs": [{"id": 7, "title": "DevOps Engineer", "company": "Acme"}],
            },
        }

        def fetch_page(query, page):
            return responses[(query["keywords"], page)]

        jobs, coverage = collect_discovery_jobs(
            [
                {"keywords": "devops engineer", "location": "India"},
                {"keywords": "site reliability engineer", "location": "India"},
            ],
            fetch_page,
            max_pages=1,
        )

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["discovery_id"], "jooble:7")
        self.assertEqual(coverage["results_received"], 2)
        self.assertEqual(coverage["unique_jobs"], 1)
        self.assertEqual(coverage["duplicate_results"], 1)
        self.assertEqual(coverage["unique_companies"], 1)

    def test_stops_when_a_page_contains_no_jobs(self):
        requested_pages = []

        def fetch_page(query, page):
            requested_pages.append(page)
            return {"totalCount": 500, "jobs": []}

        jobs, coverage = collect_discovery_jobs(
            [{"keywords": "mlops", "location": "India"}],
            fetch_page,
            max_pages=10,
        )

        self.assertEqual(jobs, [])
        self.assertEqual(requested_pages, [1])
        self.assertEqual(coverage["pages_requested"], 1)

    def test_paginates_each_query_using_its_own_result_count(self):
        requested = []

        def fetch_page(query, page):
            requested.append((query["keywords"], page))
            job_id = f"{query['keywords']}:{page}"
            return {"totalCount": 2, "jobs": [{"id": job_id, "title": query["keywords"]}]}

        jobs, _ = collect_discovery_jobs(
            [
                {"keywords": "devops", "location": "India"},
                {"keywords": "mlops", "location": "India"},
            ],
            fetch_page,
            max_pages=2,
        )

        self.assertEqual(len(jobs), 4)
        self.assertEqual(requested, [("devops", 1), ("devops", 2), ("mlops", 1), ("mlops", 2)])


if __name__ == "__main__":
    unittest.main()
