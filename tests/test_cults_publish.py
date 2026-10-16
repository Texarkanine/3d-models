"""Publisher behavior: URLs, description, schema filtering, and Cults calls."""
import base64
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.cults_publish import (
    assemble_description,
    choose_action,
    ensure_made_with_ai,
    file_url,
    publish,
    select_arguments,
    set_creation_id,
)

REPO = "Texarkanine/3d-models"
TAG = "h7-bulb-storage-v1.0.0"
ATTRIBUTES = "*.png filter=lfs diff=lfs merge=lfs -text\n"
SECRET = "test-secret"


def _type(text):
    if text.endswith("!"):
        return {"kind": "NON_NULL", "name": None, "ofType": _type(text[:-1])}
    if text.startswith("["):
        return {"kind": "LIST", "name": None, "ofType": _type(text[1:-1])}
    return {"kind": "SCALAR", "name": text, "ofType": None}


def _args(spec):
    return [{"name": name, "type": _type(gql)} for name, gql in spec.items()]


CREATE_ARGS = {
    "name": "String!",
    "description": "String!",
    "imageUrls": "[String!]",
    "fileUrls": "[String!]",
    "locale": "LocaleEnum!",
    "categoryId": "String!",
    "subCategoryIds": "[String!]",
    "licenseCode": "String",
    "madeWithAi": "Boolean!",
    "downloadPrice": "Float",
    "tagNames": "[String!]",
}
UPDATE_ARGS = {
    "id": "ID!",
    "name": "String",
    "description": "String",
    "licenseCode": "String",
    "madeWithAi": "Boolean",
    "downloadPrice": "Float",
}
ASSET_ARGS = {
    "createBlueprint": {"creationId": "ID!", "fileUrl": "String!", "position": "Int"},
    "createIllustration": {"creationId": "ID!", "imageUrl": "String!", "position": "Int"},
    "destroyBlueprint": {"id": "ID!"},
    "destroyIllustration": {"id": "ID!"},
}


def _row(item):
    return {
        "id": item["id"],
        "name": item["name"],
        "blueprints": [{"id": asset_id} for asset_id in item["blueprints"]],
        "illustrations": [{"id": asset_id} for asset_id in item["illustrations"]],
    }


class FakeCults:
    """GraphQL stand-in. Honors search offset and limit.

    rows are creation records. matches is a shorthand: each id becomes a row
    named listing_name with no assets. An ids variable selects a row by the
    slug of a global id, and by the row id when that id is not a global id.
    Like Cults, updateCreation without downloadPrice fails the price check.
    """

    def __init__(self, *, matches=None, rows=None, creation_id="creation-1", errors=None,
                 create_args=None, update_args=None, asset_args=None, omit_mutations=(),
                 page_cap=None, listing_name="Example part", blueprint_errors=None):
        self.creation_id = creation_id
        self.errors = errors
        self.blueprint_errors = blueprint_errors
        self.create_args = CREATE_ARGS if create_args is None else create_args
        self.update_args = UPDATE_ARGS if update_args is None else update_args
        self.asset_args = ASSET_ARGS if asset_args is None else asset_args
        self.omit_mutations = set(omit_mutations)
        self.page_cap = page_cap
        if rows is None:
            self.rows = [
                {"id": item, "name": listing_name, "blueprints": [], "illustrations": []}
                for item in (matches or [])
            ]
        else:
            self.rows = rows
        self.calls = []

    def __call__(self, query, variables, auth):
        self.calls.append((query, variables, auth))
        if "__schema" in query:
            fields = [
                {"name": "createCreation", "args": _args(self.create_args)},
                {"name": "updateCreation", "args": _args(self.update_args)},
            ]
            for name, spec in self.asset_args.items():
                if name not in self.omit_mutations:
                    fields.append({"name": name, "args": _args(spec)})
            return {"data": {"__schema": {"mutationType": {"fields": fields}}}}
        if "licenses" in query:
            return {"data": {"licenses": [
                {"code": "gpl", "name": "GNU General Public License"},
            ]}}
        if "creationsBatch" in query:
            rows = self.rows
            if variables.get("ids") is not None:
                wanted = set(variables["ids"])
                rows = [row for row in self.rows if _batch_ids_key(row["id"]) in wanted]
                return {"data": {"myself": {"creationsBatch": {
                    "total": len(rows),
                    "results": [_row(row) for row in rows[:variables["limit"]]],
                }}}}
            offset = variables["offset"]
            size = variables["limit"]
            if self.page_cap is not None:
                size = min(size, self.page_cap)
            chunk = rows[offset:offset + size]
            return {"data": {"myself": {"creationsBatch": {
                "total": len(rows),
                "results": [_row(row) for row in chunk],
            }}}}
        if "createBlueprint(" in query:
            errors = self.blueprint_errors or []
            blueprint = None if errors else {"id": "bp-new"}
            return {"data": {"createBlueprint": {"blueprint": blueprint, "errors": errors}}}
        if "createIllustration(" in query:
            return {"data": {"createIllustration": {"illustration": {"id": "il-new"}, "errors": []}}}
        if "destroyBlueprint(" in query:
            return {"data": {"destroyBlueprint": {"errors": []}}}
        if "destroyIllustration(" in query:
            return {"data": {"destroyIllustration": {"errors": []}}}
        operation = "updateCreation" if "updateCreation(" in query else "createCreation"
        if self.errors:
            return {"data": {operation: {"creation": None, "errors": self.errors}}}
        if operation == "updateCreation" and "downloadPrice" not in variables:
            return {"data": {operation: {
                "creation": None,
                "errors": ["Price must be greater than or equal to 0.5"],
            }}}
        return {"data": {operation: {"creation": {"id": self.creation_id}, "errors": []}}}


