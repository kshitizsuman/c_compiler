struct s {
  int a;
  float b;
};

struct t {
  int a;
  float b;
};

void g(int x, float y) {
  printf(x);
  printf("\n");
  printf(y);
}

void main() {
  struct s x;
  struct s y;
  float q;
  x.b = 2.0;
  y = x;
  x.b = -4;
  g(x.b, y.b);
}
