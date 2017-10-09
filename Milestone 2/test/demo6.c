struct s {
    int a;
    float b[5][5];
};

struct t{
    struct s x[10];
};

void f(int * a[10], float b[8][5]) {
    b[1][2] = 10.4;
}

void main() {
    float a[10][10];
    int b[10][10];
    int * c[5];
    struct t y;
    int i;
    float * fp;
    y.x[3].b[1][2] = 4.8;
    f(c,y.x[3].b);
    print(y.x[3].b[1][2]);
}
