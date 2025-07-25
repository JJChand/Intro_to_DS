#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <string>

using namespace std;


void f(int p[], int size) {
    int *a = &p[1];
    for (int i = size-2; i >= 0; i--) {
        a[i] += a[i-1];
    }
}

int main() {
    int a[] = {6, 5, 4, 3, 2, 1};

    int * q = &a[2];
    f(q,3);

    for (int i = 0; i < 6; i++) {
        cout << a[i] << " ";
    }
    return 0;
}