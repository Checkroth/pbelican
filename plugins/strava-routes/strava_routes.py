import dataclasses
import requests

from pelican import signals
from pelican.contents import Article
from pelican.readers import BaseReader

STRAVA_ACTIVITIES_ENDPOINT = ""

@dataclasses.dataclass
class StravaRouteData:
    t: str

    @classmethod
    def from_strava_data(cls, ,strava_data: dict):
        return StravaRouteData("TEST")

def addArticle(articleGenerator):
    pass


def fetch_from_strava() -> list[StravaRouteData]:
    # Fetch a
    auth_token = "TEST"
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    routes = []
    def _fetch_from_strava(page: int = 1):
        run_url = f"{STRAVA_ACTIVITIES_ENDPOINT}?page={page}"
        response = requests.get(run_url, headers=auth_headers)
        if response.status_code == 200:
            routes.append(StravaRouteData.from_strava_data(response.json()))
        return page + 1

    prev_len = -1  # Anything other than 0 to kick off the loop.
    page = 1
    while prev_len != len(routes):
        page = _fetch_from_strava(page)
    return routes



def generate_graphs():
    pass

def register():
    signals.article_generator_pretaxonomy.connect(addArticle())