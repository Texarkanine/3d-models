"""Publish one model tag to Cults from publish.yaml and author.yaml."""
import json
import os
import re
from pathlib import PurePosixPath
from urllib.parse import quote

import yaml

ENDPOINT = "https://cults3d.com/graphql"
USER_AGENT = "Texarkanine GitHub CICD for Cults3D"
_PAGE = 50
_INTROSPECT = """
query Introspect {
  __schema {
    mutationType {
      fields {
        name
        args {
          name
          type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
        }
      }
    }
  }
}
"""
_LICENSES = """
query Licenses {
  licenses { code name(locale: %s) }
}
"""
_SEARCH = """
query Mine($limit: Int!, $offset: Int!) {
  myself {
    creationsBatch(limit: $limit, offset: $offset) {
      total
      results { id name(locale: %s) }
    }
  }
}
"""


def file_url(path, *, repository, tag, component, attributes):
    """Return the public GitHub URL Cults can fetch for one publish path.

    path is relative to the model directory. attributes is the text of
    .gitattributes. An extension marked filter=lfs uses the media host.
    Every other path uses the raw host.
    """
    if repository.count("/") != 1 or repository.startswith("/"):
        raise ValueError("repository must be owner/name")
    parts = (component, *PurePosixPath(path).parts)
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"refusing path {path}")
    suffix = "/".join(quote(part) for part in parts)
    host = (
        "https://media.githubusercontent.com/media"
        if _is_lfs(path, attributes)
        else "https://raw.githubusercontent.com"
    )
    return f"{host}/{repository}/{quote(tag, safe='')}/{suffix}"


def assemble_description(description, boilerplate, license_name, manufacturing, *, manufacturing_argument):
    """Return one Cults description.

    The model description comes first. The author boilerplate follows, with
    {license_name} replaced. Non-empty manufacturing is a Manufacturing
    section when manufacturing_argument is None, and is left out of the
    description when that argument is set. Empty manufacturing adds nothing.
    """
    parts = []
    if description and str(description).strip():
        parts.append(str(description).strip())
    parts.append(str(boilerplate).replace("{license_name}", license_name).strip())
    text = "" if manufacturing is None else str(manufacturing).strip()
    if text and not manufacturing_argument:
        parts.append("Manufacturing\n\n" + text)
    return "\n\n".join(parts)


def select_arguments(payload, arguments):
    """Keep the payload keys that arguments lists.

    arguments maps an argument name to {"non_null": bool, "graphql_type": str}.
    Keys the schema does not list are dropped.
    """
    return {key: value for key, value in payload.items() if key in arguments}


def ensure_made_with_ai(arguments):
    """Return the schema argument that carries the made-with-AI flag.

    Raise ValueError when arguments has no such argument, so the caller
    can refuse before it creates or updates a listing.
    """
    for name in arguments:
        if name.lower().replace("_", "") == "madewithai":
            return name
    raise ValueError("Cults schema has no made-with-AI argument")


def choose_action(local_id, matches):
    """Return ("create", None) or ("update", creation_id).

    matches is the list of remote creation ids whose name equals the listing.
    Raise ValueError when more than one id matches, or when local_id is set
    and disagrees with the single match.
    """
    local = (local_id or "").strip()
    if len(matches) > 1:
        raise ValueError(f"{len(matches)} Cults creations share this name")
    if len(matches) == 1:
        if local and local != matches[0]:
            raise ValueError("local cults_creation_id disagrees with the Cults creation of this name")
        return ("update", matches[0])
    if local:
        return ("update", local)
    return ("create", None)


def set_creation_id(document, creation_id):
    """Return document with cults_creation_id set.

    Every other line is unchanged. document is the publish.yaml text.
    """
    rendered = json.dumps(creation_id)
    found = False
    lines = []
    for line in document.splitlines(keepends=True):
        if line.startswith("cults_creation_id:"):
            newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
            lines.append(f"cults_creation_id: {rendered}{newline}")
            found = True
        else:
            lines.append(line)
    if not found:
        raise ValueError("cults_creation_id is missing")
    return "".join(lines)


