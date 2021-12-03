from typing import Any
import logging
from typing import Any
from typing import Union

from ipfabric.intent_models import Group
from .intent_models import IntentCheck

logger = logging.getLogger()


class Intent:
    def __init__(self, client):
        self.client: Any = client
        self.intent_checks: list = self.get_intent_checks()
        self.groups: list = self.get_groups()

    def get_intent_checks(self):
        """
        Gets all intent checks and returns a list of them.  You can also:
            ipf.intent()  # Loads the intents to intent_checks
            print(len(ipf.intent.intent_checks))
        :return: list: List of intent checks
        """
        res = self.client.get('reports', params=dict(snapshot=self.client.snapshot_id))
        res.raise_for_status()
        return [IntentCheck(**check) for check in res.json()]

    def get_groups(self):
        res = self.client.get('reports/groups')
        res.raise_for_status()
        return [Group(**group) for group in res.json()]

    @property
    def custom(self):
        return [c for c in self.intent_checks if c.custom]

    @property
    def builtin(self):
        return [c for c in self.intent_checks if not c.custom]

    @property
    def intent_by_id(self):
        return {c.intent_id: c for c in self.intent_checks}

    @property
    def intent_by_name(self):
        return {c.name: c for c in self.intent_checks}

    @property
    def group_by_id(self):
        return {g.group_id: g for g in self.groups}

    @property
    def group_by_name(self):
        return {g.name: g for g in self.groups}

    def get_results(self, intent: IntentCheck, color: Union[str, int], snapshot_id: str = None):
        if isinstance(color, str):
            color = dict(green=0, blue=10, amber=20, red=30)[color]
        return self.client.fetch_all(intent.api_endpoint, snapshot_id=snapshot_id, reports=intent.web_endpoint,
                                     filters={intent.column: ['color', 'eq', color]})
