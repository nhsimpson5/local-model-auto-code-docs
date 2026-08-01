/* Sample C file with undocumented functions, used to test the scanner. */

int add_numbers(int a, int b) {
    return a + b;
}

int find_max(int *values, int length) {
    int result = values[0];
    for (int i = 1; i < length; i++) {
        if (values[i] > result) {
            result = values[i];
        }
    }
    return result;
}
