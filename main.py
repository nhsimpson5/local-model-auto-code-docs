import sys
from pipeline import run_pipeline, CONVENTION_BY_LANGUAGE

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "sample_code"
    run_pipeline(target, False, CONVENTION_BY_LANGUAGE)
      
if __name__ == "__main__":
    main()