_ASSET_REQUIREMENTS = {
    "createBlueprint": ("creationId", "fileUrl"),
    "createIllustration": ("creationId", "imageUrl"),
    "destroyBlueprint": ("id",),
    "destroyIllustration": ("id",),
}
_ASSET_SELECTION = {
    "createBlueprint": "blueprint { id } errors",
    "createIllustration": "illustration { id } errors",
    "destroyBlueprint": "errors",
    "destroyIllustration": "errors",
}
_KEPT_MUTATIONS = ("createCreation", "updateCreation", *_ASSET_REQUIREMENTS)
_ASSET_RETRY_WAITS = (10, 30, 60)
_ASSETS = """
query Assets($ids: [String!], $limit: Int!, $offset: Int!) {
  myself {
    creationsBatch(ids: $ids, limit: $limit, offset: $offset) {
      total
      results {
        id
        blueprints { id }
        illustrations { id }
      }
    }
  }
}
"""
_GALLERY = """
query Gallery($ids: [String!], $limit: Int!, $offset: Int!) {
  myself {
    creationsBatch(ids: $ids, limit: $limit, offset: $offset) {
      total
      results {
        id
        details
        blueprints { id fileName fileExtension imageUrl }
      }
    }
  }
}
"""
_PREVIEW_WAIT_SECONDS = 15
_PREVIEW_ATTEMPTS = 13


def require_asset_mutations(mutations):
    """Raise ValueError unless an update can add and remove files and photos.

    mutations maps a mutation name to argument specs. createBlueprint must
    accept creationId and fileUrl. createIllustration must accept creationId
    and imageUrl. destroyBlueprint and destroyIllustration must accept id.
    """
    for name, required in _ASSET_REQUIREMENTS.items():
        spec = mutations.get(name)
        if spec is None:
            raise ValueError(f"Cults schema is missing {name}")
        for argument in required:
            if argument not in spec:
                raise ValueError(f"Cults schema {name} has no {argument} argument")


def create_assets(*, transport, auth, mutations, creation_id, file_urls, image_urls, sleep):
    """Add file_urls as blueprints and image_urls as illustrations.

    creation_id is the existing Cults creation. Cults fetches each URL
    while it handles the call, and that fetch fails now and then on a good
    URL. A call that Cults fails is tried again after each wait in
    _ASSET_RETRY_WAITS; sleep(seconds) does the waiting. RuntimeError naming
    the mutation and the URL is raised when the last attempt fails. This
    does not remove existing assets.
    """
    for operation, key, urls in (
        ("createBlueprint", "fileUrl", file_urls),
        ("createIllustration", "imageUrl", image_urls),
    ):
        for url in urls:
            for wait in (*_ASSET_RETRY_WAITS, None):
                try:
                    _call_mutation(
                        transport, auth, mutations, operation,
                        {"creationId": creation_id, key: url},
                    )
                    break
                except RuntimeError as exc:
                    if wait is None:
                        raise RuntimeError(
                            f"Cults {operation} failed for {url} after "
                            f"{len(_ASSET_RETRY_WAITS) + 1} attempts: {exc}"
                        ) from exc
                    sleep(wait)


def destroy_assets(*, transport, auth, mutations, blueprint_ids, illustration_ids):
    """Remove blueprint and illustration ids captured before the creates.

    A non-empty errors list from Cults raises RuntimeError.
    """
    for asset_id in blueprint_ids:
        _call_mutation(transport, auth, mutations, "destroyBlueprint", {"id": asset_id})
    for asset_id in illustration_ids:
        _call_mutation(transport, auth, mutations, "destroyIllustration", {"id": asset_id})


def _call_mutation(transport, auth, mutations, operation, payload):
    arguments = mutations[operation]
    selected = {key: value for key, value in payload.items() if key in arguments}
    result = _graphql(
        transport,
        auth,
        _mutation(operation, arguments, selected, _ASSET_SELECTION[operation]),
        selected,
    )
    body = result[operation]
    if body.get("errors"):
        raise RuntimeError(f"Cults {operation} failed: {body['errors']}")
    return body


