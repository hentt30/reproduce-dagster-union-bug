#!/usr/bin/env python3
"""
Bug Reproduction: TypeError: 'str' object is not a mapping

This script reproduces a bug in Dagster's config handling when using Python's
built-in Union type with Pydantic's discriminator field.

The issue occurs in Dagster's _config/pythonic_config/config.py around line 224
when trying to handle discriminated unions.
"""

import typing as t
from typing_extensions import Literal

import dagster as dg
from pydantic import Field


class SimpleConfigA(dg.Config):
    """Simple config class A with discriminator."""
    cfg_type: Literal["type_a"] = "type_a"


class SimpleConfigB(dg.Config):
    """Simple config class B with discriminator."""
    cfg_type: Literal["type_b"] = "type_b"


class TestConfig(dg.Config):
    """Test config that demonstrates the bug."""
    union_field: t.Union[SimpleConfigA, SimpleConfigB] = Field(
        default=SimpleConfigA(),
        discriminator="cfg_type",
    )


def reproduce_bug():
    """Reproduces the bug: 'str' object is not a mapping when using discriminated unions with Python Union type."""
    print("Creating config with discriminated union...")
    config = TestConfig(union_field=SimpleConfigA())
    
    print("Serializing config...")
    config_dict = config.model_dump()
    print(f"Serialized config: {config_dict}")
    
    print("Attempting to deserialize config...")
    try:
        # This line fails with TypeError: 'str' object is not a mapping
        # The issue is in Dagster's config handling of discriminated unions with Python Union types
        TestConfig.model_validate(config_dict)
        print("SUCCESS: Config deserialized without error")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        print("\nThis reproduces the bug in Dagster's config handling.")
        print("The issue occurs when using Python's Union type with Pydantic's discriminator field.")


if __name__ == "__main__":
    reproduce_bug()