def write_repo(root, *, license_code="gpl", category_id="cat", creation_id="",
               manufacturing="", made_with_ai=True, files=None, photos=True):
    (root / "author.yaml").write_text(
        "cults_nick: texarkanine\n"
        "locale: EN\n"
        f"made_with_ai: {'true' if made_with_ai else 'false'}\n"
        "boilerplate:\n"
        "  description: \"pursuant to the terms of the {license_name}.\"\n"
    )
    (root / ".gitattributes").write_text(ATTRIBUTES)
    model = root / "widget"
    model.mkdir()
    if photos:
        img = model / "img"
        img.mkdir()
        (img / "part.png").write_bytes(b"png")
    (model / "readme.png").write_bytes(b"png")
    id_line = "cults_creation_id:\n" if creation_id == "" else f"cults_creation_id: \"{creation_id}\"\n"
    if files is None:
        files = ["part.stl"]
    files_block = "files: []\n" if not files else "files:\n" + "".join(f"  - {path}\n" for path in files)
    (model / "publish.yaml").write_text(
        "name: Example part\n"
        "description: A spare part.\n"
        f"manufacturing: {manufacturing}\n"
        "tags: []\n"
        f"license_code: {license_code}\n"
        f"category_id: {category_id}\n"
        "subcategory_ids:\n"
        "  - sub\n"
        + files_block
        + "images:\n"
        "  - img/not-uploaded.png\n"
        + id_line
    )


def _publish(root, transport, **kwargs):
    return publish(
        root=root,
        component="widget",
        tag=TAG,
        repository=REPO,
        api_key=SECRET,
        transport=transport,
        **kwargs,
    )


_MUTATION_NAMES = (
    "createBlueprint",
    "destroyBlueprint",
    "createIllustration",
    "destroyIllustration",
    "createCreation",
    "updateCreation",
)


def _mutations(transport):
    return [
        query for query, _variables, _auth in transport.calls
        if any(f"{name}(" in query for name in _MUTATION_NAMES)
    ]


def _operation_names(transport):
    names = []
    for query, _variables, _auth in transport.calls:
        for name in _MUTATION_NAMES:
            if f"{name}(" in query:
                names.append(name)
                break
    return names


