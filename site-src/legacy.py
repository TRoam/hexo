# -*- coding: utf-8 -*-
"""Load preserved public article bodies and static media; no server backups required."""
from pathlib import Path
import json,shutil

def load_legacy(root,out):
    articles=json.loads((root/'content/history.json').read_text())
    assert len(articles)==36
    shutil.copytree(root/'media/history',out/'legacy-assets',dirs_exist_ok=True)
    return articles
