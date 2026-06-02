#!/usr/bin/env bash

source ./tools/linux/set_env.sh

alembic upgrade head
