//TEST CASE: Iterative Fibonacci

int fib(int n) {
	if(n == 0)
		return 0;
	if(n == 1)
		return 1;
	int previous = 0;
	int current = 1;
	int next;
	for(int i=2; i<=n; i++) {
		next = current + previous;
		previous = current;
		current = next;
	}
	return next;
}

int main() {
	int n;
	get(n);
	put(fib(n));
}