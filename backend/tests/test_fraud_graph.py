"""Unit tests for app.services.fraud_graph — mocked AsyncSession, no live Postgres needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import fraud_graph as svc


class FakeResult:
    """Mimics SQLAlchemy's Result: .mappings().first()/.all(), .scalar(), .all()."""

    def __init__(self, row=None, rows=None, scalar=None):
        self._row = row
        self._rows = rows if rows is not None else []
        self._scalar = scalar

    def mappings(self):
        return self

    def first(self):
        return self._row

    def all(self):
        return self._rows

    def scalar(self):
        return self._scalar


class FakeRow:
    """Mimics a plain (non-mapping) Row with attribute access, e.g. row.source_id."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# ---------------------------------------------------------------------------
# get_entity_neighbourhood
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_entity_neighbourhood_no_match():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])
    result = await svc.get_entity_neighbourhood(db, "phone_number", "+911234567890")
    assert result == {"nodes": [], "edges": []}
    db.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_entity_neighbourhood_with_nodes_and_edges():
    node_id = uuid4()
    neighbour_id = uuid4()
    nodes = [
        {"id": node_id, "entity_type": "phone_number", "entity_value": "+911234567890",
         "risk_score": 80, "display_label": "Caller", "properties": {}, "cluster_id": None, "depth": 0},
        {"id": neighbour_id, "entity_type": "upi_id", "entity_value": "scam@ybl",
         "risk_score": 90, "display_label": "UPI", "properties": {}, "cluster_id": None, "depth": 1},
    ]
    edges = [
        {"id": uuid4(), "source_id": node_id, "target_id": neighbour_id, "relationship": "linked_to",
         "weight": 1.0, "properties": {}, "first_seen": None, "last_seen": None,
         "source_label": "+911234567890", "target_label": "scam@ybl"},
    ]

    db = AsyncMock()
    db.execute.side_effect = [FakeResult(rows=nodes), FakeResult(rows=edges)]

    result = await svc.get_entity_neighbourhood(db, "phone_number", "+911234567890", depth=2)

    assert len(result["nodes"]) == 2
    assert len(result["edges"]) == 1
    # UUIDs must be JSON-serialised to plain strings
    assert isinstance(result["nodes"][0]["id"], str)
    assert result["nodes"][0]["id"] == str(node_id)


# ---------------------------------------------------------------------------
# get_money_flow
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_money_flow():
    entity_id = uuid4()
    rows = [
        {"id": uuid4(), "source_id": entity_id, "target_id": uuid4(), "amount": 50000.0,
         "first_seen": None, "from_entity": "acc1", "from_type": "bank_account",
         "to_entity": "acc2", "to_type": "bank_account", "direction": "outflow", "hop": 1},
    ]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=rows)

    result = await svc.get_money_flow(db, entity_id)

    assert len(result) == 1
    assert result[0]["amount"] == 50000.0
    assert isinstance(result[0]["source_id"], str)


# ---------------------------------------------------------------------------
# Union-Find
# ---------------------------------------------------------------------------

def test_union_find_basic_grouping():
    uf = svc._UnionFind()
    uf.union("a", "b")
    uf.union("b", "c")
    uf.union("x", "y")

    assert uf.find("a") == uf.find("b") == uf.find("c")
    assert uf.find("x") == uf.find("y")
    assert uf.find("a") != uf.find("x")


def test_union_find_singleton_not_unioned():
    uf = svc._UnionFind()
    uf.union("a", "b")
    assert uf.find("z") == "z"  # never unioned, is its own root
    assert "z" in uf.nodes()


# ---------------------------------------------------------------------------
# detect_communities
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_detect_communities_filters_small_clusters():
    a, b, c, x, y = "a", "b", "c", "x", "y"
    # a-b-c form a 3-node cluster (kept); x-y form a 2-node cluster (filtered out, min=3)
    edges = [FakeRow(source_id=a, target_id=b), FakeRow(source_id=b, target_id=c), FakeRow(source_id=x, target_id=y)]

    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=edges)

    communities = await svc.detect_communities(db, min_cluster_size=3)

    assert len(communities) == 1
    (members,) = communities.values()
    assert set(members) == {a, b, c}


@pytest.mark.asyncio
async def test_detect_communities_empty_graph():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])

    communities = await svc.detect_communities(db)
    assert communities == {}


# ---------------------------------------------------------------------------
# persist_communities
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_persist_communities_creates_new_cluster():
    new_cluster_id = uuid4()
    member_ids = ["a", "b", "c"]

    db = AsyncMock()
    db.execute.side_effect = [
        FakeResult(scalar=None),          # existing cluster lookup -> none
        FakeResult(scalar=5),             # edge_count
        FakeResult(scalar=new_cluster_id),  # INSERT ... RETURNING id
        FakeResult(),                     # UPDATE entities.cluster_id
    ]

    result = await svc.persist_communities(db, {"a": member_ids})

    assert result == [{"cluster_id": str(new_cluster_id), "node_count": 3, "edge_count": 5}]
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_persist_communities_reuses_existing_cluster():
    existing_cluster_id = uuid4()
    member_ids = ["a", "b", "c"]

    db = AsyncMock()
    db.execute.side_effect = [
        FakeResult(scalar=existing_cluster_id),  # existing cluster found
        FakeResult(scalar=5),                    # edge_count
        FakeResult(),                            # UPDATE clusters
        FakeResult(),                            # UPDATE entities.cluster_id
    ]

    result = await svc.persist_communities(db, {"a": member_ids})

    assert result == [{"cluster_id": str(existing_cluster_id), "node_count": 3, "edge_count": 5}]
    # Should NOT have issued an INSERT — only 4 execute calls total (no 5th insert call)
    assert db.execute.await_count == 4
