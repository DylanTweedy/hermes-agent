import os
import unittest
from datetime import datetime
from unittest import mock

from hermes_cli.session_ids import new_cli_session_id


class SessionNamespaceTests(unittest.TestCase):
    def test_parallel_launcher_namespaces_produce_distinct_ids_and_rotation_stays_scoped(self):
        start = datetime(2026, 10, 3, 15, 20, 30)
        with mock.patch.dict(os.environ, {"HERMES_SESSION_NAMESPACE": "herdr:workspace:tab:pane-a"}):
            first = new_cli_session_id(start)
        with mock.patch.dict(os.environ, {"HERMES_SESSION_NAMESPACE": "herdr:workspace:tab:pane-b"}):
            second = new_cli_session_id(start)

        self.assertNotEqual(first, second)
        self.assertIn("herdr-workspace-tab-pane-a", first)
        self.assertIn("herdr-workspace-tab-pane-b", second)
        self.assertNotEqual(first.split("_")[2], second.split("_")[2])

    def test_without_namespace_preserves_existing_session_id_shape(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("HERMES_SESSION_NAMESPACE", None)
            session_id = new_cli_session_id(datetime(2026, 10, 3, 15, 20, 30))
        self.assertRegex(session_id, r"^20261003_152030_[0-9a-f]{6}$")


if __name__ == "__main__":
    unittest.main()
