//more that 7 reg

int fac(int a) {
	if(a == 0)
		return 0;
	else if (a == 1)
	{
		return 1;
	}
	else
		return fac(a-1)+fac(a-2);
}

int main(){
	int n ;
	get(n);
	int res = fac(n);
	put(res);
}