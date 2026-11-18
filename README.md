# 성적 CSV 검증 프로그램

## ① 무엇을 하나요 (What)
성적 CSV를 읽어 유효한 이름·점수 목록과 건너뛴 행의 이유를 반환합니다.
점수는 0~100의 정수이며, 같은 이름의 행도 모두 남깁니다.

## ② 왜 만들었나요 (Why)
성적의 유효값을 자동으로 판단하고 검사하기 위해서 만들었습니다.

## ③ 어떻게 쓰나요 (How)
Python이 설치된 환경에서 실행합니다.

```powershell
git clone https://github.com/DaeGyu-Park/AI-programing-week11-final.git
cd AI-programing-week11-final
python -m pip install pytest pytest-cov
python load_scores.py scores.csv
```

배포 scores.csv의 결과는 유효 5개, 건너뜀 5개입니다.
여러 파일은 `python check.py scores.csv empty.csv weird.csv`로 확인합니다.

## ④ 어떻게 테스트하나요
```powershell
python -m pytest
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
python -m pytest test_ai_A.py --cov=load_scores --cov-report=term-missing
python -m pytest test_ai_B.py --cov=load_scores --cov-report=term-missing
```

`test_load_scores.py` 실행 결과는 11개 통과·1개 실패입니다. 강의에서 일부러 틀리도록 넣은 `assert len(kept) == 99`를 그대로 유지했으며, 실제 값 5와 달라 실패합니다. 이 파일의 커버리지는 76%입니다.
A 초안은 18개 통과·커버리지 80%, B 초안은 19개 통과·80%입니다.

## ⑤ 파일 구성
- `load_scores.py`: 성적 CSV를 읽는 프로그램
- `scores.csv`, `empty.csv`, `weird.csv`: 실습 데이터
- `test_load_scores.py`: 강의 코드 그대로의 정상·예외·경계값 및 의도적 실패 테스트
- `test_ai_A.py`, `test_ai_B.py`: AI 테스트 초안
- `bug3_logic.py`, `prompts.txt`: 수업의 함정 실험 코드와 프롬프트
- `check.py`: 여러 CSV를 확인하는 도구
- `.gitignore`, `LICENSE`: Python 제외 규칙과 MIT 라이선스

## ⑥ 만든 사람과 AI 사용
박대규 / 학번: 2026100415.
AI는 A/B 초안과 README 작성에 사용했습니다.
