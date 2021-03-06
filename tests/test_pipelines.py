# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import jsone
import pytest
import yaml


@pytest.mark.parametrize(
    "pipeline_file",
    (
        os.path.realpath(os.path.join("infra", f))
        for f in os.listdir("infra")
        if f.endswith(".yml")
    ),
)
def test_jsone_validates(pipeline_file):
    with open(pipeline_file, "r") as f:
        yaml_content = yaml.safe_load(f.read())

    result = jsone.render(yaml_content, context={"version": "42.0"})
    tasks = result["tasks"]

    all_ids = [task["ID"] for task in tasks]

    # Make sure there are no duplicate IDs.
    assert len(all_ids) == len(set(all_ids))

    # Make sure all dependencies are present.
    for task in tasks:
        assert "dependencies" not in task or all(
            dependency in all_ids for dependency in task["dependencies"]
        )