def _batch_ids_key(creation_id):
    """Return the creationsBatch ids value Cults matches for a row id.

    A global id decodes to Creation/<slug>, and Cults matches the slug.
    Any other id is matched as itself.
    """
    try:
        decoded = base64.b64decode(creation_id, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return creation_id
    prefix = "Creation/"
    slug = decoded[len(prefix):]
    if decoded.startswith(prefix) and slug:
        return slug
    return creation_id


def _owned_row(creation_id="local-1", *, name="Example part", blueprints=(), illustrations=()):
    return {
        "id": creation_id,
        "name": name,
        "blueprints": list(blueprints),
        "illustrations": list(illustrations),
    }


class FileUrlTests(unittest.TestCase):
    def test_stl_path_uses_raw_host(self):
        url = file_url(
            "h7_cover.stl",
            repository=REPO,
            tag=TAG,
            component="h7-bulb-storage",
            attributes=ATTRIBUTES,
        )
        self.assertEqual(
            url,
            "https://raw.githubusercontent.com/Texarkanine/3d-models/"
            "h7-bulb-storage-v1.0.0/h7-bulb-storage/h7_cover.stl",
        )

    def test_lfs_extension_uses_media_host(self):
        url = file_url(
            "img/h7-bulb-storage-clip-cura.png",
            repository=REPO,
            tag=TAG,
            component="h7-bulb-storage",
            attributes=ATTRIBUTES,
        )
        self.assertEqual(
            url,
            "https://media.githubusercontent.com/media/Texarkanine/3d-models/"
            "h7-bulb-storage-v1.0.0/h7-bulb-storage/img/h7-bulb-storage-clip-cura.png",
        )


class DescriptionTests(unittest.TestCase):
    def test_boilerplate_replaces_license_name(self):
        text = assemble_description(
            "A spare part.",
            "pursuant to the terms of the {license_name}.",
            "GNU General Public License",
            "",
            manufacturing_argument=None,
        )
        self.assertIn("A spare part.", text)
        self.assertIn("GNU General Public License", text)
        self.assertNotIn("{license_name}", text)

    def test_manufacturing_without_schema_field_is_in_the_description(self):
        text = assemble_description(
            "A spare part.",
            "Shared line.",
            "GPL",
            "Layer height 0.2",
            manufacturing_argument=None,
        )
        self.assertIn("Layer height 0.2", text)
        self.assertIn("Manufacturing", text)

    def test_manufacturing_with_schema_field_is_left_out_of_the_description(self):
        text = assemble_description(
            "A spare part.",
            "Shared line.",
            "GPL",
            "Layer height 0.2",
            manufacturing_argument="manufacturingNotes",
        )
        self.assertNotIn("Layer height 0.2", text)

    def test_empty_manufacturing_has_no_manufacturing_section(self):
        text = assemble_description(
            "A spare part.",
            "Shared line.",
            "GPL",
            "",
            manufacturing_argument=None,
        )
        self.assertNotIn("Manufacturing", text)


class ArgumentTests(unittest.TestCase):
    def test_unknown_payload_keys_are_dropped(self):
        got = select_arguments(
            {"name": "A", "nope": 1},
            {"name": {"non_null": True, "graphql_type": "String!"}},
        )
        self.assertEqual(got, {"name": "A"})

    def test_made_with_ai_argument_is_returned(self):
        self.assertEqual(ensure_made_with_ai({"madeWithAi": {}}), "madeWithAi")

    def test_missing_made_with_ai_argument_raises(self):
        with self.assertRaises(ValueError):
            ensure_made_with_ai({"name": {}})


class ChooseActionTests(unittest.TestCase):
    def test_no_local_id_and_no_match_creates(self):
        self.assertEqual(choose_action("", []), ("create", None))

    def test_local_id_updates_that_id(self):
        self.assertEqual(choose_action("local-1", []), ("update", "local-1"))

    def test_one_remote_match_updates_that_id(self):
        self.assertEqual(choose_action("", ["remote-9"]), ("update", "remote-9"))

    def test_two_remote_matches_refuse(self):
        with self.assertRaises(ValueError):
            choose_action("", ["remote-9", "remote-8"])

    def test_local_id_that_disagrees_with_the_single_match_refuses(self):
        with self.assertRaises(ValueError):
            choose_action("local-1", ["remote-9"])


class SetCreationIdTests(unittest.TestCase):
    def test_empty_id_is_set_and_other_lines_stay(self):
        document = "name: Example part\nlicense_code: gpl\ncults_creation_id:\n"
        got = set_creation_id(document, "creation-1")
        self.assertEqual(
            got,
            "name: Example part\nlicense_code: gpl\ncults_creation_id: \"creation-1\"\n",
        )


class PublishTests(unittest.TestCase):
    def test_publish_returns_the_creation_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root)
            transport = FakeCults()
            got = _publish(root, transport)
        self.assertEqual(got, "creation-1")
        query, variables, auth = next(
            call for call in transport.calls if "createCreation(" in call[0]
        )
        self.assertEqual(auth, ("texarkanine", SECRET))
        self.assertNotIn(SECRET, query)
        self.assertEqual(
            variables["fileUrls"],
            [f"https://raw.githubusercontent.com/{REPO}/{TAG}/widget/part.stl"],
        )
        self.assertEqual(
            variables["imageUrls"],
            [f"https://media.githubusercontent.com/media/{REPO}/{TAG}/widget/img/part.png"],
        )
        joined = " ".join(variables["imageUrls"])
        self.assertNotIn("readme.png", joined)
        self.assertNotIn("not-uploaded.png", joined)
        self.assertIs(variables["madeWithAi"], True)
        self.assertIn("GNU General Public License", variables["description"])
        self.assertEqual(variables["downloadPrice"], 0)
        self.assertEqual(variables["licenseCode"], "gpl")
        self.assertEqual(_operation_names(transport), ["createCreation"])

    def test_publish_raises_when_cults_returns_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root)
            transport = FakeCults(errors=["Cults refused the file"])
            with self.assertRaises(RuntimeError) as caught:
                _publish(root, transport)
        self.assertIn("Cults refused the file", str(caught.exception))

    def test_schema_without_made_with_ai_refuses_before_a_mutation(self):
        create_args = {key: value for key, value in CREATE_ARGS.items() if key != "madeWithAi"}
        update_args = {key: value for key, value in UPDATE_ARGS.items() if key != "madeWithAi"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root)
            transport = FakeCults(create_args=create_args, update_args=update_args)
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_made_with_ai_sends_the_author_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, made_with_ai=False)
            transport = FakeCults()
            _publish(root, transport)
        variables = next(call[1] for call in transport.calls if "createCreation(" in call[0])
        self.assertIs(variables["madeWithAi"], False)

    def test_blank_license_code_refuses_before_the_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, license_code="")
            def transport(*_args):
                raise AssertionError("transport was called")
            with self.assertRaises(ValueError):
                _publish(root, transport)

    def test_blank_category_id_refuses_before_the_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, category_id="")
            def transport(*_args):
                raise AssertionError("transport was called")
            with self.assertRaises(ValueError):
                _publish(root, transport)

    def test_local_id_updates_that_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()])
            got = _publish(root, transport)
        self.assertEqual(got, "creation-1")
        variables = next(call[1] for call in transport.calls if "updateCreation(" in call[0])
        self.assertEqual(variables["id"], "local-1")
        self.assertNotIn("fileUrls", variables)
        self.assertEqual(
            _operation_names(transport),
            ["updateCreation", "createBlueprint", "createIllustration"],
        )

    def test_one_remote_match_updates_that_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root)
            transport = FakeCults(matches=["remote-9"])
            _publish(root, transport)
        variables = next(call[1] for call in transport.calls if "updateCreation(" in call[0])
        self.assertEqual(variables["id"], "remote-9")

    def test_two_remote_matches_refuse_before_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root)
            transport = FakeCults(matches=["remote-9", "remote-8"], page_cap=1)
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_manufacturing_schema_field_is_sent_and_not_repeated(self):
        create_args = dict(CREATE_ARGS, manufacturingNotes="String")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, manufacturing="Layer height 0.2")
            transport = FakeCults(create_args=create_args)
            _publish(root, transport)
        variables = next(call[1] for call in transport.calls if "createCreation(" in call[0])
        self.assertEqual(variables["manufacturingNotes"], "Layer height 0.2")
        self.assertNotIn("Layer height 0.2", variables["description"])

    def test_update_without_file_arguments_sends_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()])
            got = _publish(root, transport)
        self.assertEqual(got, "creation-1")
        asset_read = next(call for call in transport.calls if call[1].get("ids") is not None)
        self.assertEqual(asset_read[1]["ids"], ["local-1"])
        blueprint = next(call for call in transport.calls if "createBlueprint(" in call[0])
        self.assertIn("fileUrl", blueprint[1])
        self.assertNotIn("position", blueprint[1])
        self.assertIn("blueprint { id } errors", blueprint[0])
        self.assertEqual(
            blueprint[1]["fileUrl"],
            f"https://raw.githubusercontent.com/{REPO}/{TAG}/widget/part.stl",
        )
        illustration = next(call for call in transport.calls if "createIllustration(" in call[0])
        self.assertIn("illustration { id } errors", illustration[0])
        self.assertEqual(
            illustration[1]["imageUrl"],
            f"https://media.githubusercontent.com/media/{REPO}/{TAG}/widget/img/part.png",
        )
        update = next(call for call in transport.calls if "updateCreation(" in call[0])
        self.assertNotIn("fileUrls", update[1])
        self.assertNotIn("imageUrls", update[1])
        self.assertIn("A spare part.", update[1]["description"])
        self.assertEqual(
            _operation_names(transport),
            ["updateCreation", "createBlueprint", "createIllustration"],
        )

    def test_free_update_sends_a_zero_price_with_the_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()])
            _publish(root, transport)
        variables = next(call[1] for call in transport.calls if "updateCreation(" in call[0])
        self.assertEqual(variables["downloadPrice"], 0)
        self.assertEqual(variables["licenseCode"], "gpl")

    def test_schema_without_license_code_refuses_before_a_mutation(self):
        """Cults resets the license to its default when a price arrives without one."""
        update_args = {key: value for key, value in UPDATE_ARGS.items() if key != "licenseCode"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()], update_args=update_args)
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_global_creation_id_is_looked_up_by_slug(self):
        slug = "h7-bulb-storage"
        global_id = base64.b64encode(f"Creation/{slug}".encode()).decode()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id=global_id)
            transport = FakeCults(rows=[_owned_row(global_id)])
            got = _publish(root, transport)
        self.assertEqual(got, "creation-1")
        asset_read = next(call for call in transport.calls if call[1].get("ids") is not None)
        self.assertEqual(asset_read[1]["ids"], [slug])
        update = next(call[1] for call in transport.calls if "updateCreation(" in call[0])
        self.assertEqual(update["id"], global_id)

    def test_update_omits_file_arguments_when_the_schema_lists_them(self):
        update_args = dict(UPDATE_ARGS, fileUrls="[String!]", imageUrls="[String!]")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()], update_args=update_args)
            _publish(root, transport)
        variables = next(call[1] for call in transport.calls if "updateCreation(" in call[0])
        self.assertNotIn("fileUrls", variables)
        self.assertNotIn("imageUrls", variables)

    def test_update_replaces_previous_assets(self):
        row = _owned_row(blueprints=["b1", "b2"], illustrations=["i1"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[row])
            _publish(root, transport)
        destroyed = [
            call[1]["id"] for call in transport.calls if "destroyBlueprint(" in call[0]
        ]
        destroyed += [
            call[1]["id"] for call in transport.calls if "destroyIllustration(" in call[0]
        ]
        self.assertEqual(destroyed, ["b1", "b2", "i1"])
        self.assertNotIn("bp-new", destroyed)
        self.assertNotIn("il-new", destroyed)
        self.assertEqual(
            _operation_names(transport),
            [
                "updateCreation",
                "createBlueprint",
                "createIllustration",
                "destroyBlueprint",
                "destroyBlueprint",
                "destroyIllustration",
            ],
        )

    def test_stored_id_with_no_name_match_still_replaces_assets(self):
        row = _owned_row(name="Old title", blueprints=["b1", "b2"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[row])
            _publish(root, transport)
        destroyed = [call[1]["id"] for call in transport.calls if "destroyBlueprint(" in call[0]]
        self.assertEqual(destroyed, ["b1", "b2"])

    def test_chosen_id_missing_from_the_scan_refuses_before_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults()
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_missing_create_blueprint_refuses_before_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()], omit_mutations=["createBlueprint"])
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_create_blueprint_without_file_url_refuses_before_a_mutation(self):
        asset_args = dict(ASSET_ARGS)
        asset_args["createBlueprint"] = {"creationId": "ID!", "position": "Int"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()], asset_args=asset_args)
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_empty_file_list_refuses_before_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1", files=[])
            transport = FakeCults(rows=[_owned_row()])
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_empty_photo_list_refuses_before_a_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1", photos=False)
            transport = FakeCults(rows=[_owned_row()])
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_update_without_description_refuses_before_a_mutation(self):
        update_args = {key: value for key, value in UPDATE_ARGS.items() if key != "description"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[_owned_row()], update_args=update_args)
            with self.assertRaises(ValueError):
                _publish(root, transport)
        self.assertEqual(_mutations(transport), [])

    def test_blueprint_errors_stop_before_destroy(self):
        row = _owned_row(blueprints=["b1"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[row], blueprint_errors=["Cults refused the file"])
            with self.assertRaises(RuntimeError):
                _publish(root, transport)
        self.assertNotIn("destroyBlueprint", _operation_names(transport))

    def test_update_errors_stop_before_destroy(self):
        row = _owned_row(blueprints=["b1"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_repo(root, creation_id="local-1")
            transport = FakeCults(rows=[row], errors=["Cults refused the text"])
            with self.assertRaises(RuntimeError):
                _publish(root, transport)
        self.assertNotIn("createBlueprint", _operation_names(transport))
        self.assertNotIn("createIllustration", _operation_names(transport))
        self.assertNotIn("destroyBlueprint", _operation_names(transport))
