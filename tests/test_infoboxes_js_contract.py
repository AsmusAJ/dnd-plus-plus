from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / 'ttrpg' / 'static' / 'js' / 'infiboxes.js'


def test_new_box_template_sets_box_id_attribute():
    js = JS_PATH.read_text()
    assert 'box-id="${boxId}"' in js
    assert '<h5 class="mb-0 pt-2 pb-2 header" box-id="${boxId}"' in js
    assert 'class="mb-0 pt-2 pb-2 header box-id="' not in js
