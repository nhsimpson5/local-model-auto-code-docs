// Sample C++ file with undocumented functions, a class, and a struct —
// used to test the scanner's C/C++ handling beyond plain C syntax.

namespace mathutils {

int add_numbers(int a, int b) { return a + b; }

int find_max(int *values, int length) {
  int result = values[0];
  for (int i = 1; i < length; i++) {
    if (values[i] > result) {
      result = values[i];
    }
  }
  return result;
}

class Counter {
public:
  Counter(int start = 0) : count(start) {}

  int increment(int step = 1) {
    count += step;
    return count;
  }

private:
  int count;
};

struct Point {
  int x;
  int y;
};

} // namespace mathutils