def _batch_ids_key(creation_id):
    """Return the creationsBatch ids value for a stored creation id.

    Cults matches the slug. A global id decodes to Creation/<slug>. Any other
    id is sent unchanged.
    """
    import base64

    try:
        decoded = base64.b64decode(creation_id, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return creation_id
    prefix = "Creation/"
    slug = decoded[len(prefix):]
    if decoded.startswith(prefix) and slug:
        return slug
    return creation_id


def _listing_assets(transport, auth, creation_id):
    """Return blueprint ids and illustration ids for one creation.

    The read is myself.creationsBatch filtered by the slug of that id. Raise
    ValueError when no row's id equals the stored creation id.
    """
    data = _graphql(
        transport,
        auth,
        _ASSETS,
        {"ids": [_batch_ids_key(creation_id)], "limit": 1, "offset": 0},
    )
    batch = data["myself"]["creationsBatch"] or {}
    for row in batch.get("results") or []:
        if row["id"] == creation_id:
            return (
                [item["id"] for item in row.get("blueprints") or []],
                [item["id"] for item in row.get("illustrations") or []],
            )
    raise ValueError("Cults has no creation with this id")


def _ready_stl(blueprint):
    """Return whether this blueprint is an STL whose preview image exists."""
    extension = (blueprint.get("fileExtension") or "").lower()
    name = (blueprint.get("fileName") or "").lower()
    if extension != "stl" and not name.endswith(".stl"):
        return False
    return bool(blueprint.get("imageUrl"))


def _gallery_state(transport, auth, creation_id):
    """Return details and blueprints for one creation.

    Raise ValueError when no row's id equals the stored creation id.
    """
    data = _graphql(
        transport,
        auth,
        _GALLERY,
        {"ids": [_batch_ids_key(creation_id)], "limit": 1, "offset": 0},
    )
    batch = data["myself"]["creationsBatch"] or {}
    for row in batch.get("results") or []:
        if row["id"] == creation_id:
            return row
    raise ValueError("Cults has no creation with this id")


def _bump_details(*, transport, auth, mutations, creation_id, license_code, details):
    """Send one updateCreation that changes details.

    downloadPrice and licenseCode go with it. A price without the license
    resets the license, and a missing price fails the update.
    """
    arguments = mutations["updateCreation"]
    payload = {
        "id": creation_id,
        "details": details,
        "downloadPrice": 0,
        "licenseCode": license_code,
    }
    selected = select_arguments(payload, arguments)
    missing = [name for name in payload if name not in selected]
    if missing:
        raise RuntimeError(f"gallery refresh dropped {', '.join(missing)}")
    result = _graphql(
        transport, auth, _mutation("updateCreation", arguments, selected), selected,
    )
    body = result["updateCreation"]
    if body.get("errors"):
        raise RuntimeError(f"Cults updateCreation failed: {body['errors']}")
    if not (body.get("creation") or {}).get("id"):
        raise RuntimeError("Cults updateCreation returned no creation id")


def _refresh_gallery(*, transport, auth, mutations, creation_id, license_code, stl_count, sleep):
    """Rebuild the public gallery from the assets left after the file swap.

    Cults rebuilds that gallery only when updatedAt changes. Adding and
    deleting assets does not change it, and neither does updateCreation
    with the same field values. details is set to a different value and
    then restored.

    An STL preview image appears after Cults has stored the file. The edit
    waits until every STL from the tag has one. A gallery built earlier
    stays without that preview.
    """
    ready = 0
    state = None
    for attempt in range(_PREVIEW_ATTEMPTS):
        state = _gallery_state(transport, auth, creation_id)
        ready = sum(
            1 for blueprint in state.get("blueprints") or [] if _ready_stl(blueprint)
        )
        if ready >= stl_count:
            break
        if attempt == _PREVIEW_ATTEMPTS - 1:
            state = None
            break
        sleep(_PREVIEW_WAIT_SECONDS)
    if state is None:
        raise RuntimeError(
            f"Cults had {ready} STL previews after the file swap; the tag has {stl_count}"
        )
    current = state.get("details") or ""
    sentinel = ".." if current == "." else "."
    for details in (sentinel, current):
        _bump_details(
            transport=transport,
            auth=auth,
            mutations=mutations,
            creation_id=creation_id,
            license_code=license_code,
            details=details,
        )


def _stl_count(file_urls):
    """Return how many file URLs are STLs."""
    return sum(1 for url in file_urls if url.lower().split("?", 1)[0].endswith(".stl"))


def publish(*, root, component, tag, repository, api_key, transport=None, sleep=None):
    """Create or update the Cults listing and return the creation id.

    transport(query, variables, auth) returns the decoded GraphQL JSON.
    auth is (cults_nick, api_key). Raise when Cults returns a non-empty
    errors list. The api_key is not written into the query. sleep(seconds)
    waits between attempts to add a file or photo; it defaults to
    time.sleep.

    Every listing is free: downloadPrice is 0. updateCreation fails the
    price check when downloadPrice is absent, and a price sent without
    licenseCode resets the license to the Cults default.

    On an update, the public gallery is rebuilt after the old assets are
    gone and each STL preview exists. Cults rebuilds that gallery only
    when a field changes, so details is edited and then restored.
    """
    from pathlib import Path

    root = Path(root)
    record = yaml.safe_load((root / component / "publish.yaml").read_text())
    author = yaml.safe_load((root / "author.yaml").read_text())
    attributes = (root / ".gitattributes").read_text()
    _require_text(record.get("license_code"), "license_code")
    _require_text(record.get("category_id"), "category_id")
    if not api_key:
        raise ValueError("CULTS3D_API_KEY is empty")
    if transport is None:
        transport = _http_transport
    if sleep is None:
        import time

        sleep = time.sleep
    auth = (author["cults_nick"], api_key)
    locale = author["locale"]
    if not re.fullmatch(r"[A-Z]{2}", str(locale)):
        raise ValueError(f"unsupported locale {locale}")

    mutations = _mutation_arguments(transport, auth)
    create_args = mutations["createCreation"]
    ensure_made_with_ai(create_args)
    license_name = _license_name(transport, auth, str(record["license_code"]).strip(), locale)
    matches = _matching_ids(transport, auth, str(record["name"]).strip(), locale)
    action, creation_id = choose_action(record.get("cults_creation_id"), matches)
    arguments = create_args if action == "create" else mutations["updateCreation"]
    ai_argument = ensure_made_with_ai(arguments)
    manufacturing_argument = _manufacturing_argument(arguments)
    flag = author["made_with_ai"]
    if not isinstance(flag, bool):
        raise ValueError("made_with_ai must be a boolean")
    manufacturing = record.get("manufacturing") or ""
    description = assemble_description(
        record.get("description") or "",
        author["boilerplate"]["description"],
        license_name,
        manufacturing,
        manufacturing_argument=manufacturing_argument,
    )
    file_urls = [
        file_url(path, repository=repository, tag=tag, component=component, attributes=attributes)
        for path in record.get("files") or []
    ]
    image_urls = [
        file_url(path, repository=repository, tag=tag, component=component, attributes=attributes)
        for path in _listing_photos(root / component)
    ]
    payload = {
        "name": str(record["name"]).strip(),
        "description": description,
        "locale": locale,
        "categoryId": str(record["category_id"]).strip(),
        "subCategoryIds": list(record.get("subcategory_ids") or []),
        "licenseCode": str(record["license_code"]).strip(),
        "downloadPrice": 0,
        ai_argument: flag,
    }
    if str(manufacturing).strip() and manufacturing_argument:
        payload[manufacturing_argument] = str(manufacturing).strip()
    tags = list(record.get("tags") or [])
    if tags:
        payload["tagNames"] = tags
    previous = ([], [])
    if action == "create":
        payload["fileUrls"] = file_urls
        payload["imageUrls"] = image_urls
    else:
        if not file_urls:
            raise ValueError("files is empty")
        if not image_urls:
            raise ValueError("img is empty")
        if "description" not in arguments:
            raise ValueError("updateCreation has no description argument")
        if "details" not in arguments:
            raise ValueError("updateCreation has no details argument")
        require_asset_mutations(mutations)
        if "id" not in arguments:
            raise ValueError("updateCreation has no id argument")
        previous = _listing_assets(transport, auth, creation_id)
    selected = select_arguments(payload, arguments)
    if action == "create" and ("fileUrls" not in selected or "imageUrls" not in selected):
        raise ValueError(f"{action} cannot carry fileUrls and imageUrls; refusing a partial publish")
    if ai_argument not in selected:
        raise ValueError("made-with-AI flag was dropped")
    if "licenseCode" not in selected:
        raise ValueError("licenseCode was dropped; a price without it resets the Cults license")
    operation = "createCreation" if action == "create" else "updateCreation"
    if action == "update":
        selected["id"] = creation_id
    result = _graphql(transport, auth, _mutation(operation, arguments, selected), selected)
    payload_result = result[operation]
    if payload_result.get("errors"):
        raise RuntimeError(f"Cults {operation} failed: {payload_result['errors']}")
    created = payload_result.get("creation") or {}
    if not created.get("id"):
        raise RuntimeError(f"Cults {operation} returned no creation id")
    if action == "update":
        create_assets(
            transport=transport,
            auth=auth,
            mutations=mutations,
            creation_id=creation_id,
            file_urls=file_urls,
            image_urls=image_urls,
            sleep=sleep,
        )
        destroy_assets(
            transport=transport,
            auth=auth,
            mutations=mutations,
            blueprint_ids=previous[0],
            illustration_ids=previous[1],
        )
        _refresh_gallery(
            transport=transport,
            auth=auth,
            mutations=mutations,
            creation_id=creation_id,
            license_code=str(record["license_code"]).strip(),
            stl_count=_stl_count(file_urls),
            sleep=sleep,
        )
    return created["id"]


def main(argv=None):
    """Publish from COMPONENT, TAG, GITHUB_REPOSITORY, and CULTS3D_API_KEY.

    --set-creation-id writes that id into the component's publish.yaml and
    does not call Cults.
    """
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Publish one model tag to Cults.")
    parser.add_argument("--set-creation-id", metavar="ID")
    args = parser.parse_args(argv)
    component = os.environ["COMPONENT"]
    record = Path(component) / "publish.yaml"
    if args.set_creation_id is not None:
        if not args.set_creation_id.strip():
            raise SystemExit("creation id is empty")
        record.write_text(set_creation_id(record.read_text(), args.set_creation_id))
        return 0
    print(publish(
        root=Path("."),
        component=component,
        tag=os.environ["TAG"],
        repository=os.environ["GITHUB_REPOSITORY"],
        api_key=os.environ["CULTS3D_API_KEY"],
    ))
    return 0


def _listing_photos(model_dir):
    """Return the files in img/, relative to the model directory.

    A photo is uploaded because it is in that folder. publish.yaml does not
    keep a second copy of the list.
    """
    img = model_dir / "img"
    if not img.is_dir():
        return []
    return sorted(
        path.relative_to(model_dir).as_posix()
        for path in img.iterdir()
        if path.is_file()
    )


def _is_lfs(path, attributes):
    name = PurePosixPath(path).name
    for raw in attributes.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        bits = line.split()
        if len(bits) < 2 or "filter=lfs" not in bits[1:]:
            continue
        pattern = bits[0]
        if pattern.startswith("*.") and name.endswith(pattern[1:]):
            return True
    return False


def _require_text(value, label):
    if value is None or not str(value).strip():
        raise ValueError(f"{label} is blank")


def _graphql(transport, auth, query, variables):
    if auth[1] in query or auth[1] in json.dumps(variables):
        raise RuntimeError("refusing to put the API key in the Cults request")
    body = transport(query, variables, auth)
    if not isinstance(body, dict):
        raise RuntimeError("Cults returned a response that is not an object")
    if body.get("errors"):
        raise RuntimeError(f"Cults request failed: {body['errors']}")
    data = body.get("data")
    if data is None:
        raise RuntimeError("Cults returned no data")
    return data


def _mutation_arguments(transport, auth):
    data = _graphql(transport, auth, _INTROSPECT, {})
    found = {}
    for field in data["__schema"]["mutationType"]["fields"]:
        if field["name"] in _KEPT_MUTATIONS:
            found[field["name"]] = {
                arg["name"]: _parse_type(arg["type"]) for arg in field["args"]
            }
    if "createCreation" not in found or "updateCreation" not in found:
        raise ValueError("Cults schema is missing createCreation or updateCreation")
    return found


def _parse_type(node):
    return {"non_null": node["kind"] == "NON_NULL", "graphql_type": _format_type(node)}


def _format_type(node):
    if node["kind"] == "NON_NULL":
        return _format_type(node["ofType"]) + "!"
    if node["kind"] == "LIST":
        return "[" + _format_type(node["ofType"]) + "]"
    return node["name"]


def _license_name(transport, auth, code, locale):
    data = _graphql(transport, auth, _LICENSES % locale, {})
    for item in data["licenses"]:
        if item["code"] == code:
            return item["name"]
    raise ValueError(f"Cults has no license {code}")


def _matching_ids(transport, auth, name, locale):
    found = []
    offset = 0
    total = None
    while total is None or offset < total:
        data = _graphql(
            transport,
            auth,
            _SEARCH % locale,
            {"limit": _PAGE, "offset": offset},
        )
        batch = data["myself"]["creationsBatch"]
        total = batch["total"]
        rows = batch["results"]
        if not rows:
            break
        found.extend(row["id"] for row in rows if row["name"] == name)
        offset += len(rows)
        if offset > 10000:
            raise RuntimeError("stopped scanning Cults creations past 10000")
    return found


def _manufacturing_argument(arguments):
    for name in arguments:
        if "manufactur" in name.lower():
            return name
    return None


def _mutation(operation, arguments, selected, selection="creation { id } errors"):
    definitions = ", ".join(
        f"${name}: {arguments[name]['graphql_type']}" for name in selected
    )
    assignments = ", ".join(f"{name}: ${name}" for name in selected)
    return (
        f"mutation Publish({definitions}) "
        f"{{ {operation}({assignments}) {{ {selection} }} }}"
    )


def _http_transport(query, variables, auth):
    import base64
    import urllib.error
    import urllib.request

    body = json.dumps({"query": query, "variables": variables}).encode()
    token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"Cults HTTP {exc.code}: {detail}") from None


if __name__ == "__main__":
    raise SystemExit(main())
