//ODD - EVEN Mututal recursion

int ev(int);
int od(int);

int main() {
	int a;
	get(a);
	ev(a);
}

void ev(int a) {
	if(a > 0) {
		put(a);
		od(a-1);
	}
}

void od(int b) {
	if(b > 0) {
		put(b);
		ev(b-1);
	}
}