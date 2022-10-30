#!/bin/bash
python db_utils/create_tables.py
python db_utils/load_fixtures.py
exec "$@"