import random
import pytest
from feast import FeatureStore


# Mock setup for FeatureStore
store = FeatureStore(repo_path="feature_repos/redis")


@pytest.fixture
def setup_feature_service(request):
    """Fixture to set up the feature service and entities."""
    num_features = request.param.get("num_features", 50)
    num_entities = request.param.get("num_entities", 10)

    # Create the feature service
    feature_service = store.get_feature_service(f"feature_service_{num_features // 50 - 1}")

    # Generate random entity rows
    entity_rows = [{"entity": random.randint(0, 10000)} for _ in range(num_entities)]

    return feature_service, entity_rows


@pytest.mark.parametrize(
    "setup_feature_service", [
        {"num_features": 50, "num_entities": 10},
        {"num_features": 100, "num_entities": 10},
        {"num_features": 150, "num_entities": 10},
        {"num_features": 250, "num_entities": 10},
    ], 
    indirect=True,
    ids=["50_features_10_entities", "100_features_10_entities", "150_features_10_entities", "250_features_10_entities"]
)
def test_num_features(benchmark, setup_feature_service):
    """Benchmark test for store.get_online_features."""
    feature_service, entity_rows = setup_feature_service

    # Benchmark the function
    result = benchmark(store.get_online_features, feature_service, entity_rows)

    # Validate the result (optional, add if needed)
    assert result is not None



@pytest.mark.parametrize(
    "setup_feature_service", [
        {"num_features": 50, "num_entities": 50},
        {"num_features": 50, "num_entities": 100},
        {"num_features": 50, "num_entities": 500},
        {"num_features": 50, "num_entities": 1000},
    ], 
    indirect=True,
    ids=["50_features_50_entities", "50_features_100_entities", "50_features_500_entities", "50_features_1000_entities"]
)
def test_num_entities(benchmark, setup_feature_service):
    """Benchmark test for store.get_online_features."""
    feature_service, entity_rows = setup_feature_service

    # Benchmark the function
    result = benchmark(store.get_online_features, feature_service, entity_rows)

    # Validate the result (optional, add if needed)
    assert result is not None
