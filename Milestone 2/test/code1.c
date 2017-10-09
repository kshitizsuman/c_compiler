struct s1{
	int a, b;
	char *d;
};

int foo(int a) {
	struct s1 b;
}

int main() {
	struct s2{
		int a2, b2;
		char *d2;
	};
	int d = s2.a2;

}