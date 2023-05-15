"""OSR Sphinx extension."""

import os
import shutil
from pathlib import Path
from typing import Any

import requests
import sphinx.application
from sphinx.config import Config

from osr_mechanical import __version__
from osr_sphinx.domain import OsrDomain


def open_graph_image_url(user: str, repo: str) -> str:
    """Get URL of GitHub Open Graph Image."""
    query = f"""{{
      repository(owner: "{user}", name: "{repo}") {{
        openGraphImageUrl
      }}
    }}"""

    headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}

    try:
        response = requests.post(
            url="https://api.github.com/graphql", json={"query": query}, headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)

    try:
        og_image_url = response.json()["data"]["repository"]["openGraphImageUrl"]
    except KeyError:
        raise Exception("Expected key data.repository.openGraphImageUrl")

    return str(og_image_url)


def get_image(url: str, save_as: Path) -> None:
    """Get image and save."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)

    with open(save_as, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)


def download_open_graph_image(app: sphinx.application.Sphinx, config: Config) -> bool:
    """Download Open Graph image."""
    save_as = Path(app.outdir) / config.ogp_image

    if not save_as.exists():
        image_url = open_graph_image_url("sethfischer", "rover")
        get_image(image_url, save_as)

        return True

    return False


def setup(app: sphinx.application.Sphinx) -> dict[str, Any]:
    """Set up."""
    app.add_domain(OsrDomain)

    app.connect("config-inited", download_open_graph_image)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
