"""명세 제공 조건을 참고해 이 대화에서 생성한 AI 보조 초안. 독립 실험 아님."""
import pytest
from load_scores import load_scores

def test_normal_contract(tmp_path):
    path = tmp_path / "normal.csv"
    path.write_text("name,score\n가람,88\n나래,64\n", encoding="utf-8")
    assert load_scores(path) == ([("가람", 88), ("나래", 64)], [])

def test_file_not_found_contract(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "does_not_exist.csv")

def test_header_only_contract(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("name,score\n", encoding="utf-8")
    assert load_scores(path) == ([], [])

@pytest.mark.parametrize("line", ["가람", "가람,88,비고", ",,"])
def test_invalid_column_contract(tmp_path, line):
    path = tmp_path / "columns.csv"
    path.write_text(f"name,score\n{line}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [] and len(skipped) == 1
    assert skipped[0][0:2] == (2, line) and skipped[0][2]

@pytest.mark.parametrize("raw", ["", "결석", "88.5", "abc"])
def test_non_integer_or_empty_score_contract(tmp_path, raw):
    path = tmp_path / "score.csv"
    path.write_text(f"name,score\n가람,{raw}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [] and len(skipped) == 1
    assert skipped[0][0:2] == (2, f"가람,{raw}") and skipped[0][2]

def test_empty_name_contract(tmp_path):
    path = tmp_path / "name.csv"
    path.write_text("name,score\n,90\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [] and len(skipped) == 1
    assert skipped[0][0:2] == (2, ",90") and skipped[0][2]

def test_duplicate_names_contract(tmp_path):
    path = tmp_path / "duplicates.csv"
    path.write_text("name,score\n가람,88\n가람,91\n", encoding="utf-8")
    assert load_scores(path) == ([("가람", 88), ("가람", 91)], [])

def test_blank_and_quoted_name_contract(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text('name,score\n\n"최,네번",77\n\n', encoding="utf-8")
    assert load_scores(path) == ([("최,네번", 77)], [])

@pytest.mark.parametrize("score,valid", [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)])
def test_score_range_contract(tmp_path, score, valid):
    path = tmp_path / "range.csv"
    path.write_text(f"name,score\n가람,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    if valid:
        assert kept == [("가람", score)] and skipped == []
    else:
        assert kept == [] and len(skipped) == 1
        assert skipped[0][0:2] == (2, f"가람,{score}") and skipped[0][2]
