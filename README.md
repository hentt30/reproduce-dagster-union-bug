# Dagster Bug Reproduction: TypeError with Discriminated Unions

## Issue Description

This repository contains a minimal reproduction of a bug in Dagster's config handling when using Python's built-in `Union` type with Pydantic's `discriminator` field.

**Error:** `TypeError: 'str' object is not a mapping`

**Location:** `dagster/_config/pythonic_config/config.py:224`

## How to Reproduce

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the reproduction script:
   ```bash
   python bug_reproduction.py
   ```

## Expected vs Actual Behavior

**Expected:** Config should serialize and deserialize without errors when using discriminated unions.

**Actual:** The deserialization fails with `TypeError: 'str' object is not a mapping` when trying to handle the discriminated union.

## Root Cause

The issue occurs in Dagster's config handling when processing discriminated unions. When a config with a discriminated union is serialized, it creates a structure like:

```python
{'union_field': {'cfg_type': 'type_a'}}
```

During deserialization, Dagster tries to process this as a discriminated union but encounters an issue where `nested_values` is a string instead of a mapping, causing the error when trying to unpack it with `**nested_values`.

The specific error occurs in this line of Dagster's code:
```python
modified_data_by_config_key[config_key] = {
    **nested_values,  # This fails when nested_values is a string
    discriminator_key: discriminated_value,
}
```

## Affected Versions

- Dagster: 1.11.8
- Pydantic: 2.11.7

## Workaround

Use Dagster's `Union` type instead of Python's built-in `Union`:

```python
# Instead of:
union_field: t.Union[SimpleConfigA, SimpleConfigB] = Field(...)

# Use:
union_field: dg.Union[SimpleConfigA, SimpleConfigB] = Field(...)
```

## Stack Trace

The error occurs in Dagster's `_config/pythonic_config/config.py` around line 224 during the `__init__` method when processing discriminated union fields.
