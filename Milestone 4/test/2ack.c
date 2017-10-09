//Ackerman

int ackermann(int x, int y) {
	int p, t = -1;
	if(x == 0){
		t = y + 1;
	}
	else if(y == 0)
		t = ackermann(x-1,1);
	else{
		t = ackermann(x-1,ackermann(x,y-1));
	}

	return t;
}

int main() {
	int x;
	int y;
	get(x);
	get(y);
	put(ackermann(x,y));
}