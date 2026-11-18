"""배포 CSV를 load_scores로 확인하는 명령줄 도구."""
import argparse
from load_scores import load_scores

def main():
    parser = argparse.ArgumentParser(description="성적 CSV의 유효값과 건너뛴 줄 확인")
    parser.add_argument("paths", nargs="+", help="확인할 CSV 경로")
    args = parser.parse_args()
    for path in args.paths:
        kept, skipped = load_scores(path)
        print(f"{path}: 유효 {len(kept)}개, 건너뜀 {len(skipped)}개")
        print("kept:", kept)
        print("skipped:", skipped)

if __name__ == "__main__":
    main()
