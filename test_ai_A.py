"""코드 제공 조건을 참고해 이 대화에서 생성한 AI 보조 초안. 독립 실험 아님."""
import pytest
from load_scores import load_scores

def test_valid_rows(tmp_path):
    path = tmp_path / "a.csv"
    path.write_text("name,score\n가람,80\n나래,90\n", encoding="utf-8")
    assert load_scores(path) == ([("가람", 80), ("나래", 90)], [])

def test_header_only(tmp_path):
    path = tmp_path / "header.csv"
    path.write_text("name,score\n", encoding="utf-8")
    assert load_scores(path) == ([], [])

def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")

@pytest.mark.parametrize("row", ["하나", "하나,20,추가", ",,"])
def test_wrong_column_count(tmp_path, row):
    path = tmp_path / "columns.csv"
    path.write_text(f"name,score\n{row}\n", encoding="utf-8")
    assert load_scores(path) == ([], [(2, row, "열 개수가 2가 아님")])

def test_empty_name(tmp_path):
    path = tmp_path / "name.csv"
    path.write_text("name,score\n   ,90\n", encoding="utf-8")
    assert load_scores(path) == ([], [(2, "   ,90", "이름이 비어 있음")])

@pytest.mark.parametrize("raw,reason", [("", "점수가 비어 있음"), ("결석", "점수가 정수가 아님"), ("88.5", "점수가 정수가 아님")])
def test_invalid_score(tmp_path, raw, reason):
    path = tmp_path / "invalid.csv"
    path.write_text(f"name,score\n하나,{raw}\n", encoding="utf-8")
    assert load_scores(path) == ([], [(2, f"하나,{raw}", reason)])

@pytest.mark.parametrize("score,valid", [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)])
def test_boundaries(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n하나,{score}\n", encoding="utf-8")
    expected = ([("하나", score)], []) if valid else ([], [(2, f"하나,{score}", "점수가 0~100 밖")])
    assert load_scores(path) == expected

def test_duplicate_names_are_preserved(tmp_path):
    path = tmp_path / "duplicates.csv"
    path.write_text("name,score\n하나,80\n하나,90\n", encoding="utf-8")
    assert load_scores(path) == ([("하나", 80), ("하나", 90)], [])

def test_bom_whitespace_blank_and_comma(tmp_path):
    path = tmp_path / "special.csv"
    path.write_text('name,score\n\n"최,네번",77\n  가람  , 80 \n', encoding="utf-8-sig")
    assert load_scores(path) == ([("최,네번", 77), ("가람", 80)], [])
