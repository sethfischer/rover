"""Test console utilities."""

from osr_mechanical.console.utilities import snake_to_camel_case


class TestSnakeToCamelCase:
    """Test snake to camel case utility."""

    def test_lower_snake_case(self) -> None:
        """Test valid snake case."""
        result = snake_to_camel_case("valid_snake_case")

        assert "ValidSnakeCase" == result
